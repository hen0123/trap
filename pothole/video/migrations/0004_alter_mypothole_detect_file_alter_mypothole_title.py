# Generated by Django 4.1.7 on 2023-04-06 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0003_alter_mypothole_lat_alter_mypothole_long_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mypothole',
            name='detect_file',
            field=models.ImageField(upload_to='upload'),
        ),
        migrations.AlterField(
            model_name='mypothole',
            name='title',
            field=models.CharField(default='20230406_122855_679466', max_length=200),
        ),
    ]
