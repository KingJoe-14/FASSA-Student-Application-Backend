from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from accounts.permissions import IsAdmin, IsSuperAdmin
from clubs.models import Club, ClubMembership, ClubEvent
from clubs.serializers import ClubSerializer, ClubMembershipSerializer, ClubEventSerializer


# -------------------------------
# CLUB CRUD (Admins & Superadmins)
# -------------------------------
class AdminClubListCreateView(generics.ListCreateAPIView):
    """List all clubs or create a new club (Admin/Superadmin)"""
    serializer_class = ClubSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsSuperAdmin]
    queryset = Club.objects.all().order_by('-created_at')


class AdminClubRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a club"""
    serializer_class = ClubSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsSuperAdmin]
    queryset = Club.objects.all()


# -------------------------------
# CLUB MEMBERSHIPS (Assign Leaders/Executives)
# -------------------------------
class AdminClubMemberListCreateView(generics.ListCreateAPIView):
    """List members of a club or add a new member (Admin/Superadmin)"""
    serializer_class = ClubMembershipSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsSuperAdmin]

    def get_queryset(self):
        club_id = self.kwargs.get('club_id')
        return ClubMembership.objects.filter(club_id=club_id)

    def get_serializer_context(self):
        """Pass the club instance to the serializer"""
        context = super().get_serializer_context()
        club_id = self.kwargs.get('club_id')
        context['club'] = generics.get_object_or_404(Club, id=club_id)
        return context

    def perform_create(self, serializer):
        student = serializer.validated_data['student_id']
        club = self.get_serializer_context()['club']

        # Prevent adding the same student twice
        if ClubMembership.objects.filter(club=club, student=student).exists():
            raise ValidationError("Student is already a member of this club.")

        serializer.save()  # Serializer handles student + club assignment


class AdminClubMemberRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update (role), or remove a member from a club"""
    serializer_class = ClubMembershipSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsSuperAdmin]
    queryset = ClubMembership.objects.all()


# -------------------------------
# CLUB EVENTS (Approve/Manage)
# -------------------------------
class AdminClubEventListCreateView(generics.ListCreateAPIView):
    """List events for all clubs or create a new event"""
    serializer_class = ClubEventSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsSuperAdmin]
    queryset = ClubEvent.objects.all().order_by('-event_date')

    def perform_create(self, serializer):
        # Automatically assign the admin who created the event
        serializer.save(created_by=self.request.user)


class AdminClubEventRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update (approve/reject), or delete a club event"""
    serializer_class = ClubEventSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsSuperAdmin]
    queryset = ClubEvent.objects.all()
