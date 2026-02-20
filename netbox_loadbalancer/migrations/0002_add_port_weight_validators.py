import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netbox_loadbalancer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='virtualserver',
            name='port',
            field=models.PositiveIntegerField(
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(65535),
                ],
            ),
        ),
        migrations.AlterField(
            model_name='poolmember',
            name='port',
            field=models.PositiveIntegerField(
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(65535),
                ],
            ),
        ),
        migrations.AlterField(
            model_name='poolmember',
            name='weight',
            field=models.PositiveIntegerField(
                default=1,
                validators=[
                    django.core.validators.MaxValueValidator(65535),
                ],
            ),
        ),
    ]
