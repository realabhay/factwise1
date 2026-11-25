# Factwise project board

A Django app for managing users, teams, project boards, and tasks.

## Run locally

Requires Python 3.9 or newer. From the repository root:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r factwise\requirements.txt
python manage.py runserver
```

The repository includes a migrated SQLite database with sample users, teams, boards, and tasks. To recreate it from scratch, run:

```powershell
python manage.py migrate
python manage.py loaddata sample_data.json
```

Open <http://127.0.0.1:8000/> to see the app's welcome page. The database file `db.sqlite3` is intentionally tracked so the sample data is ready immediately after checkout. After resetting it, use `git checkout -- db.sqlite3` to restore the committed sample database.

## Assignment interfaces

The base interfaces are `factwise.user_base.UserBase`, `factwise.team_base.TeamBase`, and `factwise.project_board_base.ProjectBoardBase`. They return JSON strings where specified in their method documentation. Board exports are written to `out/<board name>.txt`; the directory is created automatically.

Task titles are globally unique, as enforced by the model. Install the packages listed in `factwise/requirements.txt`; board export uses `prettytable`.

## CRUD manual

See [CRUD_GUIDE.md](CRUD_GUIDE.md) for shell examples and current API limitations.
