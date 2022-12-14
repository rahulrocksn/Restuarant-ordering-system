# Generated by Django 4.0.4 on 2022-05-24 07:05

import chewapp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chewapp', '0004_order_payment_reference'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='imgName',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='menuitem',
            name='menuImg',
            field=models.ImageField(default='chewapp\\static\\chewapp\\FoodImages\testing.jpg', upload_to='static/'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='status',
            field=models.IntegerField(default=chewapp.models.OrderStatus['PLACED']),
        ),
    ]
