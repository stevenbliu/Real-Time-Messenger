# chat/routing.py
from django.urls import re_path
from chat import consumers
from django.urls import path

websocket_urlpatterns = [
    path('ws/chat/<str:room_name>/', consumers.ChatConsumer.as_asgi()),
    path('ws/chat/1/', consumers.ChatConsumer.as_asgi()),

]

