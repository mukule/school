# Generated by Django 4.2.2 on 2023-07-04 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_delete_studentresult'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='class_teacher_comments',
            field=models.TextField(blank=True),
        ),
    ]