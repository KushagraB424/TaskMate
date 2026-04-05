from rest_framework import serializers

class ChatQuerySerializer(serializers.Serializer):
    session_id = serializers.CharField(max_length=255)
    message = serializers.CharField()
