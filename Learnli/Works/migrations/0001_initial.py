# Generated by Django 3.2.25 on 2024-08-15 19:22

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Classes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(max_length=1000000)),
                ('title', models.CharField(max_length=1000000)),
                ('description', ckeditor.fields.RichTextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='media')),
                ('Duration', models.CharField(max_length=2000)),
                ('created_on', models.DateField(auto_now=True)),
                ('category', models.CharField(choices=[('science', 'science'), ('Arts', 'Arts'), ('Engineering', 'Engineering'), ('Business', 'Business'), ('creative_work', 'creative_work'), ('Languages', 'Languages'), ('computor_science', 'computer_science'), ('others', 'others'), ('Religios_studies', 'Religious_studies')], max_length=100000000)),
            ],
        ),
        migrations.CreateModel(
            name='Lessons',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000000)),
                ('power', models.CharField(max_length=11)),
                ('position', models.IntegerField(blank=True, null=True)),
                ('created_on', models.DateField(auto_now_add=True)),
                ('notes', models.FileField(upload_to='notes/')),
                ('video', models.FileField(upload_to='video/')),
                ('display_image', models.ImageField(blank=True, null=True, upload_to='media')),
                ('subtitle_file', models.FileField(blank=True, null=True, upload_to='subtitles/')),
                ('transcript_file', models.FileField(blank=True, null=True, upload_to='transcripts/')),
            ],
        ),
        migrations.CreateModel(
            name='Subjects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100000)),
                ('description', ckeditor.fields.RichTextField()),
                ('created_on', models.DateField(auto_now=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='media')),
            ],
        ),
    ]
