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

class UserBase:
    """
    Base interface implementation for API's to manage users.
    """

    # create a user
    def create_user(self, request: str) -> str:
        """
        :param request: A json string with the user details
        {
          "name" : "<user_name>",
          "display_name" : "<display name>"
        }
        :return: A json string with the response {"id" : "<user_id>"}

        Constraint:
            * user name must be unique
            * name can be max 64 characters
            * display name can be max 64 characters
        """

        dict = json.loads(request)
        name = dict["name"]
        display_name = dict["display_name"]

        entry = User(user_name = name, display_name = display_name)
        entry.save()
        obj = User.objects.get(user_name = entry.user_name)
        number = obj.user_id
        return_dict = {}
        return_dict["id"] = number
        return json.dumps(return_dict)

    # list all users
    def list_users(self) -> str:
        """
        :return: A json list with the response
        [
          {
            "name" : "<user_name>",
            "display_name" : "<display name>",
            "creation_time" : "<some date:time format>"
          }
        ]
        """
        entries = User.objects.all()
        serialized = []

        for x in entries:
          dict = {}
          dict["name"] = x.user_name
          dict["display_name"] = x.display_name
          dict["creation_time"] = x.creation_time.strftime('%a %d %b %Y, %I:%M%p')
          serialized.append(dict)

        return json.dumps(serialized)

    # describe user
    def describe_user(self, request: str) -> str:
        """
        :param request: A json string with the user details
        {
          "id" : "<user_id>"
        }

        :return: A json string with the response

        {
          "name" : "<user_name>",
          "description" : "<some description>",
          "creation_time" : "<some date:time format>"
        }

        """
        request = json.loads(request)
        entry = User.objects.get(user_id = request["id"])
        dict = {}
        dict["name"] = entry.user_name
        dict["description"] = entry.description
        dict["creation_time"] = entry.creation_time.strftime('%a %d %b %Y, %I:%M%p')
        return json.dumps(dict)

    # update user
    def update_user(self, request: str) -> str:
        """
        :param request: A json string with the user details
        {
          "id" : "<user_id>",
          "user" : {
            "name" : "<user_name>",
            "display_name" : "<display name>"
          }
        }

        :return:

        Constraint:
            * user name cannot be updated
            * name can be max 64 characters
            * display name can be max 128 characters
        """
        
        deserialized = json.loads(request)
        id = deserialized["id"]
        name = deserialized["user"]["name"]
        display_name = deserialized["user"]["display_name"]
        if len(name) > 64 or len(display_name) > 128:
          raise Exception("Error! user_name must be under 64 characters and display_name must be under 128 characters")
        else:
          entry = User.objects.get(user_id = id)
          entry.display_name = display_name
          entry.user_name = name
          entry.save()    


    def get_user_teams(self, request: str) -> str:
        """
        :param request:
        {
          "id" : "<user_id>"
        }

        :return: A json list with the response.
        [
          {
            "name" : "<team_name>",
            "description" : "<some description>",
            "creation_time" : "<some date:time format>"
          }
        ]
        """
        user_id = json.loads(request)["id"]
        user_id = User.objects.get(user_id = user_id)
        qset = UserxTeam.objects.filter(user_id = user_id)
        
        serialized = [] 
        for x in qset:
          team = x.team_id
          dict = {}
          dict["name"] = team.team_name
          dict["description"] = team.team_description
          dict["creation_time"] = team.creation_time.strftime('%a %d %b %Y, %I:%M%p')
          serialized.append(dict)
        
        return json.dumps(serialized)


