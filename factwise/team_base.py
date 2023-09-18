import sys
import os
import django
sys.path.append('C:\\Users\\apcr7\\OneDrive\\Documents\\Downloads\\Factwise_python challenge 25082023\\factwise-python\\mysite')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from factwise.models import User
from factwise.models import Team
from factwise.models import UserxTeam
import json

class TeamBase:
    """
    Base interface implementation for API's to manage teams.
    For simplicity a single team manages a single project. And there is a separate team per project.
    Users can be
    """

    # create a team - passed
    def create_team(self, request: str) -> str:
        """
        :param request: A json string with the team details
        {
          "name" : "<team_name>",
          "description" : "<some description>",
          "admin": "<id of a user>"
        }
        :return: A json string with the response {"id" : "<team_id>"}

        Constraint:
            * Team name must be unique
            * Name can be max 64 characters
            * Description can be max 128 characters
        """
        serialzed = json.loads(request)
        admin = User.objects.get(user_id = serialzed["admin"])
        entry = Team(team_name = serialzed["name"], team_description = serialzed["description"], admin = admin)
        entry.save()
        return_value = dict(id = Team.objects.get(team_name = serialzed["name"]).team_id)
        return json.dumps(return_value)

    # list all teams - passed
    def list_teams(self) -> str:
        """
        :return: A json list with the response.
        [
          {
            "name" : "<team_name>",
            "description" : "<some description>",
            "creation_time" : "<some date:time format>",
            "admin": "<id of a user>"
          }
        ]
        """
        entries = Team.objects.all()
        serialized = []
        for x in entries:
          dict = {}
          dict["name"] = x.team_name
          dict["description"] = x.team_description
          dict["creation_time"] = x.creation_time.strftime('%a %d %b %Y, %I:%M%p')
          dict["admin"] = x.admin.user_id
          serialized.append(dict)
        
        return json.dumps(serialized)

    # describe team - passed
    def describe_team(self, request: str) -> str:
        """
        :param request: A json string with the team details
        {
          "id" : "<team_id>"
        }

        :return: A json string with the response

        {
          "name" : "<team_name>",
          "description" : "<some description>",
          "creation_time" : "<some date:time format>",
          "admin": "<id of a user>"
        }

        """
        team_id = json.loads(request)["id"]

        entry = Team.objects.get(team_id = team_id)
        dict = {}
        dict["name"] = entry.team_name
        dict["description"] = entry.team_description
        dict["creation_time"] = entry.creation_time.strftime('%a %d %b %Y, %I:%M%p')
        dict["admin"] = entry.admin.user_id

        return json.dumps(dict)

    # update team - passed
    def update_team(self, request: str) -> str:
        """
        :param request: A json string with the team details
        {
          "id" : "<team_id>",
          "team" : {
            "name" : "<team_name>",
            "description" : "<team_description>",
            "admin": "<id of a user>"
          }
        }

        :return:

        Constraint:
            * Team name must be unique
            * Name can be max 64 characters
            * Description can be max 128 characters
        """
        serialized = json.loads(request)
        team_id = serialized["id"]
        team_name = serialized["team"]["name"]
        team_description = serialized["team"]["description"]
        admin = serialized["team"]["admin"]
        if len(team_name) > 64 or len(team_description) > 128:
          raise Exception("Length of team_name/description is too long")
        else:
          entry = Team.objects.get(team_id = team_id)
          entry.team_name = team_name
          entry.team_description = team_description
          admin = User.objects.get(user_id = admin)
          entry.admin = admin
          entry.save()
          return "Success"

    # add users to team - passed
    def add_users_to_team(self, request: str):
        """
        :param request: A json string with the team details
        {
          "id" : "<team_id>",
          "users" : ["user_id 1", "user_id2"]
        }

        :return:

        Constraint:
        * Cap the max users that can be added to 50
        """
        serialized = json.loads(request)
        team_id = serialized["id"]
        users = serialized["users"]
        entries = UserxTeam.objects.filter(team_id = team_id)
        no_of_members = len(entries)
        spaceLeft = 50 - no_of_members
        if len(users) > spaceLeft:
          raise Exception("Users being added to the team will exceed 50 members total")
        else:
          for x in users:
            #checking if member already exists
            left = UserxTeam.objects.filter(user_id = x, team_id = team_id)
            if len(left) > 0:
               continue
            else:
               user = User.objects.get(user_id = x)
               team = Team.objects.get(team_id = team_id)
               new_entry = UserxTeam(team_id = team, user_id = user)
               new_entry.save()
           

    # remove users from team - passed
    def remove_users_from_team(self, request: str):
        """
        :param request: A json string with the team details
        {
          "id" : "<team_id>",
          "users" : ["user_id 1", "user_id2"]
        }

        :return:

        Constraint:
        * Cap the max users that can be added to 50
        """
        serialized = json.loads(request)
        team_id = serialized["id"]
        users = serialized["users"]

        team = Team.objects.get(team_id = team_id)
        for user_id in users:
           user = User.objects.get(user_id = user_id)
           UserxTeam.objects.filter(team_id = team, user_id = user).delete()

    # list users of a team - passed
    def list_team_users(self, request: str):
        """
        :param request: A json string with the team identifier
        {
          "id" : "<team_id>"
        }

        :return:
        [
          {
            "id" : "<user_id>",
            "name" : "<user_name>",
            "display_name" : "<display name>"
          }
        ]
        """
        serialized = json.loads(request)
        team_id = serialized["id"]

        users = []
        user_list = UserxTeam.objects.filter(team_id = team_id)
        for x in user_list:
           user = x.user_id
           dict = {}
           dict["id"] = user.user_id
           dict["name"] = user.user_name
           dict["display_name"] = user.display_name
           users.append(dict)

        return json.dumps(users)


