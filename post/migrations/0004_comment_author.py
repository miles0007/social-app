# Generated by Django 3.0.3 on 2020-04-25 05:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_comment_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
    ]