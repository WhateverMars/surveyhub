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
            print('======= NO ID ==========')
            return alert(request, "Surveyhub", "If you would like to create a survey please click on the account tab to login or register")

        questions = db.execute("SELECT * FROM questions WHERE number<=:noquestions AND id=:id", noquestions=db.execute("SELECT questions From users WHERE id=:id", id=id)[0]["questions"], id=id)
        
        #return render_template("index.html", questions = questions)
        return render(request, "index.html", {
            'questions' : questions
        })


def account(request):
    if request.user.is_authenticated:
        print('User is logged in as' + str(request.user))
        return alert(request,'User is logged in','')
    
    if request.method == "POST":
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

        user = authenticate(request, username=username, password=password)
        print('user is ' + str(user))
        # Check if authentication successful
        if user is not None:
            print('User is not none')
            login(request, user)
            return HttpResponseRedirect(reverse("account"))
        else:
            print('User is actually none')
            return render(request, "survey/account.html", {
                "message": "Invalid username and/or password."
            })
        
    '''
    
    if request.method == "POST":

        #check username given
        if not request.form.get("username"):
            return alert("username please","")

        #check passwork given
        elif not request.form.get("password"):
            return alert("password please","")

        #check for name in db
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        #check name and password match
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return alert("Invalid username/password","")

        #log user in
        session["user_id"] = rows[0]["id"]
        return alert("Logged in","")

    else:
        
    '''
    return render(request, 'survey/account.html')

def register(request):
    #if the user is already logged in
    if request.user.id:
        return alert(request,"Logged in","")

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]
        email = "N/A"
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(request, "survey/register.html", {
                "message": "Passwords must match."
            })

        #check username given
        if not username:
            return render(request, "survey/register.html", {
                "message": "Invalid Username."
            })
        
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            print(user)
            user.save()
            surveyer = Surveyer(user = user)
            surveyer.save()
        except IntegrityError:
            return render(request, "survey/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
        
        
        #generate hash for password
        #hash=generate_password_hash(request.form.get("password"))

    else:
        return render(request, "survey/register.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def editor(request):
    if request.method == "POST":

        print('----USER id: ' + str(id))
        #record the desired number of questions
        noquestions = User.objects.get(id)
        print(noquestions)
        noquestions = db.execute("SELECT questions From users WHERE id=:id", id=session.get("user_id"))[0]["questions"]

        #Continue loop while questions exist.
        i=1
        while request.form.get("q%i"%i):

            #for cases where there is no question to be updated, insert new question entry
            if not db.execute("SELECT question FROM questions WHERE id=:id AND number=:number", id=session.get("user_id"), number=i):
                db.execute("INSERT INTO questions (id, number, question) VALUES(:id, :number, :question)", id=session.get("user_id"), number=i, question=request.form.get("q%i"%i))

            #if there are previous questions, overwrite them
            else:
                db.execute("UPDATE questions SET question = :question WHERE number =:number AND id= :id", question=request.form.get("q%i"%i), number = i, id = session.get("user_id"))

            #continue loop while anwers exist.
            j = 1
            noanswers = 0
            while request.form.get("q"+str(i)+"a"+ str(j)):
                db.execute("UPDATE questions SET ans"+str(j)+" =:ans WHERE number =:number AND id= :id", ans=request.form.get("q"+str(i)+"a"+ str(j)), number = i, id = session.get("user_id"))
                noanswers += 1
                j += 1
            #record how many answers each question has
            db.execute("UPDATE questions SET type=:type WHERE number =:number AND id=:id", type=noanswers, number=i, id=session.get("user_id"))
            i += 1

        #set the number of questions the user has in their survey
        db.execute("UPDATE users SET questions=:questions WHERE id=:id", questions=i-1, id=session.get("user_id"))

        return alert("Questions saved", "")

    else:
        print('_____________')
        #print(request.GET.get('noquestions'))
        if request.GET.get('noquestions'):
            noquestions = int(request.GET.get('noquestions'))
        else:
            noquestions = 0
        #pass through previous questions for autofill from current survey
        print('----User below----')
        print(request.user)
        #questions = db.execute("SELECT * FROM questions WHERE number<=:noquestions AND id=:id", noquestions=db.execute("SELECT questions From users WHERE id=:id", id=session.get("user_id"))[0]["questions"], id=session.get("user_id"))
        questions = Question.objects.filter(asker=request.user.id)
        print('----questions below----')
        print(questions)
        #users = db.execute("SELECT * FROM users WHERE id=:id", id=session.get("user_id"))
        #users_no_questions=int(users[0]["questions"])
        users_no_questions=int(Surveyer.objects.get(user = request.user.id).questions)
        print('----number of questions below----')
        print(users_no_questions)
        #return render_template("editor.html",questions=questions, users=users, users_no_questions=users_no_questions, noquestions=int(request.args.get("noquestions", 0)))
        return render(request, 'survey/tester.html', {
            'questions' : questions,
            'range' : range(1,noquestions+1),
            'users_no_questions' : users_no_questions
        })




#this page is flexable to display as required
def alert(request, message, message2):
    return render(request, "survey/alert.html", {
                "message": message,
                "message2": message2
            })