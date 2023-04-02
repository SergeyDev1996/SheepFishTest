from rest_framework import serializers

from checks.models import Check


class CheckCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Check
        fields = "__all__"
