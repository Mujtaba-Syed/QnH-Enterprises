# Generated by Django 5.1.7 on 2025-03-31 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('product_type', models.CharField(choices=[('perfume', 'Perfume'), ('shirt', 'Shirt'), ('car', 'Car'), ('watch', 'Watch')], default='perfume', max_length=50)),
                ('sku', models.CharField(max_length=100, unique=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('brand', models.CharField(blank=True, max_length=100, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='product_images/')),
                ('attributes', models.JSONField(blank=True, default=dict, null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]
