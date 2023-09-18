import sys
import os
import django
sys.path.append('C:\\Users\\apcr7\\OneDrive\\Documents\\Downloads\\Factwise_python challenge 25082023\\factwise-python\\mysite')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from factwise.models import User
from factwise.models import Team
from factwise.models import Board
from factwise.models import Task
import json
from prettytable import PrettyTable

class ProjectBoardBase:
    """
    A project board is a unit of delivery for a project. Each board will have a set of tasks assigned to a user.
    """

    # create a board - passed
    def create_board(self, request: str):
        """
        :param request: A json string with the board details.
        {
            "name" : "<board_name>",
            "description" : "<description>",
            "team_id" : "<team id>"
            "creation_time" : "<date:time when board was created>"
        }
        :return: A json string with the response {"id" : "<board_id>"}

        Constraint:
         * board name must be unique for a team
         * board name can be max 64 characters
         * description can be max 128 characters
        """
        serialized = json.loads(request)
        team = Team.objects.get(team_id = serialized["team_id"])
        entry = Board(board_name = serialized["name"], board_description = serialized["description"], team_id = team)
        entry.save()
        ret = {}
        ret["id"] = Board.objects.get(board_name = serialized["name"]).board_id
        return json.dumps(ret)
        

    # close a board - passed
    def close_board(self, request: str) -> str:
        """
        :param request: A json string with the user details
        {
          "id" : "<board_id>"
        }

        :return:

        Constraint:
          * Set the board status to CLOSED and record the end_time date:time
          * You can only close boards with all tasks marked as COMPLETE
        """
        serialized = json.loads(request)
        board_id = serialized["id"]
        board = Board.objects.get(board_id = board_id)
        tasks = Task.objects.filter(board_id = board)
        all_closed = True
        for task in tasks:
            if task.task_status != "COMPLETE":
                all_closed = False
                break
        
        if all_closed:
            board.board_status = "CLOSED"
            board.save()
        else:
            raise Exception("Tasks are incomplete. Board cannot be closed")

    # add task to board - notes - passed
    def add_task(self, request: str) -> str:
        """
        :param request: A json string with the task details. Task is assigned to a user_id who works on the task
        {
            "title" : "<task_title>",
            "board_id" : <board_id>,
            "description" : "<description>",
            "user_id" : "<user id>"
        }
        :return: A json string with the response {"id" : "<task_id>"}

        Constraint:
         * task title must be unique for a board
         * title name can be max 64 characters
         * description can be max 128 characters

        Constraints:
        * Can only add task to an OPEN board
        """
        serialized = json.loads(request)
        board = Board.objects.get(board_id = serialized["board_id"])
        
        if board.board_status == "OPEN":
            open = True
        else:
            open = False
        if not open:
            raise Exception("Board is not open")
        elif(len(serialized["title"]) > 64 or len(serialized["description"]) > 128):
            raise Exception("Length of title/description is too long")
        else:
            user = User.objects.get(user_id = serialized["user_id"])
            entry = Task(task_title = serialized["title"], board_id = board, user_id = user, task_description = serialized["description"])
            entry.save()
            id = Task.objects.get(task_title = serialized["title"]).task_id
            dict = {}
            dict["id"] = id
            return json.dumps(dict)

    # update the status of a task - passed
    def update_task_status(self, request: str):
        """
        :param request: A json string with the user details
        {
            "id" : "<task_id>",
            "status" : "OPEN | IN_PROGRESS | COMPLETE"
        }
        """
        serialized = json.loads(request)
        entry = Task.objects.get(task_id = serialized["id"])
        if serialized["status"] == "OPEN" or serialized["status"] == "IN_PROGRESS" or serialized["status"] == "COMPLETE":
            entry.task_status = serialized["status"]
            entry.save()
        else:
            raise Exception("Value of status provided in invalid")    
        

        

    # list all open boards for a team - passed
    def list_boards(self, request: str) -> str:
        """
        :param request: A json string with the team identifier
        {
          "id" : "<team_id>"
        }

        :return:
        [
          {
            "id" : "<board_id>",
            "name" : "<board_name>"
          }
        ]
        """
        serialized = json.loads(request)
        team_id = serialized["id"]
        team = Team.objects.get(team_id = team_id)
        entries = Board.objects.filter(team_id = team)
        ret = []
        for x in entries:
            if entries == None or len(entries) == 0:
                break
            else:
                dict = {}
                dict["id"] = x.board_id
                dict["name"] = x.board_name
                ret.append(dict)

        return json.dumps(ret)
            

    # passed - notes
    def export_board(self, request: str) -> str:
        """
        Export a board in the out folder. The output will be a txt file.
        We want you to be creative. Output a presentable view of the board and its tasks with the available data.
        :param request:
        {
          "id" : "<board_id>"
        }
        :return:
        {
          "out_file" : "<name of the file created>"
        }
        """
        serialized = json.loads(request)
        board_id = serialized["id"]
        board = Board.objects.get(board_id = board_id)
        dict = {}
        dict["board_name"] = board.board_name
        dict["board_description"] = board.board_description
        dict["board_id"] = board.board_id
        dict["board_status"] = board.board_status
        dict["creation_time"] = board.creation_time.strftime('%a %d %b %Y, %I:%M%p')
        if board.end_time == None:
            dict["end_time"] = board.end_time
        else:
            dict["end_time"] = board.end_time.strftime("%d/%m/%Y, %H:%M:%S")
        team = board.team_id
        if team == None:
            dict["team_status"] = "NOT_ASSIGNED"
        else:
            dict["team_status"] = "ASSIGNED"
            dict["team_name"] = team.team_name
            dict["team_id"] = team.team_id
            dict["team_description"] = team.team_description
            dict["team_admin"] = team.admin.user_id

        text = json.dumps(dict) + "\n\n\nTasks:\n"

        table = PrettyTable()
        table.field_names = ["task_id", "title", "description", "status", "user_id", "user_name", "creation_time"]
        tasks = Task.objects.filter(board_id = board)
        for task in tasks:
            user = task.user_id
            table.add_row([task.task_id, task.task_title, task.task_description, task.task_status, user.user_id, user.user_name, task.creation_time.strftime("%d/%m/%Y, %H:%M:%S")])
        
        text = text + table.get_string()

        with open("out/" + board.board_name + ".txt", 'w') as f:
            f.write(text)

        ret = {}
        ret["out_file"] = board.board_name + ".txt"
        return json.dumps(ret)


