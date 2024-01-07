# telegrambot/urls.py

from django.urls import path
from .views import setwebhook, telegram_bot 

urlpatterns = [
  path('setwebhook/', setwebhook, name='setwebhook'),
  path('getpost/', telegram_bot, name='telegram_bot'),
]