# Generated by Django 3.2.25 on 2024-08-15 19:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Works', '0001_initial'),
        ('Examination', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='test_answer_response',
            name='Subject',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Subject', to='Works.subjects'),
        ),
        migrations.AddField(
            model_name='test_answer_response',
            name='answer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='answer', to='Examination.test_answer'),
        ),
    ]
