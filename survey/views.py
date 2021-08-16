from django.db.models.fields import EmailField
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Surveyer, User, Question, Result, Analysis
from django.urls import reverse
from django.db import IntegrityError

# Create your views here.
#def index(request):
#    return render(request, "survey/alert.html")

def index(request):
    
    #if survey submittwed
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
        id = request.GET.get('id')

        # if no id, present with homepage
        if not id:
            return alert(request, "Surveyhub", "If you would like to create a survey please click on the account tab to login or register")

        # give questions
        questions = Question.objects.filter(asker = id)
        return render(request, "survey/index.html", {
            'questions' : questions
        })


def account(request):

    # if the user is already logged in
    if request.user.is_authenticated:
        return alert(request,'User is logged in','')
    
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
        email = "N/A"
        confirmation = request.POST["confirmation"]

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
            surveyer = Surveyer(user = user)
            surveyer.save()
        except IntegrityError:
            return render(request, "survey/register.html", {
                "message": "Username already taken."
            })

        # log user in
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
        
    else:
        return render(request, "survey/register.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

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
        return alert(request, "Questions saved", "")

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

def results(request):
    return render(request, 'survey/tester.html')


# this page is flexable to display messages as required
def alert(request, message, message2):
    return render(request, "survey/alert.html", {
                "message": message,
                "message2": message2
            })