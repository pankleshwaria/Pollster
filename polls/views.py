from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from .models import Questions, Choices
from datetime import datetime


# Get questions and display them
def index(request):
    latest_question_list = Questions.objects.order_by('-pub_date')
    context = {'latest_question_list': latest_question_list}

    return render(request, 'polls/index.html', context=context)


# Show specific question and their choices
def detail(request, question_id):
    try:
        question = Questions.objects.get(pk=question_id)
    except Questions.DoseNotExist:
        raise Http404("Question dose not exists")

    return render(request, 'polls/detail.html', {'question': question})


# Get object and show result
def results(request, question_id):
    question = get_object_or_404(Questions, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


# Vote for a question choice
def vote(request, question_id):
    question = get_object_or_404(Questions, pk=question_id)
    try:
        selected_choice = question.choices_set.get(pk=request.POST['choice'])
    except (KeyError, Choices.DoesNotExist):
        # Display the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't selected a choice"
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice after
        # user hits the back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))


# Add a new question
def add_question(request):

    if request.method == 'POST':

        print()
        print(type(request.POST.get('question', None)))
        print()

        if request.POST.get("question", "") == "" or request.POST.get("choice", "") == "":
            context = {
                "error_message": "Question/Choice filed cannot be empty",
            }
            return render(request, 'polls/create_question.html', context=context)

        question = Questions(question_text=request.POST.get('question'), pub_date=datetime.now())

        options = request.POST.getlist('choice')

        if options:
            question.save()
            for option in options:
                choice = question.choices_set.create(choice_text=option)
                choice.save()

        return HttpResponseRedirect(reverse('polls:index'))
    else:
        return render(request, 'polls/create_question.html')


# Delete a question
def delete(request, question_id):
    question = Questions.objects.get(pk=question_id)
    question.delete()

    return HttpResponseRedirect(reverse('polls:index'))
