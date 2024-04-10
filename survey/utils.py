import random

from django.shortcuts import render

from survey.models import Question


# this is used to generate a link for the users survey
def random_string(size):
    rand_str = ""
    for i in range(size):
        rand_int = random.randint(97, 122)
        if random.randint(0, 1):
            rand_int -= 32
        rand_str += chr(rand_int)
    return rand_str


# this page is flexable to display messages as required
def alert(request, message, message2):

    # checks if the user is logged in
    if request.user.id:
        # this simply checks if the user has created a survey already
        questions = Question.objects.filter(asker=request.user)
        return render(
            request,
            "survey/alert.html",
            {"message": message, "message2": message2, "questions": questions},
        )

    return render(
        request, "survey/alert.html", {"message": message, "message2": message2}
    )
