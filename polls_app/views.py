from django.forms import ValidationError
from django.shortcuts import redirect, render, reverse
from .models import Question, Choice
import re
from extra_views import *

def question_list(request):
    my_data = {}

    if request.method == "POST":

        do_delete = "delete_question" in request.POST 

        try:
            if do_delete:
                question_id_to_delete = request.POST["delete_question"]
                Question.objects.get(id=question_id_to_delete).delete()
            else:
                q = Question()
                q.question_text = request.POST["question"]
                q.full_clean() # raise a validateion error if something in our model record was invalid
                q.save()
        except ValidationError as ve:
            my_data["error"] = ve.message_dict


    my_data["all_questions"] = Question.objects.all()

    return render(request, "pages/question_list.html", my_data)
    


def question_detail(request, question_id):
    my_data = {}

    if request.method == "POST":
        try:
            choice_id = request.POST["choice"]
            c = Choice.objects.get(id=choice_id)
            c.votes += 1
            c.full_clean() # raise a validateion error if something in our model record was invalid
            c.save()

        except ValidationError as ve:
            my_data["error"] = ve.message_dict

    my_data["question"] = Question.objects.get(id=question_id)
    return render(request, "pages/question_detail.html", my_data)


def question_edit(request, question_id):
    my_data = {}

    if request.method == "POST":
        try:
            q = Question.objects.get(pk=question_id)
            q.question_text = request.POST["question"]
            q.full_clean() # raise a validateion error if something in our model record was invalid
            q.save()

            for field in request.POST:
                pattern = r"choice-(\d+)" # group #1 will be the id of the choice
                match = re.search(pattern, field)
                if match:
                    c = Choice.objects.get(id=match.group(1))
                    c.choice_text = request.POST[field]
                    c.full_clean()
                    c.save()

            return redirect(reverse("question-detail", args=(question_id, )))

        except ValidationError as ve:
            my_data["error"] = ve.message_dict


    my_data["question"] = Question.objects.get(id=question_id)
    return render(request, "pages/question_edit.html", my_data)
