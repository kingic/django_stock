from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
import win32com.client
import pythoncom
from .forms import StockForm
from .models import Search


from .models import Choice, Question
# Create your views here.


# 장고 예제
class IndexView(generic.ListView):
    template_name = 'polls/csstest.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published question."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


# 장고 예제
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        :return:
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


# 장고 예제
class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back Button
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


# 초기화면
def stockwatch(request):
    pythoncom.CoInitialize()
    objCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
    # 기본 사이드 바 메뉴 list
    industry_list = Search.objects.values_list('industry_code', flat=True).distinct().order_by('industry_code')
    industry_name = []

    for code in industry_list:
        industry_name.append((code, objCpCodeMgr.GetIndustryName(code)))
    pythoncom.CoUninitialize()
    return render(request, 'polls/csstest.html', {'industry_names': industry_name})


# retrieve
def stock_result(request):
    pythoncom.CoInitialize()
    objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")      # 연결
    objCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")  # 종목 리스트
    objStockMst = win32com.client.Dispatch("DsCbo1.StockMstM")   # 복수 종목 검색
    objStockMst1 = win32com.client.Dispatch("DsCbo1.StockMst")   # 단일 종목 검색

    bConnect = objCpCybos.IsConnect
    if bConnect == 0:
        print("PLUS가 정상적으로 연결되지 않음. ")
        exit()
    else:
        print("PLUS가 정상적으로 연결됨. ")

    # get user request
    search_name = request.GET.get('stock_name', '')
    search_code = request.GET.get('stock_code', '')
    search_ic = request.GET.get('industry_code', '')

    # 기본 사이드 바 메뉴 list
    industry_list = Search.objects.values_list('industry_code', flat=True).distinct().order_by('industry_code')
    industry_name = []
    for code in industry_list:
        industry_name.append((code, objCpCodeMgr.GetIndustryName(code)))

    # 종목명 / 종목코드 관련 검색
    code_string = ""
    select_list = Search.objects.all()
    s = select_list.filter(name__icontains=search_name, code__icontains=search_code, industry_code__icontains=search_ic)
    print("through....s:", s.count())

    # 검색 종목에 대한 DB 업데이트(110개 단위로)
    for s_obj in s:
        code_string += s_obj.code
        if len(code_string) == 770:                     # (전체 종목: 110개) * (종목 당 character: 7글자)
            objStockMst.SetInputValue(0, code_string)   # 전체 종목에 대한 코드 반환 (max = 110)
            objStockMst.BlockRequest()
            count = objStockMst.GetHeaderValue(0)
            for index in range(count):
                get_code = objStockMst.GetDataValue(0, index)       # 종목 List 에서 순차적으로 종목코드 탐색
                s_p = Search.objects.get(code=get_code)             # 해당 종목코드로 search (DB 탐색)
                s_p.cprice = objStockMst.GetDataValue(4, index)     # 해당 종목 현재가 Instance 업데이트
                s_p.diff = objStockMst.GetDataValue(2, index)       # 해당 종목 전일대비 Instance 업데이트
                # 반영 하는지 test
                print("1",s_p.name, s_p.cprice, s_p.industry_code, s_p.diff)
                s_p.save()                                          # 변경 사항 DB에 저장
            code_string = ""
            continue

    # 전체종목 % 110개 만큼의 종목들에 대한 DB 업데이트
    if len(code_string) > 0:
        objStockMst.SetInputValue(0, code_string)
        objStockMst.BlockRequest()
        count = objStockMst.GetHeaderValue(0)
        for index in range(count):
            get_code = objStockMst.GetDataValue(0,index)
            s_p = Search.objects.get(code=get_code)
            s_p.cprice = objStockMst.GetDataValue(4, index)
            s_p.diff = objStockMst.GetDataValue(2, index)
            # 반영 하는지 test
            print("2",s_p.name, s_p.cprice, s_p.industry_code, s_p.diff)
            s_p.save()

    pythoncom.CoUninitialize()

    context = {'select_list': s, 'industry_names': industry_name}
    return render(request, 'polls/csstest.html', context)
# git test

# db 내용 추가(초기에 1회만 실행해주면 됨) / url:polls/stock_add
def db_add(request):

    # 연결 여부 체크
    pythoncom.CoInitialize()
    objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
    bConnect = objCpCybos.IsConnect
    if (bConnect == 0):
        print("PLUS가 정상적으로 연결되지 않음. ")
        exit()

    # 종목코드 리스트 구하기
    objStockMst = win32com.client.Dispatch("DsCbo1.StockMst")
    objCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
    codeList = objCpCodeMgr.GetStockListByMarket(1)  # 거래소
    # codeList2 = objCpCodeMgr.GetStockListByMarket(2)  # 코스닥

    #print("거래소 종목코드", len(codeList))
    for i, code in enumerate(codeList):
        name = objCpCodeMgr.CodeToName(code)
        stdPrice = objCpCodeMgr.GetStockStdPrice(code)
        industry = objCpCodeMgr.GetStockIndustryCode(code)
        db = Search.objects.get(name=name, code=code)
        db.industry_code = industry
        db.industry_name = objCpCodeMgr.GetIndustryName(industry)
        db.save()

    pythoncom.CoUninitialize()
    return render(request, 'polls/csstest.html')

