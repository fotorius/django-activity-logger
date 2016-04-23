# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion

def fix_paths(apps,schema_editor):
    """
    Copy the information from the Entry.path to a Path.name and reference the new
    instance from Entry.path_name to Path
    """
    Entry = apps.get_model("activity_logger", "Entry")
    Path = apps.get_model("activity_logger", "Path")

    entries = Entry.objects.all()
    for entry in entries:
        paths = Path.objects.filter(name=entry.deprecated_path)
        if paths:
            path = paths[0]
        else:
            path = Path(name=entry.deprecated_path).save()
        entry.path_name = path
        entry.save()
class Migration(migrations.Migration):

    dependencies = [
        ('activity_logger', '0009_auto_20160423_0919'),
    ]

    operations = [
        migrations.RunPython(fix_paths),
    ]
