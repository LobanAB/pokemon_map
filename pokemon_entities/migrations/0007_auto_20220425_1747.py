# Generated by Django 3.1.14 on 2022-04-25 14:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0006_auto_20220422_1422'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pokemonentity',
            old_name='Lat',
            new_name='lat',
        ),
        migrations.RenameField(
            model_name='pokemonentity',
            old_name='Lon',
            new_name='lon',
        ),
        migrations.RenameField(
            model_name='pokemonentity',
            old_name='Pokemon',
            new_name='pokemon',
        ),
    ]