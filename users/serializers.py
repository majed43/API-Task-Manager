from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "password",
            "birth_date",
            "date_joined",
            "updated_at",
            "last_login",
        )

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = User(**validated_data)
        if password is not None:
            user.set_password(password)
        user.save()
        return user


class UserUpdateProfile(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    birth_date = serializers.DateField(required=False)

    class Meta:
        model = User
        fields = ("username", "email", "birth_date")

    def validate_username(self, value):
        if User.objects.filter(username=value).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError("Email already exists.")
        return value


class EmailAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if email and password:
            user = User.objects.filter(email=email).first()
            if user is None or not user.check_password(password):
                raise serializers.ValidationError("Invalid email or password.")
            data["user"] = user
        else:
            raise serializers.ValidationError("Must include 'email' and 'password'.")

        return data


class UserUpdatePassword(serializers.Serializer):
    current_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    def validate_current_password(self, value):
        user = self.instance
        if not user.check_password(value):
            raise serializers.ValidationError("Current password is incorrect.")
        return value

    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError(
                "new password must be at least 8 characters"
            )
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data["new_password"])
        instance.save()
        return instance
