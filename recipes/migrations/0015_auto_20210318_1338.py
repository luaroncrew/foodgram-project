# Generated by Django 3.0.5 on 2021-03-18 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0014_auto_20210317_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='media/', verbose_name='картинка'),
        ),
    ]
