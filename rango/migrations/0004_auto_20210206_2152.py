# Generated by Django 2.2.17 on 2021-02-06 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0003_choice_question'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'categories'},
        ),
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(default=''),
            preserve_default=False,
        ),
    ]
