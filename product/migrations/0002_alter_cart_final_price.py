# Generated by Django 3.2.7 on 2021-09-30 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='final_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10),
        ),
    ]
