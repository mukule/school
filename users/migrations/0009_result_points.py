# Generated by Django 4.2.2 on 2023-07-04 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_remove_result_points'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='points',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
    ]