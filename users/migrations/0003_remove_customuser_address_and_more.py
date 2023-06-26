# Generated by Django 4.2.2 on 2023-06-26 08:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_customuser_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='address',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='contact_number',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='current_class',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='curriculum_activity',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='leadership',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='parent_contact',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='parent_name',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='subjects',
        ),
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('address', models.CharField(max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='parent', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]