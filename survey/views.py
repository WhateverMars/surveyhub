from django.db.models import query
from django.db.models.fields import EmailField
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Surveyer, User, Question, Result, Analysis
from django.urls import reverse
from django.db import IntegrityError
from .util import random_string
import random
import csv


def index(request):
    
    #if survey submitted
    if request.method == "POST":
        
        # record the surveyer and calculate which number person surveyed this is
        surveyer = Surveyer.objects.get(user=User(id = request.POST['asker']))
                
        noquestions = Surveyer.objects.get(user = surveyer).questions
                
        users = Result.objects.filter(asker = surveyer.user).values('user').distinct()
        
        usernum = len(users) + 1
        

        # record their selected answer for each question to the results table. Iterate through all questions
        for i in range(noquestions):

            number = i + 1
            question = Question.objects.get(asker = surveyer.user, number = number)
            
            # dynamically request answer
            answer = request.POST['%i' % (number)]
            
            # save results to db
            r = Result(asker=surveyer.user, user=usernum, number=number, question=question.question, type=question.type, answer=answer)
            r.save()

        # show results received    
        return alert(request, "Results saved", "Thank you")

    else:
        # Checks which surveyer gave this user the survey.
        surveyer = Surveyer.objects.filter(link = request.GET.get('id')).first()
        
        # if no id, present with homepage
        if not surveyer:
            if request.user.is_authenticated:
                return account(request)
            else:
                return alert(request, "QuestioNet", "If you would like to create a survey please click on the account tab to login or register.")

        # give questions
        questions = Question.objects.filter(asker = surveyer.user.id, number__lte = surveyer.questions)

        return render(request, "survey/index.html", {
            'questions' : questions
        })


def account(request):

    # if the user is already logged in
    if request.user.is_authenticated:
        return alert(request,'Welcome ' + request.user.username+'!','You can now create or edit surveys.')
    
    if request.method == "POST":
        # retrieve posted data
        username = request.POST['username']
        password = request.POST['password']

        # if no username or password given
        if not username:
            return render(request, 'survey/account.html', {
                'message' : 'username not valid'
            })

        if not password:
            return render(request, 'survey/account.html', {
                'message' : 'password not valid'
            })
        
        # Check if authentication successful
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # authentication success
            login(request, user)
            return HttpResponseRedirect(reverse("account"))
        else:
            # unable to authenticate
            return render(request, "survey/account.html", {
                "message": "Invalid username and/or password."
            })
        
    return render(request, 'survey/account.html')

