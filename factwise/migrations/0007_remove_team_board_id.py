# Generated by Django 4.2.3 on 2023-09-18 07:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('factwise', '0006_alter_task_task_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='board_id',
        ),
    ]
