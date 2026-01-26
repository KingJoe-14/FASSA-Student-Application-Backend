from rest_framework import generics, permissions
from .models import Announcement
from .serializers import AnnouncementSerializer
from accounts.permissions import IsAdmin, IsSuperAdmin  # reuse your permissions

class AnnouncementListView(generics.ListAPIView):
    serializer_class = AnnouncementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Announcement.objects.filter(is_active=True)

class AnnouncementCreateView(generics.CreateAPIView):
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAdmin | IsSuperAdmin]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class AnnouncementDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAdmin | IsSuperAdmin]
    queryset = Announcement.objects.all()
