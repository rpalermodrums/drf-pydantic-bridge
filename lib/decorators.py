from pydantic import create_model
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from django.db import transaction

def pydantic_model(django_model_cls):
    def from_django(django_instance: models.Model):
        if not django_instance:
            raise ValueError("Invalid Django instance provided.")

        pydantic_model_cls = create_model(
            django_instance.__class__.__name__ + "Pydantic",
            **{field.name: field.python_type for field in django_instance._meta.fields}
        )
        return pydantic_model_cls(**{field.name: getattr(django_instance, field.name) for field in django_instance._meta.fields})

    def to_django(pydantic_instance):
        try:
            instance = django_model_cls.objects.get(id=pydantic_instance.id)
        except ObjectDoesNotExist:
            instance = django_model_cls()
        for field, value in pydantic_instance.dict().items():
            setattr(instance, field, value)
        return instance

    setattr(django_model_cls, "from_django", staticmethod(from_django))
    setattr(django_model_cls, "to_django", to_django)

    return django_model_cls

def pydantic_serializer(django_serializer_cls):
    class Meta:
        model = django_serializer_cls.Meta.model

    def to_internal_value(self, data):
        pydantic_model = create_model(
            self.Meta.model.__name__ + "Pydantic",
            **{field.name: (field.python_type) for field in self.Meta.model._meta.fields}
        )
        pydantic_instance = pydantic_model(**data)
        return pydantic_instance.to_django() # type: ignore

    def to_representation(self, obj):
        pydantic_model = create_model(
            obj.__class__.__name__ + "Pydantic",
            **{field.name: field.python_type for field in obj._meta.fields}
        )
        pydantic_instance = pydantic_model.from_django(obj) # type: ignore
        return pydantic_instance.dict()

    def create(self, validated_data):
        with transaction.atomic():
            return self.Meta.model.objects.create(**validated_data)

    setattr(django_serializer_cls, 'Meta', Meta)
    setattr(django_serializer_cls, 'to_internal_value', to_internal_value)
    setattr(django_serializer_cls, 'to_representation', to_representation)
    setattr(django_serializer_cls, 'create', create)

    return django_serializer_cls
