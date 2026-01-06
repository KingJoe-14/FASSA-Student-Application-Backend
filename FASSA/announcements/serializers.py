from rest_framework import serializers
from .models import Announcement

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ['id', 'title', 'content', 'created_by', 'created_at', 'updated_at', 'is_active']
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']
