# chat/views.py
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Message
from .serializers import MessageSerializer
from rest_framework.decorators import api_view
import logging
logger = logging.getLogger(__name__)

# ViewSet for handling Message CRUD operations
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def perform_create(self, serializer):
        # Here we could add additional logic, e.g., checking for message content or other processing
        serializer.save(user=self.request.user)

# API View for sending a message
@api_view(['POST'])
def send_message(request, topic_id):
    if request.method == 'POST':
        # topic = Topic.objects.get(id=topic_id)
        content = request.data.get('content')
        message = Message.objects.create(user=request.user, content=content)
        return Response({'message': 'Message sent successfully!', 'message_id': message.id})
from rest_framework import status

@api_view(['GET', 'POST'])
def test(request):
    if request.method == 'GET':
        logger.info(f"Message created successfully: {'21312321'}")
        return Response({'message': 'Test Message sent successfully!'})
    
    if request.method == 'POST':
        # Assuming you're sending a topic_id and content in the request body
        content = request.data.get('content')

        # Create the message
        message = Message.objects.create(user=request.user, content=content)
        
        logger.info(f"Message created successfully: {message.id}")

        return Response({'message': 'Message created successfully!', 'message_id': message.id}, status=status.HTTP_201_CREATED)
from django.shortcuts import render

def index(request, room_name):
    logger.info(f"User joined room: {room_name}")
    return render(request, 'chat/index.html', {'room_name': room_name})