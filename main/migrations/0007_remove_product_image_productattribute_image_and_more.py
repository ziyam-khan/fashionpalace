# Generated by Django 4.0.2 on 2022-02-25 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_banner_img'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='image',
        ),
        migrations.AddField(
            model_name='productattribute',
            name='image',
            field=models.ImageField(null=True, upload_to='product_imgs/'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='img',
            field=models.ImageField(upload_to='banner_imgs/'),
        ),
    ]
