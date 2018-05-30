# Generated by Django 2.0.5 on 2018-05-30 10:31

import cover.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(max_length=4000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('upvotes', models.PositiveIntegerField(default=0)),
                ('downvotes', models.PositiveIntegerField(default=0)),
                ('image', models.ImageField(blank=True, default='', upload_to=cover.models.post_image_path)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SchoolProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('points', models.PositiveIntegerField(default=0)),
                ('website', models.URLField(blank=True, default='')),
                ('image', models.ImageField(blank=True, upload_to=cover.models.school_image_path)),
                ('address', models.TextField(blank=True)),
                ('country', models.TextField(default='IN')),
            ],
        ),
        migrations.CreateModel(
            name='StudentProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=20)),
                ('bio', models.TextField(blank=True, default='')),
                ('gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('reputation', models.PositiveIntegerField(default=0)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='school', to='cover.SchoolProfile')),
                ('user', models.OneToOneField(on_delete='cascade', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=255)),
                ('last_updated', models.DateTimeField(auto_now_add=True)),
                ('views', models.PositiveIntegerField(default=0)),
                ('upvotes', models.PositiveIntegerField(default=0)),
                ('downvotes', models.PositiveIntegerField(default=0)),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topics', to='cover.Board')),
                ('starter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topics', to=settings.AUTH_USER_MODEL)),
                ('voters', models.ManyToManyField(blank=True, related_name='voters', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='cover.Topic'),
        ),
        migrations.AddField(
            model_name='post',
            name='updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='post',
            name='voters',
            field=models.ManyToManyField(blank=True, related_name='post_voters', to=settings.AUTH_USER_MODEL),
        ),
    ]
