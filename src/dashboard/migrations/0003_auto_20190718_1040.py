# Generated by Django 2.2.3 on 2019-07-18 10:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_article'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='posted_on',
            new_name='posted_age',
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
