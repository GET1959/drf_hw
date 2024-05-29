from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from users.models import User, Payment, Subscription


class UserSerializer(serializers.ModelSerializer):
    payment_list = SerializerMethodField()

    def get_payment_list(self, obj):
        return [payment.__str__() for payment in Payment.objects.filter(user=obj)]

    class Meta:
        model = User
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"
