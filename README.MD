
# DrfPydanticBridge

DrfPydanticBridge is a Python package that facilitates the integration of Pydantic models with Django models and Django REST Framework (DRF) serializers. This package provides decorators that allow seamless conversion between Django models and Pydantic models, enabling robust data validation using Pydantic while leveraging Django's ORM and DRF's powerful features.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
    - [Defining Django Models](#defining-django-models)
    - [Creating DRF Serializers](#creating-drf-serializers)
    - [Views and URLs](#views-and-urls)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)
- [Changelog](#changelog)

## Features
- Convert Django models to Pydantic models and vice versa using a simple decorator.
- Convert DRF serializers to use Pydantic models for data validation with a decorator.
- Seamless integration with your existing Django and DRF projects.

## Installation
```bash
pip install drf-pydantic-bridge
```

## Usage

### Defining Django Models
```python
# models.py
from django.db import models
from drf_pydantic_bridge.decorators import pydantic_model

@pydantic_model
class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    # ... rest of your fields ...

# ... rest of your models ...
```

### Creating DRF Serializers
```python
# serializers.py
from rest_framework import serializers
from drf_pydantic_bridge.decorators import pydantic_serializer
from .models import Address

@pydantic_serializer
class AddressSerializer(serializers.Serializer):
    class Meta:
        model = Address
        fields = '__all__'

# ... rest of your serializers ...
```

### Views and URLs
```python
# views.py
# ... your views using the DjangoPydanticBridge serializers ...

# urls.py
# ... your URL configurations ...
```

## Testing
The `tests` directory contains a comprehensive test suite to validate the functionality provided by DjangoPydanticBridge.

```bash
python manage.py test drf_pydantic_bridge
```

## Contributing
We welcome contributions to DjangoPydanticBridge! Please see our contributing guidelines for more details.

## License
DjangoPydanticBridge is distributed under the MIT License. See `LICENSE` for more details.

## Contact
For any inquiries, feel free to open an issue on GitHub or contact the maintainer directly.

## Changelog
Please refer to the `CHANGELOG.md` file for more details on what has changed recently.
