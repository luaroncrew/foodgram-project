# Generated by Django 3.0.5 on 2021-03-14 17:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0009_auto_20210313_1307'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='ingredients',
        ),
        migrations.AddField(
            model_name='component',
            name='recipe',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='ingredients', to='recipes.Recipe'),
            preserve_default=False,
        ),
    ]
