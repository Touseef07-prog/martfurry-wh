# Generated by Django 2.2.12 on 2021-11-08 15:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0010_auto_20211106_0652'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('order', '0004_delete_subscription'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscription_id', models.CharField(max_length=100)),
                ('date', models.DateTimeField(editable=False)),
                ('quantity', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('delivered', 'delivered'), ('undelivered', 'undelivered')], default='undelivered', max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]