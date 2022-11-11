# Generated by Django 4.1.3 on 2022-11-11 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tokens', '0002_jwttoken_expiration_alter_jwttoken_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jwttoken',
            name='expiration',
            field=models.SmallIntegerField(choices=[(1, '1 დღიანი'), (2, '2 დღიანი'), (7, '1 კვირიანი'), (30, '1 თვიანი'), (90, '3 თვიანი'), (180, '6 თვიანი'), (365, '1 წლიანი'), (730, '2 წლიანი')], help_text='თოქენის ვალიდურობის დრო'),
        ),
    ]