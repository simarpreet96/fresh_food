# Generated by Django 2.2 on 2020-02-14 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0003_billingaddress'),
    ]

    operations = [
        migrations.AddField(
            model_name='wish',
            name='price',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
