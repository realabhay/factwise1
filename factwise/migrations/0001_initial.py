# Generated by Django 4.2.3 on 2023-09-13 14:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('board_name', models.CharField(max_length=64, unique=True)),
                ('board_description', models.CharField(max_length=128)),
                ('board_id', models.IntegerField(primary_key=True, serialize=False)),
                ('board_status', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('team_id', models.IntegerField(primary_key=True, serialize=False)),
                ('team_name', models.CharField(max_length=64, unique=True)),
                ('team_description', models.CharField(max_length=128)),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_name', models.CharField(max_length=64, unique=True)),
                ('display_name', models.CharField(max_length=128)),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('user_id', models.IntegerField(primary_key=True, serialize=False)),
                ('team_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='factwise.team')),
            ],
        ),
        migrations.AddField(
            model_name='team',
            name='admin',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='factwise.user'),
        ),
        migrations.AddField(
            model_name='team',
            name='board_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='factwise.board'),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('task_title', models.CharField(max_length=64, unique=True)),
                ('task_description', models.CharField(max_length=128)),
                ('task_id', models.IntegerField(primary_key=True, serialize=False)),
                ('task_status', models.CharField(max_length=15)),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('board_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='factwise.board')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='factwise.user')),
            ],
        ),
    ]