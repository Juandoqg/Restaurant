# Generated by Django 5.0.3 on 2024-10-15 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_user_documento_user_expedicion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='documento',
            field=models.IntegerField(null=True),
        ),
    ]
