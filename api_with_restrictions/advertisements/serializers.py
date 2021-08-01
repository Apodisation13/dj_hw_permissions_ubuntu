from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from advertisements.models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator', 'status', 'created_at', )

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        creator = self.context["request"].user.id
        # print(creator)
        total_open = Advertisement.objects.filter(creator__id=creator, status='OPEN').count()
        # print(total_open)
        if total_open > 10:
            raise ValidationError({'detail': 'Можно иметь не более десяти открытых объявлений'})
        return data

    # def validate_title(self, value):
    #     """проверить поле title - например на 5 символов, ОБЯЗАТЕЛЬНО РЕТЁРН"""
    #     if len(value) > 5:
    #         raise ValidationError('Нельзя больше 5 символов')
    #     return value

    def validate_description(self, value):
        """проверить поле description - например что нельзя мат, ОБЯЗАТЕЛЬНО РЕТЁРН"""
        if 'ХРЕН' in value:
            raise ValidationError('Нельзя мат')
        return value
