# Generated by Django 4.2.2 on 2023-06-29 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_result_marks'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='grade',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
