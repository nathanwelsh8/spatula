# Generated by Django 2.2.3 on 2020-03-10 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spatulaApp', '0003_auto_20200310_1604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(max_length=255, upload_to='media/images\\usruploads'),
        ),
    ]