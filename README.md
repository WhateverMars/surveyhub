# QuestioNet (previosly surveyhub)

This is QuestioNet, a site for creating and sharing custom surveys. It is currently a fully functional but will receive additional updates. I am currently readying it for server stage production and will host it on pythonanywhere.
![Survey Editor page](/images/welcomepage.jpg)

This site is built primarily in Python using the Django framework. It uses sqlite to manage the database of surveys, results and user accounts. It uses html and css for the webpages and JavaScript to add some dynamic functions to pages such as login and registration functions.

## Usage

A user who would like to create a survey will first need to register an account. All they'll need is an email address, username and password. The password requirements are given as soon as they begin typing in the password field and disappear once a requirement is met. Currently the requirements are that the password must have at least 8 characters, a upper case character and a lower case character. The password is hashed by default through django's default user model.

![Survey Editor page](/images/editor.jpg)

Once they have an account they can click through to the editor page where they can select how many questions they would like their survey to have. They then can type in their questions and the multiple choice answers. They can have as few as 2 answers or as many as 6.

Once they click the save survey button, the survey is saved to the database and they are provided with a link to share the survey. Survey participants do not need accounts to complete the survey and only need to follow the link, answer the questions and hit submit.

![Survey Editor page](/images/results1.jpg)

Later the surveyor will be able to check back and click onto the results page. This page displays an automatic breakdown of the results and the raw collected data is also provided towards the bottom of the page. Further down the page is an export button which will download all the data in the form of a csv file so that they can do their own analysis if needed. Below this there is a delete button which permanently deletes all the results after confirming the users decision.

![Survey Editor page](/images/results2.jpg)

![Survey Results page](/images/results3.jpg)