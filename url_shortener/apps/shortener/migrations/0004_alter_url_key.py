# Generated by Django 4.1.3 on 2022-11-07 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shortener', '0003_rename_url_url_redirect_url_url_url_key_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='url',
            name='key',
            field=models.CharField(blank=True, max_length=256, null=True, unique=True),
        ),
    ]