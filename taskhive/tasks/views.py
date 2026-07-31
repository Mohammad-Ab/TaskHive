from rest_framework import viewsets
from .models import Task
from .serializers import TaskSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .permissions import IsTaskOwnerOrCreator
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.

class TaskViewSet(viewsets.ModelViewSet):
    #queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated,IsTaskOwnerOrCreator]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,]

    filterset_fields = ["status","priority","project","assignee",]
    search_fields = ["title","description",]
    ordering_fields = ["-created_at","deadline","priority"]

    def get_queryset(self):
        user = self.request.user

        return Task.objects.filter(
            Q(project__owner = user) | Q(project__members = user)
        ).distinct()

    def perform_create(self,serializer):
        serializer.save(created_by = self.request.user)
