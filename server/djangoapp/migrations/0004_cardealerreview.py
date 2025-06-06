# Generated by Django 5.2.1 on 2025-05-30 00:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("djangoapp", "0003_alter_carmodel_year"),
    ]

    operations = [
        migrations.CreateModel(
            name="CarDealerReview",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("purchase", models.BooleanField(default=False)),
                ("review", models.TextField()),
                ("purchase_date", models.DateField(blank=True, null=True)),
                ("car_make", models.CharField(blank=True, max_length=100)),
                ("car_model", models.CharField(blank=True, max_length=100)),
                ("car_year", models.IntegerField(blank=True, null=True)),
                ("sentiment", models.CharField(blank=True, max_length=20)),
                (
                    "dealership",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="djangoapp.dealer",
                    ),
                ),
            ],
        ),
    ]
