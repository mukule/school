# Generated by Django 4.2.2 on 2023-07-04 11:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_studentresult'),
    ]

    operations = [
        migrations.DeleteModel(
            name='StudentResult',
        ),
    ]