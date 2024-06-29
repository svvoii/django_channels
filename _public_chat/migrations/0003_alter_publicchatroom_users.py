# Generated by Django 5.0.6 on 2024-06-29 12:30

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('_public_chat', '0002_alter_publicroomchatmessage_managers_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicchatroom',
            name='users',
            field=models.ManyToManyField(blank=True, help_text='users in this chat room.', to=settings.AUTH_USER_MODEL),
        ),
    ]
