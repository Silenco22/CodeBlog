# Generated by Django 4.1.1 on 2022-10-02 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_alter_blogpost_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='image',
            field=models.FileField(upload_to=''),
        ),
    ]
