# Generated by Django 2.2.10 on 2020-05-02 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mercury", "0023_auto_20200502_1608"),
    ]

    operations = [
        migrations.AlterField(
            model_name="gfconfig",
            name="gf_name",
            field=models.CharField(blank=True, default="", max_length=64),
        ),
    ]
