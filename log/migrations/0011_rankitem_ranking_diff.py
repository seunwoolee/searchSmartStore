# Generated by Django 2.2.1 on 2019-05-22 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0010_rankitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='rankitem',
            name='ranking_diff',
            field=models.IntegerField(default=0),
        ),
    ]
