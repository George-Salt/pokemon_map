# Generated by Django 3.1.14 on 2022-10-31 12:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0012_auto_20221031_1507'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pokemon',
            name='previous_evolution',
        ),
        migrations.AddField(
            model_name='pokemon',
            name='previous_evolutions',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='next_evolutions', to='pokemon_entities.pokemon', verbose_name='Предыдущая эволюция'),
        ),
    ]