def register(request):

    # if the user is already logged in
    if request.user.id:
        return alert(request,"Logged in","")

    if request.method == "POST":

        # take in the posted data
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["password"]
        confirmation = request.POST["confirmation"]
        link = random_string(10)

        # check if the passwords match
        if password != confirmation:
            return render(request, "survey/register.html", {
                "message": "Passwords must match."
            })

        # check if username given
        if not username:
            return render(request, "survey/register.html", {
                "message": "Invalid Username."
            })
        
        # Attempt to create new user in both the user and surveyer models. These are then linked.
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            surveyer = Surveyer(user = user, link = link)
            surveyer.save()
        except IntegrityError:
            return render(request, "survey/register.html", {
                "message": "Username already taken."
            })

        # log user in
        login(request, user)
        return account(request)
        
    else:
        return render(request, "survey/register.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

@login_required(login_url='/account')
def editor(request):
    if request.method == "POST":

        # Continue loop while questions exist.
        i=1
        while i-1 < Surveyer.objects.get(user = request.user.id).questions:

            # for cases where there is no question to be updated, add a new question entry
            
            if not Question.objects.filter(asker = request.user.id, number = i):
                # if they're adding a new question to the existing survey
                q = Question(asker=request.user, number=i, question = request.POST['q%i'%i])
                q.save()
            else:
                # if there already exists a question numbered the same
                q = Question.objects.get(asker = request.user.id, number = i)
                q.question = request.POST['q%i'%i]
                q.save()
            
            # record all the answers and save them
            a = Question.objects.get(asker = request.user.id, number = i)
            a.ans1 = request.POST['q'+str(i)+'a'+ str(1)]
            a.ans2 = request.POST['q'+str(i)+'a'+ str(2)]
            a.ans3 = request.POST['q'+str(i)+'a'+ str(3)]
            a.ans4 = request.POST['q'+str(i)+'a'+ str(4)]
            a.ans5 = request.POST['q'+str(i)+'a'+ str(5)]
            a.ans6 = request.POST['q'+str(i)+'a'+ str(6)]
            a.save()

            # reset no answers each time
            noanswers = 0
            
            # record how many answers the question has       
            if a.ans6 == '':
                if a.ans5 == '':
                    if a.ans4 == '':
                        if a.ans3 == '':
                            noanswers = 2
                        else:
                            noanswers = 3
                    else:
                        noanswers = 4
                else:
                    noanswers = 5
            else:
                noanswers = 6    

            # saving the number of answers
            t = Question.objects.get(asker = request.user.id, number = i)
            t.type = noanswers
            t.save()

            # move to the next question
            i += 1

        # set the number of questions the user has in their survey
        s = Surveyer.objects.get(user = request.user.id)
        s.questions = i-1
        s.save()
        return alert(request, "Questions saved.", "You can now share your survey.")

    else:
        
        # check the GET to see how many questions the user wants
        if request.GET.get('noquestions'):
            if Surveyer.objects.get(user = request.user.id).questions != int(request.GET.get('noquestions')):
                noquestions = int(request.GET.get('noquestions'))
            else:
                noquestions = Surveyer.objects.get(user = request.user.id).questions
        else:
            noquestions = Surveyer.objects.get(user = request.user.id).questions


        # pass through previous questions for autofill from current survey
        questions = Question.objects.filter(asker=request.user.id, number__lte=noquestions)
                
        existing_questions = Question.objects.filter(asker = request.user.id).count()
        
        # update the number of questions for the user.
        s = Surveyer.objects.get(user = request.user.id)
        s.questions = noquestions
        s.save()
        
        return render(request, 'survey/editor.html', {
            'questions' : questions,
            'range_new' : range(1,noquestions+1),
            'range_existing' : range(existing_questions+1,noquestions+1),
            'users_no_questions' : noquestions
        })

@login_required(login_url='/account')
def results(request):
    
    results = Result.objects.filter(asker = request.user.id)
    
    # if the user has not recieved any results yet
    if not results:
        return alert(request, "No results yet.","Check back later once your survey has been answered.")

    # write the results to a csv file.

    # swap below statements when deploying to pythonanywhere or running locally
    with open("survey/static/results"+ str(request.user.id) +".csv", 'w') as csvfile:

    #with open("/home/QuestioNet/surveyhub/survey/static/results"+ str(request.user.id) +".csv", 'w') as csvfile:
        
        # creating a csv writer object
        writer = csv.writer(csvfile)

        # writing the column titles
        writer.writerow(["user number", "question number", "question", "answer"])

        # write each row of data
        i=0
        for row in results:
            writer.writerow([results[i].user, results[i].number, results[i].question, results[i].answer])
            i +=1

    
    surveyed = Result.objects.filter(asker = request.user.id).last().user
    
    noquestions = Surveyer.objects.get(user = request.user.id).questions
    
    questions = Question.objects.filter(asker = request.user.id)

    # summerise results
    for i in range(noquestions):
        number = i + 1
        # count the number of votes for each answer for this question
        ans1count = Result.objects.filter(asker = request.user.id, number = number, answer = questions[i].ans1).count()
        ans2count = Result.objects.filter(asker = request.user.id, number =number, answer = questions[i].ans2).count()
        ans3count = Result.objects.filter(asker = request.user.id, number = number, answer = questions[i].ans3).count()
        ans4count = Result.objects.filter(asker = request.user.id, number = number, answer = questions[i].ans4).count()
        ans5count = Result.objects.filter(asker = request.user.id, number = number, answer = questions[i].ans5).count()
        ans6count = Result.objects.filter(asker = request.user.id, number = number, answer = questions[i].ans6).count()
        
        # Update the analysis table
        if not Analysis.objects.filter(asker = request.user.id, number=number):
            a = Analysis(asker = request.user, userstot = surveyed, number=number, question=questions[i].question, ans1count=ans1count, ans2count=ans2count, ans3count=ans3count, ans4count=ans4count, ans5count=ans5count, ans6count=ans6count, ans1=questions[i].ans1, ans2=questions[i].ans2, ans3=questions[i].ans3, ans4=questions[i].ans4, ans5=questions[i].ans5, ans6=questions[i].ans6)
            a.save()

        # if there are previous entries, overwrite them
        else:
            Analysis.objects.filter(asker = request.user.id, number=number).delete()
            a = Analysis(asker = request.user, userstot = surveyed, number=number, question=questions[i].question, ans1count=ans1count, ans2count=ans2count, ans3count=ans3count, ans4count=ans4count, ans5count=ans5count, ans6count=ans6count, ans1=questions[i].ans1, ans2=questions[i].ans2, ans3=questions[i].ans3, ans4=questions[i].ans4, ans5=questions[i].ans5, ans6=questions[i].ans6)
            a.save()

    analysis = Analysis.objects.filter(asker = request.user.id)

    # return both the results and the analysis table.
    return render(request, 'survey/results.html', {
        'results' : results,
        'analysis' : analysis,
        'surveyed' : surveyed
    })


@login_required(login_url='/account')
def cleardata(request):

    # This allows for double checking with the user on deletion decision
    if request.method == 'POST':
        # delete all data from both the Results and Analysis tables
        Result.objects.filter(asker=request.user).delete()
        Analysis.objects.filter(asker=request.user).delete()
        return alert(request, 'Data Deleted', '')

    return render(request, "survey/delete.html")

# this page is flexable to display messages as required
def alert(request, message, message2):

    # checks if the user is logged in
    if request.user.id:
        # this simply checks if the user has created a survey already
        questions = Question.objects.filter(asker = request.user)
        return render(request, "survey/alert.html", {
                    'message': message,
                    'message2': message2,
                    'questions' : questions
                })

    return render(request, "survey/alert.html", {
                    'message': message,
                    'message2': message2
                })