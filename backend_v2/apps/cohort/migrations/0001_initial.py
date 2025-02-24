# Generated by Django 5.0.1 on 2024-11-14 03:38

import cohort.helpers.model.base
import django.db.models.deletion
import utils.helpers.models.base
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('utils', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000, verbose_name='course name')),
                ('description', models.TextField(verbose_name='description')),
                ('venue', models.JSONField(default=list, verbose_name='venue')),
                ('extra_info', models.TextField(verbose_name='extra_info')),
                ('status', models.BooleanField(default=True)),
                ('images', models.ManyToManyField(related_name='related_images', to='utils.image')),
            ],
            bases=(utils.helpers.models.base.BaseModelBaseMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000, verbose_name='registration name')),
                ('is_open', models.BooleanField(default=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('registrationFee', models.CharField(blank=True, max_length=50, null=True, verbose_name='registration fee')),
            ],
            bases=(utils.helpers.models.base.BaseModelBaseMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headline', models.CharField(max_length=1000, verbose_name='headline')),
                ('full_name', models.CharField(max_length=255, verbose_name='last name')),
                ('testimony', models.TextField(verbose_name='testimony')),
                ('picture', models.ImageField(upload_to=cohort.helpers.model.base.testimonial_image_location)),
                ('brief', models.CharField(max_length=255, verbose_name='author brief')),
            ],
            bases=(utils.helpers.models.base.BaseModelBaseMixin, utils.helpers.models.base.CloudinaryDeleteMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True, verbose_name='full name')),
                ('wallet_address', models.CharField(max_length=255, verbose_name='wallet address')),
                ('email', models.CharField(max_length=255, verbose_name='participant email')),
                ('status', models.CharField(choices=[('PENDING', 'PENDING'), ('ACCEPTED', 'ACCEPTED'), ('REJECTED', 'REJECTED')], default='PENDING', max_length=20)),
                ('motivation', models.TextField(null=True, verbose_name='motivation')),
                ('achievement', models.TextField(blank=True, null=True, verbose_name='achievement')),
                ('city', models.CharField(max_length=50, null=True, verbose_name='city name')),
                ('state', models.CharField(max_length=50, null=True, verbose_name='state name')),
                ('country', models.CharField(max_length=50, null=True, verbose_name='country name')),
                ('duration', models.CharField(max_length=100, null=True, verbose_name='duration')),
                ('gender', models.CharField(max_length=20, null=True, verbose_name='gender')),
                ('github', models.URLField(blank=True, max_length=250, null=True, verbose_name='github url')),
                ('number', models.CharField(max_length=20, null=True, verbose_name='phone number')),
                ('cohort', models.CharField(blank=True, max_length=10, null=True, verbose_name='cohort name')),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cohort.course')),
                ('registration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cohort.registration')),
            ],
            bases=(utils.helpers.models.base.BaseModelBaseMixin, models.Model),
        ),
    ]
