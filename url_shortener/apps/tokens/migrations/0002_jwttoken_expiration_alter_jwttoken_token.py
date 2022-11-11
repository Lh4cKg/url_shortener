# Generated by Django 4.1.3 on 2022-11-11 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tokens', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='jwttoken',
            name='expiration',
            field=models.SmallIntegerField(choices=[(1, 'ერთ დღიანი'), (2, 'ორ დღიანი'), (7, '1 კვირიანი'), (30, '1 თვიანი'), (90, '3 თვიანი'), (180, '6 თვიანი'), (365, '1 წლიანი'), (730, '2 წლიანი')], default=1, help_text='თოქენის ვალიდურობის დრო'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='jwttoken',
            name='token',
            field=models.TextField(help_text='თოქენი დაგენერირდება ავტომატურად შენახვის შემდეგ'),
        ),
    ]