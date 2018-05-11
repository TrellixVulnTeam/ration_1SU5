# Generated by Django 2.0.2 on 2018-05-11 04:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0011_user_item_updated_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_Item_Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=255)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_item_logs', to='core.Item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_item_logs', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='user_item',
            name='updated_at',
        ),
    ]