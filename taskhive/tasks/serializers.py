from rest_framework import serializers
from .models import Task
from django.utils import timezone

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

    def validate(self, attrs):
        project = attrs.get("project")
        assignee = attrs.get("assignee")

        if assignee is None:
            return attrs

        if assignee == project.owner:
            return attrs
        if project.members.filter(id=assignee.id).exists():
            return attrs

        raise serializers.ValidationError({
            "assignee":"selected user must be the project owner or one of the project members."
        })

    def validate_deadline(self,value):
        
        if value is None:
            return value

        if value < timezone.now():
            raise serializers.ValidationError("DeadLine can not be in the past.")

        return value





