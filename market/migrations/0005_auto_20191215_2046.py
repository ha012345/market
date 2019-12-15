# Generated by Django 3.0 on 2019-12-15 11:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('market', '0004_userinfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='info', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='usertype',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='type', to=settings.AUTH_USER_MODEL),
        ),
    ]
