from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render

from survey.models import Surveyer, Question
from survey.utils import alert


class EditorView(LoginRequiredMixin, View):
    login_url = "/account"

    def post(self, request):
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

    def get(self, request):
        # check the GET to see how many questions the user wants
        noquestions = (
            int(request.GET.get("noquestions"))
            if int(request.GET.get("noquestions"))
            != Surveyer.objects.get(user=request.user.id).questions
            else Surveyer.objects.get(user=request.user.id).questions
        )

        # pass through previous questions for autofill from current survey
        questions = Question.objects.filter(
            asker=request.user.id, number__lte=noquestions
        )

        existing_questions = Question.objects.filter(asker=request.user.id).count()

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
