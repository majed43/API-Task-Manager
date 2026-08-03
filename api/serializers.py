from django.conf import settings
from django.core.validators import RegexValidator
from django.utils import timezone
from rest_framework import serializers

from .models import Category, Project, Task

hex_color_validator = RegexValidator(
    regex=r"^#(?:[0-9a-fA-F]{3}){1,2}$",
    message="Enter a valid hex color code, e.g. #ff0000 or #f00",
)
User = settings.AUTH_USER_MODEL


class CategorySerializer(serializers.ModelSerializer):
    hex_color = serializers.CharField(validators=[hex_color_validator])

    class Meta:
        model = Category
        fields = (
            "id",
            "title",
            "description",
            "hex_color",
            "owner",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("owner",)

    def validate_title(self, value):
        request = self.context.get("request")
        qs = Category.objects.filter(owner=request.user, title=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                "A category with this title already exists for this user."
            )
        return value


class ProjectSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.none())

    class Meta:
        model = Project
        fields = (
            "id",
            "title",
            "category",
            "owner",
            "participants",
            "created_at",
            "updated_at",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if request:
            self.fields["category"].queryset = Category.objects.filter(
                owner=request.user
            )
            if request.method in ("PUT", "PATCH"):
                self.fields["category"].read_only = True
                self.fields["category"].required = False

    def validate_participants(self, value):
        request = self.context.get("request")
        if request and request.method in ("PUT", "PATCH") and request.user not in value:
            raise serializers.ValidationError(
                "The owner must be included in the participants list."
            )
        return value

    def validate_title(self, value):
        request = self.context.get("request")
        qs = Project.objects.filter(owner=request.user, title=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                "A project with this title already exists for this user."
            )
        return value


class TaskSerializer(serializers.ModelSerializer):

    hex_color = serializers.CharField(
        validators=[hex_color_validator],
        required=False,
        allow_null=True,
        allow_blank=True,
    )

    class Meta:
        model = Task

        fields = (
            "id",
            "title",
            "description",
            "status",
            "importance_level",
            "hex_color",
            "project",
            "assigned_to",
            "due_date",
            "created_at",
            "updated_at",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            self.fields["project"].queryset = request.user.owned_projects.all()
            if request.method in ("PUT", "PATCH"):
                self.fields["project"].read_only = True
                self.fields["project"].required = False
        else:
            serializers.ValidationError(
                "User must be authenticated to create or update a task."
            )

    def validate_due_date(self, value):
        if value and value < timezone.now().date():
            raise serializers.ValidationError("Due date cannot be in the past")
        return value

    def validate(self, data):
        project = data.get("project") or getattr(self.instance, "project", None)
        assigned_to = data.get("assigned_to") or getattr(
            self.instance, "assigned_to", None
        )

        if (
            project
            and assigned_to
            and not project.participants.filter(pk=assigned_to.pk).exists()
        ):
            raise serializers.ValidationError(
                "Assigned user does not belong to the project participants"
            )
        return data
