# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-03-13 11:22
from __future__ import unicode_literals

from django.db import migrations


def set_null_to_blank(queryset, fields):
    for element in queryset:
        for field in fields:
            value = getattr(element, field)
            if value is None:
                setattr(element, field, '')
        element.save()


def run_data_migration(apps, schema_editor):
    Task = apps.get_model('tasks', 'Task')

    set_null_to_blank(Task.objects.all(), [
        'uri',
        'uri_prefix',
        'key',
        'comment',
        'title_lang1',
        'title_lang2',
        'title_lang3',
        'title_lang4',
        'title_lang5',
        'text_lang1',
        'text_lang2',
        'text_lang3',
        'text_lang4',
        'text_lang5',
    ])


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0020_add_language_fields'),
    ]

    operations = [
        migrations.RunPython(run_data_migration),
    ]
