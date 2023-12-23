import pytest
from django_pydantic_bridge.decorators import pydantic_model, pydantic_serializer
from django.db import models
from rest_framework import serializers
from django.test import TestCase

# Mocking the Address model and its serializer
@pydantic_model
class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2)
    zip = models.CharField(max_length=10)

@pydantic_serializer
class AddressSerializer(serializers.Serializer):
    class Meta:
        model = Address
        fields = '__all__'

class TestDecorators(TestCase):
    def test_pydantic_model_decorator(self):
        django_instance = Address(street="123 Main St", city="Springfield", state="IL", zip="62704")
        pydantic_instance = Address.from_django(django_instance) # type: ignore
        assert pydantic_instance.dict() == {
            "street": "123 Main St",
            "city": "Springfield",
            "state": "IL",
            "zip": "62704"
        }

        returned_django_instance = pydantic_instance.to_django() # type: ignore
        assert returned_django_instance.street == django_instance.street
        assert returned_django_instance.city == django_instance.city

    def test_pydantic_serializer_decorator(self):
        data = {
            "street": "123 Main St",
            "city": "Springfield",
            "state": "IL",
            "zip": "62704"
        }
        serializer = AddressSerializer(data=data)
        assert serializer.is_valid()

        internal_value = serializer.to_internal_value(data)
        assert internal_value.street == "123 Main St"
        assert internal_value.city == "Springfield"

        representation = serializer.to_representation(internal_value)
        assert representation == data