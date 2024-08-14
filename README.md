# **Pygame Task Manager**
A simple and interactive task management application built with Pygame. This application allows users to create, view, edit, and delete tasks, as well as manage multiple to-do lists.

[demo](https://www.youtube.com/watch?v=3LQgge0SE9I)

## **Features**

* Create multiple to-do lists
* Add tasks with titles, descriptions, due dates, and priorities
* View all tasks in a list
* Edit existing tasks
* Delete individual tasks
* Delete entire to-do lists
* Save and load to-do lists from JSON files

## **Requirements**

* Python 3.x
* Pygame

## **Main Menu**
**The main menu offers three options:**

* Load To-Do List: Open an existing to-do list
* Create New List: Start a new to-do list
* Exit: Close the application

## **Managing Lists**

* To create a new list, select "Create New List" and enter a name for your list.
* To open an existing list, select "Load To-Do List" and choose the list you want to open.
* To delete an entire list, go to the "Load To-Do List" screen and click the "Delete" button next to the list you want to remove.

## **Managing Tasks**
**Once you've opened or created a list:**

* To add a new task, click the "Add Task" button and fill in the task details.
* To view task details, click on the task in the main list view.
* To edit a task, click the "Edit" button in the task detail view.
* To delete a task, click the "Delete" button in the task detail view.
* To mark a task as complete, use the "Complete" button (if implemented).

**Remember to click "Save Tasks" to persist your changes to the file.**
## **File Structure**

* main.py: The main script that runs the application
* task_manager.py: Contains the TaskManager class for managing tasks
* task.py: Defines the Task class
* ui_components.py: Contains classes for UI elements like buttons and input boxes
