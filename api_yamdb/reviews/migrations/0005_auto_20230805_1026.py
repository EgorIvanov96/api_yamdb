# Generated by Django 3.2 on 2023-08-05 07:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_alter_title_genre'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={},
        ),
        migrations.RemoveConstraint(
            model_name='review',
            name='unique review',
        ),
    ]
