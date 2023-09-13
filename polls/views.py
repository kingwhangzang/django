from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.template import loader

from .models import Choice, Question


def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5] 
    #출판일자를 정렬하여 5개까지만 나타내겠다.
    template = loader.get_template("polls/index.html")
    context = {
        "latest_question_list": latest_question_list,
    }
    return render(request, "polls/index.html", context)
    #return HttpResponse(template.render(context, request)) - render 없이 사용한 경우

def detail (request, question_id) :
    question = get_object_or_404(Question, pk = question_id)
    return render(request, "polls/detail.html", {"question": question})
    
    # try :
    #    question = Question.objects.get(pk = question_id)
    # except Question.DoesNotExist :
    #     raise Http404("Question does not exist")
    # return render(request, "polls/detail.html", {"question": question})
    
    #return HttpResponse("You're looking at question %s" % question_id)

def results (request, question_id):
    response = "You're looking at the results of question %s"
    return HttpResponse(response % question_id)

def vote (request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
    
#view 는 request 라는 인자를 받고, HttpResponse 라는 함수를 리턴하낟
#client 로 부터 request 를 받으면 request 에는 여러가지 정보가 담겨 있고, 이를 response 해준다.
