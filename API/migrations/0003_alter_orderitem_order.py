# Generated by Django 4.2.4 on 2023-09-04 13:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("API", "0002_rename_category_menuitem_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="orderitem",
            name="order",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="API.order"
            ),
        ),
    ]
