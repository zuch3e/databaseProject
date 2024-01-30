# General DBMS into a specialized application
## Project for the Database
The initial task for the project was to build a specialized user-interface application to interact with a database that had to be designed from scratch. 
I have decided to build a general purpose DBMS (DataBase Management System) in which any simple database can be interacted with (with the rule that all tables have a non-null, self-incrementing primary key which is represented by the first column of each table). In this general part i've built a simple login/register system which takes you to a main screen.

In the main screen we can see all the tables listed as buttons that when pressed present the contents of the table in the designated space. By pressing on an entry in this table you can edit or remove said entry. To the left side of the main screen there are two buttons:
 - Add - which lets the user add an entry to table currently viewed
 - Query - which lets the user apply custom queries by writing SQL syntax.

Both the general application and the specialized one are connecting to an SQL server and requesting a database.

The specialized application is tasked with handling multiple primary keys, removing irellevant information to a general user (primary keys, general id's which describe objects) and replaced with information that the user might want to see by making use of a hash-map and custom queries ( a user might not want to see the department_id an employee belongs to, but the name of the Department ). Besides the general manipulation of irellevant information to the general user there is also another option added to execute 16 custom queries which present relevant information about the Supermarket to the user.

The main screen, the update/delete and Add windows:

<img src="/mainscreen.png" alt="main" style="height: 400px; width:800px;"/>

The queries windows:

<img src="/queries.png" alt="main" style="height: 500px; width:500px;"/>

For more in depth information about the database scheme and its contents please check the [Documentation](https://github.com/zuch3e/databaseProject/blob/main/ProiectBD(Final)_Neleptcu_Daniel_Andrei_332AB.pdf), the code for the [General Purpose Version](https://github.com/zuch3e/databaseProject/blob/main/GeneralPurposeVersion.py) and the [Specialized Version](https://github.com/zuch3e/databaseProject/blob/main/GeneralPurposeVersion.py).

For testing purposes i've also attached the backup for the [Supermarket database](https://github.com/zuch3e/databaseProject/blob/main/Supermarket.bak).
