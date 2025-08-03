from django.db import models

# Create your models here.

# here for chat-list, saved by created time
class ChatSession(models.Model):
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

# for evey single message, including user msg and ai reply
class ChatMessage(models.Model):
    session = models.ForeignKey(ChatSession, related_name='messages', on_delete=models.CASCADE)
    is_user = models.BooleanField(default=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

# for prompt
class PromptPreset(models.Model):
    name = models.CharField(max_length=100)
    content = models.TextField()
