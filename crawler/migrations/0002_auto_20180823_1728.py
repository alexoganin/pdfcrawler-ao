# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-23 17:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pdffiles',
            options={'ordering': ['-time']},
        ),
        migrations.AlterField(
            model_name='urls',
            name='pdf_file',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='urls', to='crawler.PdfFiles'),
        ),
    ]