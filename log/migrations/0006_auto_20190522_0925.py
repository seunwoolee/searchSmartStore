# Generated by Django 2.2.1 on 2019-05-22 00:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0005_auto_20190522_0912'),
    ]

    operations = [
        migrations.RenameField(
            model_name='items',
            old_name='product_category',
            new_name='result_product_category',
        ),
        migrations.RenameField(
            model_name='items',
            old_name='product_log',
            new_name='result_product_log',
        ),
        migrations.RenameField(
            model_name='items',
            old_name='product_name',
            new_name='result_product_name',
        ),
        migrations.RenameField(
            model_name='items',
            old_name='product_price',
            new_name='result_product_price',
        ),
        migrations.RenameField(
            model_name='items',
            old_name='product_ranking',
            new_name='result_product_ranking',
        ),
        migrations.RenameField(
            model_name='items',
            old_name='product_ranking_number',
            new_name='result_product_ranking_number',
        ),
    ]
