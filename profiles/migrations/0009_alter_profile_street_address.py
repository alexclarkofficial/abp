# Generated by Django 4.2.13 on 2024-10-10 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0008_alter_profile_council_district_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="street_address",
            field=models.CharField(
                help_text=(
                    "Your street address will be used to determine your "
                    "Philadelphia City Council District and connect you "
                    "with actions you can take in your specific neighborhood."
                ),
                max_length=256,
                null=True,
                verbose_name="Street Address",
            ),
        ),
    ]
