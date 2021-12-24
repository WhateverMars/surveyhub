# QuestioNet(previously SuveyHub)

This web app is my final project for cs50w.

## Aims

The aim of this site was to build a fully functioning site where a user can create custom anonymous surveys or questionnaires. These would be flexible in how many questions are selected and how many possible answers per question. The survey can then be shared by simply sending a generic link whereby anyone who clicks on the link is brought to the survey. A results page will give the original user a breakdown of the results and the raw data.

## Structure

The site is now fully operational and has been submitted for the assignment. I am currently readying it for server stage production and will host it on pythonanywhere.

This site is built primarily in Python using the Django framework. It uses sqlite to manage the database of surveys, results and user accounts. It uses html and css for the webpages and JavaScript to add some dynamic functions to pages such as login and registration functions.

It uses the standard django structure. For the results page a .csv file is generated with the raw data from the survey answers. These are stored in the static files folder and are given in the form 'results44.csv' where 44 would be the user's id.

The views.py file contains the bulk of the project's functions while some functions are in the templates using django's template syntax.

In the util.py file is a function to create a random string of characters of given lenght. This is used to generate the link address which directs to the survey.

The site's logo was created at https://www.ucraft.com/free-logo-maker#create-logo

## Usage

A user who would like to create a survey will first need to register an account. All they'll need is an email address, username and password. The password requirements are given as soon as they begin typing in the password field and disappear once a requirement is met. Currently the requirements are that the password must have at least 8 characters, a upper case character and a lower case character.

Once they have an account they can click through to the editor page where they can select how many questions they would like their survey to have. They then can type in their questions and the multiple choice answers. They can have as few as 2 answers or as many as 6.

Once they click the save survey button, the survey is saved to the database and they are provided with a link to share the survey. Survey participants do not need accounts to complete the survey and only need to follow the link, answer the questions and hit submit.

Later the surveyor will be able to check back and click onto the results page. This page displays an automatic breakdown of the results and the raw collected data is also provided towards the bottom of the page. Further down the page is an export button which will download all the data in the form of a csv file so that they can do their own analysis if needed. Below this there is a delete button which permanently deletes all the results after confirming the users decision.

## Distinctiveness and Complexity

The project ties together everything learned during the course while being distinct from any of the assignments in structure and scope.
The most complex parts of the project was structuring the four different models to store user details such as logins and the number of questions in their survey, survey details such as the questions and answers and who owns the survey, results details such as how many results per survey, which question had which answers and finally the analysis model which combined the question details and answer stats for each survey.

The site is fully mobile compatible. Much of the html is formatted using flex and measurements given in virtual width or height which means most of it scaled automatically for different sized screens. At very narrow extremes the queries.css file changes the shape of the navigation bar and the survey's answer section.

## Running the program

There is a requirements.txt to install using 'pip install -r requirement.txt' and the project can then be run using 'python manage.py runserver'