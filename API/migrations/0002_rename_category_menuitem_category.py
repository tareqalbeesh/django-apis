# Generated by Django 4.2.4 on 2023-08-30 15:58

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("API", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="menuitem",
            old_name="Category",
            new_name="category",
        ),
    ]
