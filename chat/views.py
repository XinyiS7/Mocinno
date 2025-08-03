from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest, JsonResponse
from dotenv import load_dotenv
from .models import PromptPreset, ChatMessage, ChatSession
from .chatlogic import send_to_api  # 你提供的函数
import uuid
import os

def chat_page(request):
    presets = PromptPreset.objects.all()
    return render(request, 'chat/main_chat.html', {'presets': presets})

@csrf_exempt
def save_prompt(request):
    if request.method == 'POST':
        name = request.POST.get('prompt_option')
        content = request.POST.get('custom_prompt')

        preset = PromptPreset.objects.filter(name=name).first()
        if preset:
            preset.content = content
            preset.save()
        return JsonResponse({'status': 'ok'})

@csrf_exempt
def submit_chat(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Only POST supported")

    user_input = request.POST.get("user_input", "").strip()
    model = request.POST.get("model", "chat")
    abstract = request.POST.get("abstract") == "on"
    session_key = request.POST.get("session_key")
    load_dotenv()
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print("⚠️ 错误：找不到环境变量 DEEPSEEK_API_KEY！请先设置它。")
        exit(1)  # 或从 settings/env 中获取

    # 会话处理
    if not session_key:
        session = ChatSession.objects.create(title="新会话")
        session_key = str(session.id)
    else:
        session = ChatSession.objects.get(id=session_key)

    # 存储用户消息
    ChatMessage.objects.create(session=session, is_user=True, content=user_input)

    # 调用 AI 接口
    thinking, answer = send_to_api(mode=model, abstract=abstract, session_key=session_key, api_key=api_key)

    # 存储 AI 回复
    ChatMessage.objects.create(session=session, is_user=False, content=answer)

    # 渲染所有消息
    messages = ChatMessage.objects.filter(session=session).order_by("timestamp")
    return render(request, "chat/chat_window.html", {"messages":
                                                               messages})