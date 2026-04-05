from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import ChatSession, ChatMessage
from .serializers import ChatQuerySerializer
from .services.gemini_service import get_gemini_response

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

@method_decorator(csrf_exempt, name='dispatch')
class ChatQueryView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = ChatQuerySerializer(data=request.data)
        if serializer.is_valid():
            session_id = serializer.validated_data['session_id']
            message_text = serializer.validated_data['message']

            # Get or create session
            session, created = ChatSession.objects.get_or_create(session_id=session_id)
            
            # Attach user if logged in
            if request.user.is_authenticated and session.user is None:
                session.user = request.user
                session.save()

            # Save User Message
            ChatMessage.objects.create(session=session, sender='USER', message=message_text)

            # Get Gemini Response
            bot_reply = get_gemini_response(session, message_text)

            # Save Bot Message
            ChatMessage.objects.create(session=session, sender='BOT', message=bot_reply)

            return Response({"response": bot_reply}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
