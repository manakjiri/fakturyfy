# Generated by Django 5.0.2 on 2024-02-13 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0003_alter_entity_bank_code"),
    ]

    operations = [
        migrations.AlterField(
            model_name="entity",
            name="bank_account",
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
