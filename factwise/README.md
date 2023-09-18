This project has been implemented in using Django. Django handles the database operations. The abstract modules have been implemented to work as intended. The functions of the modules can be called as prescribed to execute them. 

The 'factwise' folder is the app which implements the functionality which is asked. 
All of the modules are located inside a Django app called 'factwise'. When the functions inside them are called they make the neccessary changes in the Django app there itself. Please setup this app in your Django project with all of its identifiers named the same and proceed from there.

The requirements.txt has the packages and their versions with which this app was developed.

NOTES - 
1. All task titles must be unique regardless of the board. There is not a seperate table for the tasks of each board they share one table hence this constraint.
2. prettytable needs to be install through pip to run ProjectBoardBase.export_board(). It formats the tasks in a neat ascii table for viewing in a text file.