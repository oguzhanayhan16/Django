# Generated by Django 5.1.4 on 2024-12-15 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_blog_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='BlogCreateDate',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
