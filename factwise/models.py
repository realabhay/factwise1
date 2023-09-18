from django.db import models

# Create your models here.

class User(models.Model):
    user_name = models.CharField(max_length=64, unique=True, blank=False, null=False)
    description = models.CharField(max_length=260, null=True)
    display_name = models.CharField(max_length=128)
    creation_time = models.DateTimeField(auto_now_add=True)
    user_id = models.IntegerField(primary_key=True)
    
class UserxTeam(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    team_id = models.ForeignKey("Team", on_delete=models.CASCADE, blank=False, null=False)

class Board(models.Model):
    board_name = models.CharField(unique=True, max_length=64, blank=False, null=False)
    board_description = models.CharField(max_length=128)
    board_id = models.IntegerField(primary_key=True)
    board_status = models.CharField(max_length=15, default="OPEN", blank=False, null=False)
    creation_time = models.DateTimeField(auto_now_add=True)
    team_id = models.ForeignKey("Team", on_delete=models.SET_NULL, null=True)
    end_time = models.DateTimeField(blank=False, null=True, default=None)

class Team(models.Model):
    team_id = models.IntegerField(primary_key=True)
    team_name = models.CharField(max_length=64, unique=True, blank=False, null=False)
    team_description = models.CharField(max_length=128)
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    creation_time = models.DateTimeField(auto_now_add=True)

class Task(models.Model):
    task_title = models.CharField(max_length=64, unique=True, blank=False, null=False)
    task_description = models.CharField(max_length=128)
    board_id = models.ForeignKey(Board, on_delete=models.CASCADE)
    task_id = models.IntegerField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    task_status = models.CharField(max_length=15, default="OPEN")
    creation_time = models.DateTimeField(auto_now_add=True)





