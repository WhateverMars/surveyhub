import csv

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from survey.models import Surveyer, User, Question, Result, Analysis
from survey.utils import random_string, alert


def index(request):

    # if survey submitted
    if request.method == "POST":

        # record the surveyer and calculate which number person surveyed this is
        surveyer = Surveyer.objects.get(user=User(id=request.POST["asker"]))

        noquestions = Surveyer.objects.get(user=surveyer).questions

        users = Result.objects.filter(asker=surveyer.user).values("user").distinct()

        usernum = len(users) + 1

        # record their selected answer for each question to the results table. Iterate through all questions
        for i in range(noquestions):

            number = i + 1
            question = Question.objects.get(asker=surveyer.user, number=number)

            # dynamically request answer
            answer = request.POST["%i" % (number)]

            # save results to db
            r = Result(
                asker=surveyer.user,
                user=usernum,
                number=number,
                question=question.question,
                type=question.type,
                answer=answer,
            )
            r.save()

        # show results received
        return alert(request, "Results saved", "Thank you")

    else:
        # Checks which surveyer gave this user the survey.
        surveyer = Surveyer.objects.filter(link=request.GET.get("id")).first()

        # if no id, present with homepage
        if not surveyer:
            if request.user.is_authenticated:
                return account(request)
            else:
                return alert(
                    request,
                    "QuestioNet",
                    "If you would like to create a survey please click on the account tab to login or register.",
                )

        # if user gets a survey from someone else
        if surveyer.user.username != request.user.username:
            logout(request)

        # give questions

        questions = Question.objects.filter(
            asker=surveyer.user.id, number__lte=surveyer.questions
        )

        return render(request, "survey/index.html", {"questions": questions})


def account(request):

    # if the user is already logged in
    if request.user.is_authenticated:
        return alert(
            request,
            f"Welcome {request.user.username}!",
            "You can now create or edit surveys.",
        )

    if request.method == "POST":
        # retrieve posted data
        username = request.POST["username"]
        password = request.POST["password"]

        # if no username or password given
        if not username:
            return render(
                request, "survey/account.html", {"message": "username not valid"}
            )

        if not password:
            return render(
                request, "survey/account.html", {"message": "password not valid"}
            )

        # Check if authentication successful
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # authentication success
            login(request, user)
            return HttpResponseRedirect(reverse("account"))
        else:
            # unable to authenticate
            return render(
                request,
                "survey/account.html",
                {"message": "Invalid username and/or password."},
            )

    return render(request, "survey/account.html")


