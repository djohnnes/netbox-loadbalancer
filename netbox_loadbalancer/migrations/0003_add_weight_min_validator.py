import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netbox_loadbalancer', '0002_add_port_weight_validators'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poolmember',
            name='weight',
            field=models.PositiveIntegerField(
                default=1,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(65535),
                ],
            ),
        ),
    ]
