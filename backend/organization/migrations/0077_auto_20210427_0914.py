# Generated by Django 2.2.13 on 2021-04-27 09:14

from django.db import migrations


class Migration(migrations.Migration):

    # manually changed this because of a merge. Without this manual change certain migrations would have had to be faked
    dependencies = [
        ('organization', '0077_auto_20210430_1031'),
    ]

    operations = [
        migrations.RenameField(
            model_name='organization',
            old_name='short_description',
            new_name='about',
        ),
    ]