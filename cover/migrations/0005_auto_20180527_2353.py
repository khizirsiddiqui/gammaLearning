# Generated by Django 2.0.5 on 2018-05-27 18:23

import cover.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cover', '0004_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, default='', upload_to=cover.models.post_image_path),
        ),
    ]
