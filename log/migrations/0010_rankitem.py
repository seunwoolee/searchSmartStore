# Generated by Django 2.2.1 on 2019-05-22 01:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0009_auto_20190522_1001'),
    ]

    operations = [
        migrations.CreateModel(
            name='RankItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('ranking', models.CharField(max_length=255)),
                ('ranking_number', models.IntegerField()),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='log.Items')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
