# Generated by Django 2.0.5 on 2018-05-30 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0002_auto_20180530_1107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='link',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]
