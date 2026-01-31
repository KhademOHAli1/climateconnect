from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from climateconnect_api.pagination import NotificationsPagination
from climateconnect_api.serializers.notification import NotificationSerializer
from climateconnect_api.models.notification import UserNotification, Notification
from rest_framework.exceptions import ValidationError
from datetime import datetime
from rest_framework.response import Response
from rest_framework import status


class ListNotificationsView(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = NotificationsPagination
    serializer_class = NotificationSerializer

    def get_queryset(self):
        user_notifications = UserNotification.objects.filter(
            user=self.request.user, read_at=None
        ).values_list("notification", flat=True)
        
        if not user_notifications:
            return Notification.objects.none()
        
        # Optimize with select_related for FK relations used in serialization
        notifications = (
            Notification.objects.filter(id__in=user_notifications)
            .select_related(
                "chat",
                "project_comment",
                "post_comment",
                "idea_comment",
            )
            .order_by("-created_at")
        )
        return notifications


class SetUserNotificationsRead(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if "notifications" not in request.data:
            raise ValidationError("Required parameter mission: notifications")
        
        # Bulk update instead of loop with individual saves
        UserNotification.objects.filter(
            notification__in=request.data["notifications"],
            user=request.user,
            read_at=None,
        ).update(read_at=datetime.now())
        
        # Get remaining unread notifications with optimized query
        all_unread_user_notifications = UserNotification.objects.filter(
            user=request.user, read_at=None
        ).values_list("notification", flat=True)
        
        if not all_unread_user_notifications:
            return Response([], status=status.HTTP_200_OK)
        
        notifications = (
            Notification.objects.filter(id__in=all_unread_user_notifications)
            .select_related(
                "chat",
                "project_comment",
                "post_comment",
                "idea_comment",
            )
            .order_by("-created_at")
        )
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
