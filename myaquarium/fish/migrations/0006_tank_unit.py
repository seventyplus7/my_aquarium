# Generated by Django 4.2.16 on 2024-12-13 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("fish", "0005_alter_myfish_options_alter_tank_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="tank",
            name="unit",
            field=models.PositiveSmallIntegerField(
                choices=[(1, "Liter"), (2, "Gallon")], null=True
            ),
        ),
    ]
