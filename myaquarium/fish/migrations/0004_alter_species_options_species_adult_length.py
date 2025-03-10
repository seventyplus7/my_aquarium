# Generated by Django 4.2.16 on 2024-12-13 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("fish", "0003_alter_species_options_species_recommended_tank"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="species",
            options={"ordering": ["name"], "verbose_name_plural": "Species"},
        ),
        migrations.AddField(
            model_name="species",
            name="adult_length",
            field=models.PositiveIntegerField(null=True),
        ),
    ]
