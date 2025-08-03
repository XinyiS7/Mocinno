from django.shortcuts import render
from .models import PromptPreset
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import PromptPreset

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