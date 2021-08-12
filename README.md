# Surveyhub

This is SurveyHub a site for creating and sharing custom surveys. It is currently a work in progress.

This site is built primarily in Python through the Django framework. It uses sqlite to manage the database of surveys, results and user accounts.

A user who would like to create a survey will first need to register an account. At present all they'll need is a username and password. Later I will likely add an email address option and stricter password requirements. Currently the password can be anything, for testing convenience. The password is hashed by default through django's default user model.

Once they have an account they can click through to the editor page where they can select how many questions they would like their survey to have. They then can type in their questions and the multiple choice answers. They can have as few as 2 answers or as many as 6. I may increase this limit later.

Once they click the save survey button, the survey is saved to the database and they are provided with a link to share the survey. Survey participants do not need accounts to complete the survey and only need to follow the link, answer the questions and hit submit.

Later the surveyor will be able to check back and click onto the results page. Once this page is completed it will display a breakdown of the results and lowerdown the raw collected data will also be given. There will also be an export button which will provide all the data in a csv file for their own analysis. There will also be a delete button which permanently deletes all the results.