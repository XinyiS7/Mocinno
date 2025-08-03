from django.shortcuts import render
from .models import PromptPreset

def chat_page(request):
    presets = PromptPreset.objects.all()
    return render(request, 'chat/main_chat.html', {'presets': presets})
