# Generated by Django 2.2.12 on 2021-11-08 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_auto_20211108_1631'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='contact',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='subscription',
            name='date',
            field=models.DateTimeField(auto_created=True, auto_now_add=True),
        ),
    ]
