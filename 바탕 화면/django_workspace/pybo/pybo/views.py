from django.utils import timezone
from django.views import generic
from django.shortcuts import render, get_object_or_404, redirect
from pybo.models import Question, Answer
from pybo.forms import QuestionForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# from django.shortcuts import render, get_object_or_404


# pybo 목록 출력
# def index(request):
#     object_list = Question.objects.order_by('-create_date')
#     context = {'object_list': object_list}
#     return render(request, 'pybo/question_list.html', context)
#
# #pybo 상세보기
# def detail(request, question_id):
#     # question = Question.objects.get(id=question_id)
#     question = get_object_or_404(Question, pk=question_id)
#     context = {'object' : question}
#     return render(request, 'pybo/question_detail.html', context)

class IndexView(generic.ListView):
    paginate_by = 10   # context = {'page_obj':page_obj}
    def get_queryset(self):
        return Question.objects.order_by('-create_date')


class DetailView(generic.DetailView):
    model = Question

@login_required(login_url='common:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다')  #오류 발생 메세지를 띄우기 위해 message 모듈 이용
        return redirect('pybo:detail', question_id=question.id)

    if request.method == "POST":   #질문 수정 화면에서 <저장하기>누르면 post 방식으로 호출되어 데이터 수정이 이뤄짐.
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date = timezone.now()  # 수정일시 저장
            question.save()
            return redirect('pybo:detail', question_id=question.id)
    else:   #질문 상세 화면에서 <수정>을 누른 경우, get방식으로 호출되어 질문 수정 화면 나타남
        form = QuestionForm(instance=question)  #질문 수정화면이 나타날ㄸ때 기존에 저장데이터가 나타나도록 instance 매개변수에 question 지정
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)

@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    question.delete()
    return redirect('pybo:index')

@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        answer.delete()
    return redirect('pybo:detail', question_id=answer.question.id)

@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=answer.question.id)

    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('pybo:detail', question_id=answer.question.id)
    else:
        form = AnswerForm(instance=answer)
    context = {'answer': answer, 'form': form}
    return render(request, 'pybo/answer_form.html', context)

# question_id로 들어온 Answer 객체 save
@login_required(login_url='common:login')
def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now(), author=request.user)
    # answer = Answer(question=question1, content=request.POST.get('content'), create_date=timezone.now())
    # answer.save()
    return redirect('pybo:detail', pk=question.id)  # detail url에서 pk로 넘겼기 때문에


# question 등록 : get 일경우 입력화면만 제공하고 // post 일 경우 form(subject, content)데이터 model 저장
@login_required(login_url='common:login')
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)  #subject = request.POST['subject']  content=request.POST['content']
        if form.is_valid():
            question = form.save(commit=False)   #question = Question(subject=subject, content= content, create_date= timezone.now())으로 객체를 생성해주고
            # 아직 commit은하지말고, 아래에  create_date 추가해야 해서
            question.create_date = timezone.now()     #subject, content는 이미 form에 있으므로 날짜만 추가
            question.author = request.user
            question.save()                       #이때는 commit= True
            return redirect('pybo:index')
    else:
        form = QuestionForm()
        context = {'form': form}
    return render(request, 'pybo/question_form.html', context)

# form = QuestionForm()
# return render(request, 'pybo/question_form.html', {'form': form})
