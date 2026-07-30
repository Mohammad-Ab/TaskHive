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

        project = attrs.get(
                "project",
                self.instance.project if self.instance else None
        )
        assignee = attrs.get(
                "assignee",
                self.instance.assignee if self.instance else None
        )

        title = attrs.get(
            "title",
            self.instance.title if self.instance else None
        )

        if assignee is not None:
            if(
                assignee != project.owner
                and not project.members.filter(id=assignee.id).exists()
                ):
                raise serializers.ValidationError({
                    "assignee":
                    "selected user must be the project owner or one of the project members."
                })

        queryset = Task.objects.filter(
            project = project,
            title = title,
        )

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError({
                "title":
                "a task with this title already exists in this project."
            })

        return attrs

    #validation for deadline time
    def validate_deadline(self,value):
        
        if value is None:
            return value

        if value < timezone.now():
            raise serializers.ValidationError("DeadLine can not be in the past.")

        return value





