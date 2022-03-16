from django.forms import ValidationError
from django.shortcuts import redirect, render, reverse
from .models import Question, Choice
import re

def question_list(request):
    my_data = {}

    if request.method == "POST":

        delete_question = "delete_question" in request.POST # dictionary field names + field values

        try:
            if delete_question:
                question_id_to_delete = request.POST["delete_question"]
                q = Question.objects.get(id=question_id_to_delete)
                if q.can_delete:
                    q.delete()
                else:
                    my_data["error"] = "YOU CAN NOT DELETE THIS QUESTION!!!!!!!!"
                
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
            add_new_choice = "choice_new" in request.POST

            if add_new_choice:
                c = Choice()
                c.choice_text = request.POST["choice"]
                c.votes = 0
                c.question = Question.objects.get(id=question_id)
                c.full_clean()
                c.save()

            else:
                q = Question.objects.get(pk=question_id)
                q.question_text = request.POST["question"]
                q.full_clean() # raise a validateion error if something in our model record was invalid
                q.save()

                for field in request.POST:
                    pattern = r"choice-(\d+)" # group #1 will be the id of the choice  ... choice-17
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
