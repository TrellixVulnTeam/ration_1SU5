# Generated by Django 2.0.2 on 2018-05-07 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_item_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]