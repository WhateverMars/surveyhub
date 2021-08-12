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
    #todo

    #create global variable to recieve the indicator of which survey to use
    global temp_id

    #if data submittwed
    if request.method == "POST":
        id = temp_id
        noquestions = db.execute("SELECT questions From users WHERE id=:id", id=id)[0]["questions"]
        rows = db.execute("SELECT * FROM questions WHERE id =:id", id=id)
        users = db.execute("SELECT DISTINCT user FROM results WHERE id =:id", id=id)
        usernum = len(users) + 1

        #record their selected answer for each question to the results table. Iterate through all questions
        for i in range(noquestions):
            number = i + 1
            question=db.execute("SELECT question FROM questions WHERE id=:id AND number=:number", id=id, number = number)[0]["question"]
            answer=request.form.get("%i" % (number))
            db.execute("INSERT INTO results (id, user, number, question, answer) VALUES (:id, :user, :number, :question, :answer)", id=id, user=usernum, number=number, question=question, answer=answer)
        return alert("Results saved", "Thank you")
    else:
        #Checks which admin gave this user the survey.
        
        print('_________')
        print(request.GET.get('id'))
        id = request.GET.get('id')
        temp_id = request.GET.get('id')

        #if no id, present with homepage
        if not id:
            return alert(request, "Surveyhub", "If you would like to create a survey please click on the account tab to login or register")

        questions = db.execute("SELECT * FROM questions WHERE number<=:noquestions AND id=:id", noquestions=db.execute("SELECT questions From users WHERE id=:id", id=id)[0]["questions"], id=id)
        
        return render(request, "index.html", {
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

    #if the user is already logged in
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


            noanswers = 0
            
            # record how many answers the question has       
            if a.ans6 == '':
                print('there is no sixth answer')
                if a.ans5 == '':
                    print('there is no fifth answer')
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




# this page is flexable to display messages as required
def alert(request, message, message2):
    return render(request, "survey/alert.html", {
                "message": message,
                "message2": message2
            })