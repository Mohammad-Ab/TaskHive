from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'status',
            'priority',
            'deadline',
            'project',
            'assignee',
            'created_by',
            'created_at',
        ]
        read_only_fields = ['id', 'created_by', 'created_at']









