# django-yamlfield
Same as Django JSONField but represent it as YAML (internally stores as JSON)


### Example


```python

from django.db import models
from django_yaml_field.fields import YAMLField


class ModelName(models.Model):
	yaml = YAMLField()
```

### License

MIT