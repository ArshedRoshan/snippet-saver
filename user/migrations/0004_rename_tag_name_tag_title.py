# Generated by Django 4.2.1 on 2023-06-02 14:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_rename_title_tag_tag_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tag',
            old_name='tag_name',
            new_name='title',
        ),
    ]
