# Generated by Django 2.2.1 on 2019-05-22 00:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0004_items'),
    ]

    operations = [
        migrations.RenameField(
            model_name='items',
            old_name='product_advertise',
            new_name='product_category',
        ),
        migrations.RenameField(
            model_name='items',
            old_name='log',
            new_name='product_log',
        ),
        migrations.RenameField(
            model_name='items',
            old_name='product_categories',
            new_name='product_ranking',
        ),
        migrations.RenameField(
            model_name='items',
            old_name='rank_number',
            new_name='product_ranking_number',
        ),
        migrations.RemoveField(
            model_name='items',
            name='product_categorys',
        ),
        migrations.RemoveField(
            model_name='items',
            name='rank',
        ),
    ]
