# Generated by Django 2.2.12 on 2021-11-05 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_product_product_stripe_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_stripe_id',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
