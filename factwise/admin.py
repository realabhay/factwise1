from django.contrib import admin

# Register your models here.

from .models import User, Board, Team, Task, UserxTeam

admin.site.register(User)
admin.site.register(Board)
admin.site.register(Team)
admin.site.register(Task)
admin.site.register(UserxTeam)
