# Generated by Django 2.0.2 on 2018-05-26 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0034_user_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='update',
            name='is_main',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
    ]
