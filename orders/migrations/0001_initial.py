# Generated by Django 3.0.4 on 2020-06-23 12:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0011_userdefaultaddress'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('carts', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(default='ABC', max_length=120, unique=True)),
                ('status', models.CharField(choices=[('Started', 'Started'), ('Abandoned', 'Abandoned'), ('Finished', 'Finished')], default='Started', max_length=120)),
                ('sub_total', models.DecimalField(decimal_places=2, default=10.99, max_digits=1000)),
                ('tax_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=1000)),
                ('final_total', models.DecimalField(decimal_places=2, default=10.99, max_digits=1000)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('billing_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='billing_address', to='accounts.UserAddress')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carts.Cart')),
                ('shipping_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shipping_address', to='accounts.UserAddress')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
