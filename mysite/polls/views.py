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


class IndexView(generic.ListView):
    template_name = 'polls/csstest.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published question."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        :return:
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


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



"""
def stockwatch(request):
    return render(request, 'polls/csstest.html')
"""


def get_name(request):
    if request.method == 'POST':
        form = StockForm(request.POST)

        if form.is_valid():

            return HttpResponseRedirect('/thanks/')

    else:
        form = StockForm()

    print(form)

    return render(request, 'csstest.html', {})


def stock_result(request):


    pythoncom.CoInitialize()
    objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
    objCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
    objStockMst = win32com.client.Dispatch("DsCbo1.StockMstM")  # 복수 종목 검색
    objStockMst1 = win32com.client.Dispatch("DsCbo1.StockMst")  # 단일 종목 검색

    bConnect = objCpCybos.IsConnect
    if bConnect == 0:
        print("PLUS가 정상적으로 연결되지 않음. ")
        exit()
    else:
        print("PLUS가 정상적으로 연결됨. ")

    search_name = request.GET.get('stock_name', '')
    search_code = request.GET.get('stock_code', '')
    search_ic = request.GET.get('industry_code', '')

    # 기본 사이드 바 메뉴 list
    industry_list = Search.objects.values_list('industry_code', flat=True).distinct().order_by('industry_code')
    industry_name = []
    for code in industry_list:
        industry_name.append((code, objCpCodeMgr.GetIndustryName(code)))

    # 사이드바 메뉴 선택 시
    if search_ic != '':
        select_list = Search.objects.filter(industry_code=search_ic).order_by('code')
        return render(request, 'polls/csstest.html', {'select_list': select_list, 'industry_names': industry_name})

    # 종목명 / 종목코드 관련 검색
    code_string = ""
    select_list = Search.objects.all()
    s = select_list.filter(name__icontains=search_name, code__icontains=search_code)

    # 검색 종목에 대한 현재가 업데이트(110개 단위로)
    for s_obj in s:
        code_string += s_obj.code
        if len(code_string) == 110:
            objStockMst.SetInputValue(0, code_string)  # 전체 종목에 대한 코드 반환 (max = 110)
            objStockMst.BlockRequest()
            count = objStockMst.GetHeaderValue(0)
            for index in range(count):
                s_p = Search.objects.get(code=objStockMst.GetDataValue(0, index))
                s_p.cprice = objStockMst.GetDataValue(4, index)

                # print(s_p.name, s_p.cprice, s_p.industry_code)
                s_p.save()

            code_string = ""
            continue

    pythoncom.CoUninitialize()

    context = {'select_list': s, 'industry_names': industry_name}
    return render(request, 'polls/csstest.html', context)


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
    objCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
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


"""
def ReqeustUpjongMst(self):
    pythoncom.CoInitialize()
    g_objCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
    codeList = g_objCodeMgr.GetIndustryList()  # 증권 산업 업종 리스트

    allcodelist = codeList
    print("전체 종목 코드 #", len(allcodelist))

    rqCodeList = []
    for i, code in enumerate(allcodelist):
        code2 = "U" + code
        rqCodeList.append(code2)
        if len(rqCodeList) == 200:
            self.obj.Request(rqCodeList, self.dicUpjongCodes)
            rqCodeList = []
            continue

    if len(rqCodeList) > 0:
        self.obj.Request(rqCodeList, self.dicUpjongCodes)

    print("증권산업업종 리스트", len(self.dicUpjongCodes))
    for key in self.dicUpjongCodes:
        self.dicUpjongCodes[key].debugPrint(1)
"""


"""
def upjong_add(request):
    pythoncom.CoInitialize()
    objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
    bConnect = objCpCybos.IsConnect
    if (bConnect == 0):
        print("PLUS가 정상적으로 연결되지 않음. ")
        exit()
    else:
        print("PLUS가 정상적으로 연결됨. ")

    objCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
    codelist = objCpCodeMgr.GetIndustryList()

    for i, code in enumerate(codelist):
        it_name = objCpCodeMgr.GetIndustryName(code)
        if Search.objects.get(industry_code=code).exists():
            db = Search.objects.get(industry_code=code)
            db.upjong_set.create(industry_cd=code, industry_name=it_name)
            continue
        else:
            continue

    pythoncom.CoUninitialize()
    return render(request, 'polls/csstest.html')

"""

"""
def search_by_ic(request):
    industry_code = request.GET.get('industry_code', '')
    industry_list = Search.objects.values_list('industry_code', flat=True).distinct().order_by('industry_code')
    industry_name = []

    pythoncom.CoInitialize()
    objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
    objCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
    bConnect = objCpCybos.IsConnect
    if (bConnect == 0):
        print("PLUS가 정상적으로 연결되지 않음. ")
        exit()
    else:
        print("PLUS가 정상적으로 연결됨. ")

    for code in industry_list:
        industry_name.append(objCpCodeMgr.GetIndustryName(code))
    pythoncom.CoUninitialize()

    return render(request, 'polls/csstest.html', {'industry_names': industry_name})
"""














