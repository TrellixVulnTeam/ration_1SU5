# Generated by Django 2.0.2 on 2018-05-16 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_taglist_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taglist',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