def register(request):

    # if the user is already logged in
    if request.user.id:
        return alert(request, "Logged in", "")

    if request.method == "POST":

        # take in the posted data
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]
        confirmation = request.POST["confirmation"]
        link = random_string(10)

        # check if the passwords match
        if password != confirmation:
            return render(
                request, "survey/register.html", {"message": "Passwords must match."}
            )

        # check if username given
        if not username:
            return render(
                request, "survey/register.html", {"message": "Invalid Username."}
            )

        # Attempt to create new user in both the user and surveyer models. These are then linked.
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            surveyer = Surveyer(user=user, link=link)
            surveyer.save()
        except IntegrityError:
            return render(
                request, "survey/register.html", {"message": "Username already taken."}
            )

        # log user in
        login(request, user)
        return account(request)

    else:
        return render(request, "survey/register.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


@login_required(login_url="/account")
def editor(request):
    if request.method == "POST":
        data = request.POST

        number_of_questions = max(
            int(key[1:])
            for key in data.keys()
            if key.startswith("q") and key[1:].isdigit() and data[key]
        )

        # Structure data as a list of dictionaries
        data = []
        for i in range(1, number_of_questions + 1):
            question_data = {}
            for key, value in request.POST.items():
                if key.startswith(f"q{i}"):
                    if "a" in key:
                        # Change the key to "ans1", "ans2", etc.
                        answer_number = key.split("a")[1]
                        question_data[f"ans{answer_number}"] = value
                    else:
                        question_data["question"] = value
            data.append(question_data)

        # Now data is a list of dictionaries, each containing the question and answers for a question
        i = 1
        for question_set in data:

            question_text = question_set["question"]
            if not question_text:
                continue

            question_obj, _ = Question.objects.get_or_create(
                asker=request.user,
                number=i,
            )
            question_obj.question = question_text

            # record all the answers and save them
            answers = [
                question_set[f"ans{j}"] for j in range(1, 7) if question_set[f"ans{j}"]
            ]
            for j in range(len(answers)):
                setattr(question_obj, f"ans{j+1}", answers[j] or None)

            # saving the number of answers
            question_obj.type = len(answers)
            question_obj.save()

            i += 1

        # set the number of questions the user has in their survey
        s = Surveyer.objects.get(user=request.user.id)
        s.questions = number_of_questions
        s.save()
        return alert(request, "Questions saved.", "You can now share your survey.")

    else:

        # check the GET to see how many questions the user wants
        if request.GET.get("noquestions"):
            if Surveyer.objects.get(user=request.user.id).questions != int(
                request.GET.get("noquestions")
            ):
                noquestions = int(request.GET.get("noquestions"))
            else:
                noquestions = Surveyer.objects.get(user=request.user.id).questions
        else:
            noquestions = Surveyer.objects.get(user=request.user.id).questions

        # pass through previous questions for autofill from current survey
        questions = Question.objects.filter(
            asker=request.user.id, number__lte=noquestions
        )

        existing_questions = Question.objects.filter(asker=request.user.id).count()

        # # update the number of questions for the user.
        # s = Surveyer.objects.get(user=request.user.id)
        # s.questions = noquestions
        # s.save()

        return render(
            request,
            "survey/editor.html",
            {
                "questions": questions,
                "range_new": range(1, noquestions + 1),
                "range_existing": range(existing_questions + 1, noquestions + 1),
                "users_no_questions": noquestions,
            },
        )


@login_required(login_url="/account")
def results(request):

    results = Result.objects.filter(asker=request.user.id)

    # if the user has not recieved any results yet
    if not results:
        return alert(
            request,
            "No results yet.",
            "Check back later once your survey has been answered.",
        )

    # write the results to a csv file.
    with open(
        f"survey/static/results/results{request.user.id}.csv",
        "w",
    ) as csvfile:

        # creating a csv writer object
        writer = csv.writer(csvfile)

        # writing the column titles
        writer.writerow(["user number", "question number", "question", "answer"])

        # write each row of data
        for row in results:
            writer.writerow(
                [
                    row.user,
                    row.number,
                    row.question,
                    row.answer,
                ]
            )

    surveyed = Result.objects.filter(asker=request.user.id).last().user

    number_of_questions = Surveyer.objects.get(user=request.user.id).questions

    questions = Question.objects.filter(asker=request.user.id)
    number = 1
    # summerise results
    for question in questions[:number_of_questions]:
        # count the number of votes for each answer for this question
        ans1count = Result.objects.filter(
            asker=request.user.id, number=number, answer=question.ans1
        ).count()
        ans2count = Result.objects.filter(
            asker=request.user.id, number=number, answer=question.ans2
        ).count()
        ans3count = Result.objects.filter(
            asker=request.user.id, number=number, answer=question.ans3
        ).count()
        ans4count = Result.objects.filter(
            asker=request.user.id, number=number, answer=question.ans4
        ).count()
        ans5count = Result.objects.filter(
            asker=request.user.id, number=number, answer=question.ans5
        ).count()
        ans6count = Result.objects.filter(
            asker=request.user.id, number=number, answer=question.ans6
        ).count()

        analysis, _ = Analysis.objects.get_or_create(
            asker=request.user, number=number,
            defaults={
                'ans1count': ans1count,
                'ans2count': ans2count,
                'ans3count': ans3count,
                'ans4count': ans4count,
                'ans5count': ans5count,
                'ans6count': ans6count,
                "userstot": surveyed,
            }
        )
        analysis.userstot = surveyed
        analysis.number = number
        analysis.question = question.question
        analysis.ans1count = ans1count
        analysis.ans2count = ans2count
        analysis.ans3count = ans3count
        analysis.ans4count = ans4count
        analysis.ans5count = ans5count
        analysis.ans6count = ans6count
        analysis.ans1 = question.ans1
        analysis.ans2 = question.ans2
        analysis.ans3 = question.ans3
        analysis.ans4 = question.ans4
        analysis.ans5 = question.ans5
        analysis.ans6 = question.ans6
        analysis.save()

        number += 1

    analysis = Analysis.objects.filter(asker=request.user.id)[:number_of_questions]

    # return both the results and the analysis table.
    return render(
        request,
        "survey/results.html",
        {"results": results, "analysis": analysis, "surveyed": surveyed},
    )


@login_required(login_url="/account")
def cleardata(request):

    # This allows for double checking with the user on deletion decision
    if request.method == "POST":
        # delete all data from both the Results and Analysis tables
        Result.objects.filter(asker=request.user).delete()
        Analysis.objects.filter(asker=request.user).delete()
        return alert(request, "Data Deleted", "")

    return render(request, "survey/delete.html")
