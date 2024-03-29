# Generated by Django 4.0.2 on 2022-04-20 10:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0011_productreview'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='banner',
            options={'verbose_name_plural': '01. Banners'},
        ),
        migrations.AlterModelOptions(
            name='brand',
            options={'verbose_name_plural': '03. Brands'},
        ),
        migrations.AlterModelOptions(
            name='cartorder',
            options={'verbose_name_plural': '08. Orders'},
        ),
        migrations.AlterModelOptions(
            name='cartorderitems',
            options={'verbose_name_plural': '09. Ordered Items'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': '02. Categories'},
        ),
        migrations.AlterModelOptions(
            name='color',
            options={'verbose_name_plural': '04. Colors'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name_plural': '06. Products'},
        ),
        migrations.AlterModelOptions(
            name='productattribute',
            options={'verbose_name_plural': '07. ProductAttributes'},
        ),
        migrations.AlterModelOptions(
            name='productreview',
            options={'verbose_name_plural': '10. Product Reviews'},
        ),
        migrations.AlterModelOptions(
            name='size',
            options={'verbose_name_plural': '05. Sizes'},
        ),
        migrations.CreateModel(
            name='wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
