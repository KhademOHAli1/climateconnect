# Generated by Django 2.2.11 on 2020-04-11 19:04

from django.db import migrations, models
import organization.models.project


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0006_auto_20200411_1658'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Points to project name', max_length=1024, verbose_name='Name')),
                ('slug', models.CharField(blank=True, help_text='URL slug for project', max_length=1024, null=True, unique=True, verbose_name='Slug')),
                ('image', models.ImageField(blank=True, help_text='Project image', null=True, upload_to=organization.models.project.project_image_path, verbose_name='Image')),
                ('status', models.CharField(choices=[('idea', 'Idea'), ('in_progress', 'In Progress'), ('finished', 'Finished'), ('cancelled', 'Cancelled'), ('recurring', 'Recurring')], default='idea', help_text='Points to status of the project', max_length=64, verbose_name='Status')),
                ('start_date', models.DateTimeField(blank=True, help_text='Points to start date of the project', null=True, verbose_name='Start Date')),
                ('end_date', models.DateTimeField(blank=True, help_text='Points to end date of the project', null=True, verbose_name='End Date')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Points to creation date of the project', verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Points to time when project was updated', verbose_name='Updated At')),
                ('short_description', models.TextField(blank=True, help_text='Points to short description about the project', null=True, verbose_name='Short Description')),
            ],
            options={
                'verbose_name': 'Project',
                'verbose_name_plural': 'Projects',
            },
        ),
    ]