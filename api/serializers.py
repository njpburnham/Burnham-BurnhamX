from django.contrib.auth.models import User, Group
from rest_framework import serializers
from django.forms import widgets
from extension.models import Customer

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Customer
        fields = ('url', 'name')


# class CustomerSerializer(serializers.Serializer):
#   pk = serializers.IntegerField(read_only=True)
#   name = serializers.CharField(max_length=100)


#   def create(self, validated_data):
#     """
#     Create and return a new `Customer` instance
#     """
#     return Customer.objects.create(**validated_data)

#   def update(self, instance, validated_data):
#     """
#     Update and return an existing `Customer` instance
#     """
#     instance.name = validated_data.get('name', instance.name)
#     instance.save()
#     return instance