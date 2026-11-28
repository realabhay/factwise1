# CRUD guide

This guide shows how to work with the Factwise assignment from Django's Python shell. The project does **not** currently expose CRUD HTTP/REST endpoints: its `/` route only returns a welcome message. The `UserBase`, `TeamBase`, and `ProjectBoardBase` classes are Python helpers that return JSON strings for some operations.

## Start the project

From the repository root in PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
python manage.py shell
```

If you have not set up a virtual environment yet, see [README.md](README.md) for installation steps. The repository includes a sample SQLite database.

In the Django shell, import the helpers and models:

```python
import json
from factwise.user_base import UserBase
from factwise.team_base import TeamBase
from factwise.project_board_base import ProjectBoardBase
from factwise.models import User, UserxTeam, Team, Board, Task

users_api = UserBase()
teams_api = TeamBase()
boards_api = ProjectBoardBase()
```

The helper methods take JSON **strings** as arguments. Use `json.dumps(...)` to build them, and `json.loads(...)` to turn returned JSON strings into Python values.

## Creation IDs

The models declare their IDs as regular integer primary keys rather than Django `AutoField`s. With this project's SQLite database, the `create_user`, `create_team`, `create_board`, and `add_task` helpers successfully create records and return generated IDs. I verified this using a transaction that was rolled back afterward. If you switch to a different database backend, review ID generation first; this SQLite behavior may not carry over unchanged.

## Users

### Read

```python
json.loads(users_api.list_users())
json.loads(users_api.describe_user(json.dumps({"id": 1})))
```

`list_users()` returns each user's name, display name, and creation time. `describe_user()` returns one user's name, description, and creation time.

### Create

```python
new_user_id = json.loads(users_api.create_user(json.dumps({
    "name": "jordan.ross",
    "display_name": "Jordan Ross",
})))["id"]
```

### Update

The helper's current implementation updates both `display_name` and `user_name`, although its docstring says the name cannot be changed:

```python
users_api.update_user(json.dumps({
    "id": 3,
    "user": {"name": "jordan.ross", "display_name": "Jordan R."},
}))
```

It does not return a success message. You can read the updated user with `describe_user`.

### Delete

There is no user-delete helper. Delete a user with the ORM:

```python
User.objects.get(user_id=3).delete()
```

Deleting a user also deletes their `UserxTeam` memberships. A team's admin reference and a task's assignee are set to null.

## Teams and memberships

### Read

```python
json.loads(teams_api.list_teams())
json.loads(teams_api.describe_team(json.dumps({"id": 1})))
json.loads(teams_api.list_team_users(json.dumps({"id": 1})))
json.loads(teams_api.get_user_teams(json.dumps({"id": 1})))
```

### Create

The admin must refer to an existing user:

```python
new_team_id = json.loads(teams_api.create_team(json.dumps({
    "name": "Release Team",
    "description": "Team preparing the release",
    "admin": 1,
})))["id"]
```

### Update

```python
teams_api.update_team(json.dumps({
    "id": 2,
    "team": {
        "name": "Release Team",
        "description": "Team coordinating the release",
        "admin": 3,
    },
}))
```

`update_team` returns `"Success"` when it completes.

### Add or remove members

Membership is managed independently from creating or deleting users:

```python
teams_api.add_users_to_team(json.dumps({"id": 2, "users": [3]}))
teams_api.remove_users_from_team(json.dumps({"id": 2, "users": [3]}))
```

A team can have at most 50 members. Removing a member removes only the membership row.

### Delete

There is no team-delete helper. Use the ORM:

```python
Team.objects.get(team_id=2).delete()
```

Deleting a team leaves its boards in place but sets their `team_id` to null; memberships for the team are deleted.

## Boards and tasks

### Create a board

A board needs an existing team:

```python
new_board_id = json.loads(boards_api.create_board(json.dumps({
    "name": "Release Prep",
    "description": "Work for the upcoming release",
    "team_id": 1,
})))["id"]
```

### Read boards and tasks

There is no `describe_board` or task-list helper. `list_boards` lists boards for a team (including boards that are not open):

```python
json.loads(boards_api.list_boards(json.dumps({"id": 2})))
list(Task.objects.filter(board_id__board_id=2).values(
    "task_id", "task_title", "task_description", "task_status", "user_id"
))
```

### Create a task

The board must be open, and the assignee must be an existing user:

```python
new_task_id = json.loads(boards_api.add_task(json.dumps({
    "title": "Write release checklist",
    "description": "Prepare the release checklist",
    "board_id": 1,
    "user_id": 1,
})))["id"]
```

The model enforces globally unique task titles, not just unique titles within one board.

### Update task status

The helper accepts `OPEN`, `IN_PROGRESS`, or `COMPLETE`:

```python
boards_api.update_task_status(json.dumps({"id": 3, "status": "IN_PROGRESS"}))
```

### Close a board

A board can be closed only when every task is `COMPLETE`:

```python
boards_api.close_board(json.dumps({"id": 2}))
```

The current implementation changes `board_status` to `CLOSED`, but it does not set `end_time` despite the method docstring saying it records that time.

### Delete

There are no board- or task-delete helpers. Use the ORM if you need to remove records:

```python
Task.objects.get(task_id=3).delete()
Board.objects.get(board_id=2).delete()
```

Deleting a board cascades and deletes its tasks. Deleting a task does not delete its board.

## Reset the sample database

If you want to discard shell changes and return to the committed sample database, close the shell and run:

```powershell
git restore db.sqlite3
```

This discards all uncommitted changes stored in the SQLite database.
