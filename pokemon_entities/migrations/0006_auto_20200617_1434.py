# Generated by Django 2.2.3 on 2020-06-17 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0005_pokemon_previous_evolution'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemon',
            name='english_title',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='pokemon',
            name='japanese_title',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
