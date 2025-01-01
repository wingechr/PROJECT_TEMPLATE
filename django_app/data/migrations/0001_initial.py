# Generated by Django 5.1 on 2025-01-01 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Data",
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
                ("key", models.CharField(max_length=128, unique=True)),
                ("value", models.TextField(blank=True, null=True)),
            ],
            options={
                "db_table": "data",
                "managed": False,
            },
        ),
    ]
