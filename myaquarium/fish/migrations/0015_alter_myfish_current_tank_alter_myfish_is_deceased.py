# Generated by Django 4.2.16 on 2024-12-14 14:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("fish", "0014_alter_species_photo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="myfish",
            name="current_tank",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="fish.tank",
            ),
        ),
        migrations.AlterField(
            model_name="myfish",
            name="is_deceased",
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
