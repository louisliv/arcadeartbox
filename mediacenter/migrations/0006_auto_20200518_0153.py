# Generated by Django 3.0.6 on 2020-05-18 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mediacenter', '0005_auto_20200517_2133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='file_path',
            field=models.FileField(upload_to='photos/'),
        ),
    ]