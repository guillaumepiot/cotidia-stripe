from rest_framework import serializers


class SubscriptionCreateSerializer(serializers.Serializer):
    plan_id = serializers.CharField()
    card_number = serializers.CharField()
    card_exp_month = serializers.IntegerField()
    card_exp_year = serializers.IntegerField()
    card_cvc = serializers.CharField()


class SubscriptionUpdateSerializer(serializers.Serializer):
    plan_id = serializers.CharField()
