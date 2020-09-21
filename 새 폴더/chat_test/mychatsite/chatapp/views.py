from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import loader

# 홈페이지 대화 말뭉치 텐서플로우 딥러닝 학습모델 챗봇 연결
from chatapp.ArkChatFramework.ArkChat.chatting_home import ChattingHomepage
# 챗봇 프레임워크에서 로깅
import os
import logging

# Create your views here.
context = {}

# 챗봇 초기화
logger = logging.getLogger(__name__)
work_dir = os.path.dirname(os.path.realpath(__file__))
bot = ChattingHomepage(work_dir)

# def index(request):
#     msg = '박형식 홈페이지'
#     return render(request, 'chatapp/index.html', {'message': msg})

def index(request):
    template = loader.get_template('chatapp/base_contents_kr.html')
    # template = loader.get_template('chatapp/base_mycareer_kr.html')
    context = {
#         'login_success' : False,
#         'latest_question_list': "test",
    }
    return HttpResponse(template.render(context, request))

def chat_home(request):
    template = loader.get_template('chatapp/chat_home_screen.html')
    context = {
        'login_success' : False,
        'initMessages' : ["화장품 제품을 추천해드릴게요!!", # 수정
                          "원하는 제품 카테고리를 선택해주세요. (스킨/토너, 로션, 에센스/세럼, 앰플, 크림)"]
    }
    return HttpResponse(template.render(context, request))

def popup_chat_home(request):
    # template = loader.get_template('chatapp/popup_chat_home_screen.html')
    template = loader.get_template('chatapp/popup_mycareer_chatting_screen.html')
    context = {
        'login_success' : False,
        'initMessages' : ["화장품 제품을 추천해드릴게요!!", # 수정
                          "원하는 제품 카테고리를 선택해주세요. (스킨/토너, 로션, 에센스/세럼, 앰플, 크림)"]
    }
    # context = {
    #     'login_success' : False,
    #     'initMessages' : ["인공지능 기반 업무자동화 RPA 컨설턴트 직무를 찾고 있는 홍길동입니다.",
    #                       "귀사를 위한 업무자동화 서비스 제공자로서 준비된 저의 역량을 소개해 드리겠습니다."]
    # }
    return HttpResponse(template.render(context, request))

def call_chatbot(request): # 수정
    if request.method == 'POST':
        if request.is_ajax():
            userID = request.POST['user']
            sentence = request.POST['message']
            step = request.POST['step'] # 질문 순서
            query = request.POST['query'] # 답변 리스트
            # # function
            # stepChk, tag = step_resp(step, tag)
            logger.debug("question[{}]".format(sentence))
            try:
                answer, tag = bot.get_answer(sentence, userID)
                stepChk, res_tag, query_list = step_resp(step, tag, query) # ??
                if res_tag == "순서에러":
                    answer = "질문에 맞지 않는 대답입니다. 다시 선택해주세요."
                    return JsonResponse({
                                'answer' : answer,
                                'stepChk' : stepChk,
                                'query': query_list
                            }, json_dumps_params = {'ensure_ascii': True})
                else:
                    answer = bot.get_answer(sentence, userID)
                    return JsonResponse({
                                'answer' : answer,
                                'stepChk' : stepChk,
                                'query': query_list
                            }, json_dumps_params = {'ensure_ascii': True})
            except:
                answer = bot.get_answer(sentence, userID)
                return HttpResponse(answer)
            # answer = sentence
            logger.debug("answer[{}]".format(answer))
    return ''

# 추가
def step_resp(step, tag, query_list):
    cate_list = ['스킨/토너', '로션', '에센스/세럼', '앰플', '크림'] # category list
    filter_list = ["복합성","건성","지성","쿨톤","웜톤","잡티","미백","주름","각질","트러블","블랙헤드","피지과다","민감성","모공","탄력","홍조","아토피"] # 17개 태그 리스트
    type_list = filter_list[:3] # 피부 타입 리스트
    tone_list = filter_list[3:5] # 피부 톤 리스트
    porb_list = filter_list[5:] # 피부 고민 리스트

    if step == 1: # 제품 카테고리 선택 단계
        if tag in cate_list:
            stepChk = True
            result = tag
            query_list.append(tag)
        else:
            stepChk = False
            result = "순서에러"
            # "잘못 입력하셨습니다." 출력

    if step == 2: # 피부 타입 선택 단계
        if tag in type_list:
            stepChk = True
            result = tag
            query_list.append(tag)
        else:
            stepChk = False
            result = "순서에러"
            # "잘못 입력하셨습니다." 출력

    if step == 3: # 피부 톤 선택 단계
        if tag in tone_list:
            stepChk = True
            result = tag
            query_list.append(tag)
        else:
            stepChk = False
            result = "순서에러"
            # "잘못 입력하셨습니다." 출력

    if step == 4: # 피부 고민 선택 단계
        if tag in porb_list:
            stepChk = True
            result = tag
            query_list.append(tag)
        else:
            stepChk = False
            result = "순서에러"
            # "잘못 입력하셨습니다." 출력

    if step == 5: # 제품 추천
        stepChk = True
        # recommend = 추천 결과 함수(결과list)
        result = "추천상품!" # + recommend
        query_list = []

    return stepChk, result, query_list