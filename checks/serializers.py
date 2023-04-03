from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class CheckSerializer(serializers.Serializer):
    point_id = serializers.IntegerField(required=True)
    order = serializers.JSONField(required=True)
    type = serializers.CharField(max_length=50, required=True)

    def validate_type(self, type):
        if type not in ("Kitchen", "Client"):
            raise ValidationError("The only possible options for the 'type' are Kitchen and Client.")
