from rest_framework import serializers


class CheckSerializer(serializers.Serializer):
    point_id = serializers.IntegerField(required=True)
    order = serializers.JSONField(required=True)
    type = serializers.CharField(max_length=50, required=True)
