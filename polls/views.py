from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render_to_response("index.html")
    # return HttpResponse("Hello, world. You're at the polls index.")

# this is all answers for all questions, should be stored in the Database.
question_answer_map = {
    "question1": {"type": "single", "answer": "A"},
    "question2": {"type": "multiple", "answer": "AB"}
}

# this is the verify function can be used for all kinds of questions
@csrf_exempt
def verifyUserAnswer(request):
    data = {}
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        answer_str = request.POST.get('answer')
        verify_result = verifyAnswer(question_id, answer_str)
        message = "Your answer is correct." if verify_result else "Your answer is incorrect."
        data = {
            "question_id": question_id,
            'message': message,
            "verify_result": verify_result
        }
    return JsonResponse(data)

# this is the commom function for verifing all kinds of questions.
def verifyAnswer(question_id, answer):
    result = False;
    question_type = question_answer_map.get(question_id).get("type")
    correct_answer = question_answer_map.get(question_id).get("answer")
    answer = answer.upper()
    # single choice question process
    if question_type == "single" :
        if correct_answer == answer:
            result = True
        else:
            result = False
    # multiple choice question process
    elif question_type == "multiple" :
        answer_list = sorted(answer)
        sorted_user_answer = ''.join(answer_list)
        if correct_answer == sorted_user_answer:
            result = True
        else: 
            result = False

    return result