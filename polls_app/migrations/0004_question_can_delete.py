# Generated by Django 4.0.3 on 2022-03-16 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls_app', '0003_alter_choice_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='can_delete',
            field=models.BooleanField(default=False),
        ),
    ]
