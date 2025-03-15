# chat/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MessageViewSet, send_message, index, test

# Initialize router
router = DefaultRouter()
router.register(r'messages', MessageViewSet)

urlpatterns = [
    path('messages/', include(router.urls)),  # Automatically generate routes for Message model
    path('send_message/<int:topic_id>/', send_message, name='send_message'),
    path('<str:room_name>/', index, name='chat_room'),
    path('x/test/', test, name='test'),

]
