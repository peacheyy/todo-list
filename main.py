import pygame
import sys
import os
from task_manager import TaskManager
from ui_components import InputBox, Button

def start_menu():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Task Manager - Start Menu')

    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()

    buttons = []

    def list_saved_files():
        files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.json')]
        return files

    def load_tasks():
        files = list_saved_files()
        if not files:
            print("No saved lists found.")
            return

        file_selection_menu(files, select_file)

    def select_file(filename):
        manager = TaskManager()
        manager.load_tasks(filename)
        start_pygame_interface(manager, filename)

    def create_new_list():
        prompt_list_name(lambda filename: start_pygame_interface(TaskManager(), filename + '.json'))

    def prompt_list_name(callback):
        screen.fill((255, 255, 255))
        pygame.display.flip()

        input_box = InputBox(300, 150, 200, 50, 'Enter list name')
        clock = pygame.time.Clock()

        def confirm_name():
            if input_box.text:
                callback(input_box.text)

        def go_back():
            start_menu()

        confirm_button = Button(300, 250, 200, 50, 'Confirm', confirm_name)
        back_button = Button(300, 350, 200, 50, 'Back', go_back)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                input_box.handle_event(event)
                confirm_button.handle_event(event)
                back_button.handle_event(event)

            screen.fill((255, 255, 255))
            input_box.update()
            input_box.draw(screen)
            confirm_button.draw(screen)
            back_button.draw(screen)

            pygame.display.flip()
            clock.tick(30)

    def exit_app():
        pygame.quit()
        sys.exit()

    load_button = Button(300, 200, 200, 50, 'Load To-Do List', load_tasks)
    new_button = Button(300, 300, 200, 50, 'Create New List', create_new_list)
    exit_button = Button(300, 400, 200, 50, 'Exit', exit_app)

    buttons = [load_button, new_button, exit_button]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for button in buttons:
                button.handle_event(event)

        screen.fill((255, 255, 255))

        for button in buttons:
            button.draw(screen)

        pygame.display.flip()
        clock.tick(30)

def file_selection_menu(files, callback):
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Task Manager - File Selection')

    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()
    buttons = []

    for i, file in enumerate(files):
        button = Button(300, 200 + i * 50, 200, 50, file[:-5], lambda f=file: callback(f))
        buttons.append(button)

    back_button = Button(300, 200 + len(files) * 50, 200, 50, 'Back', start_menu)
    buttons.append(back_button)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for button in buttons:
                button.handle_event(event)

        screen.fill((255, 255, 255))

        for button in buttons:
            button.draw(screen)

        pygame.display.flip()
        clock.tick(30)

def start_pygame_interface(manager, filename):
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Task Manager')

    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()

    buttons = []

    def add_task_prompt():
        task_input_menu(manager, filename)

    def edit_task_prompt(task_index):
        edit_task_menu(manager, filename, task_index)

    def save_tasks():
        manager.save_tasks(filename)
        print(f"Tasks saved to {filename}")

    def load_tasks():
        manager.load_tasks(filename)
        print(f"Tasks loaded from {filename}")

    def go_back():
        start_menu()

    add_button = Button(170, 550, 100, 32, 'Add Task', add_task_prompt)
    save_button = Button(300, 550, 100, 32, 'Save Tasks', save_tasks)
    load_button = Button(430, 550, 100, 32, 'Load Tasks', load_tasks)
    back_button = Button(560, 550, 100, 32, 'Back', go_back)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            add_button.handle_event(event)
            save_button.handle_event(event)
            load_button.handle_event(event)
            back_button.handle_event(event)
            for button in buttons:
                button.handle_event(event)

        screen.fill((255, 255, 255))

        tasks = manager.tasks
        buttons = []
        for i, task in enumerate(tasks):
            task_str = f"{i}. {task.title} - {'Complete' if task.complete else 'Incomplete'} - {task.description} - {task.due_date} - {task.priority}"
            task_text = font.render(task_str, True, (0, 0, 0))
            screen.blit(task_text, (20, 30 + i * 40))

            def mark_complete(idx=i):
                return lambda: manager.mark_task_complete(idx)

            def delete_task(idx=i):
                return lambda: manager.delete_task(idx)

            complete_button = Button(500, 30 + i * 40, 100, 32, 'Complete', mark_complete())
            complete_button.draw(screen)
            buttons.append(complete_button)

            delete_button = Button(610, 30 + i * 40, 100, 32, 'Delete', delete_task())
            delete_button.draw(screen)
            buttons.append(delete_button)

            edit_button = Button(720, 30 + i * 40, 100, 32, 'Edit', lambda idx=i: edit_task_prompt(idx))
            edit_button.draw(screen)
            buttons.append(edit_button)

        add_button.draw(screen)
        save_button.draw(screen)
        load_button.draw(screen)
        back_button.draw(screen)

        pygame.display.flip()
        clock.tick(30)

def task_input_menu(manager, filename):
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Add Task')

    font = pygame.font.Font(None, 36)
    input_box_title = InputBox(300, 100, 200, 50, 'Task Title')
    input_box_desc = InputBox(300, 200, 200, 50, 'Description')
    input_box_date = InputBox(300, 300, 200, 50, 'Due Date')
    input_box_priority = InputBox(300, 400, 200, 50, 'Priority (high, medium, low)')
    clock = pygame.time.Clock()

    def add_task():
        title = input_box_title.text
        description = input_box_desc.text
        due_date = input_box_date.text
        priority = input_box_priority.text
        if title:
            manager.add_task(title, description, due_date, priority)
            start_pygame_interface(manager, filename)

    def cancel():
        start_pygame_interface(manager, filename)

    add_button = Button(300, 500, 200, 50, 'Add Task', add_task)
    cancel_button = Button(300, 570, 200, 50, 'Cancel', cancel)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            input_box_title.handle_event(event)
            input_box_desc.handle_event(event)
            input_box_date.handle_event(event)
            input_box_priority.handle_event(event)

            add_button.handle_event(event)
            cancel_button.handle_event(event)

        screen.fill((255, 255, 255))

        input_box_title.update()
        input_box_desc.update()
        input_box_date.update()
        input_box_priority.update()
        input_box_title.draw(screen)
        input_box_desc.draw(screen)
        input_box_date.draw(screen)
        input_box_priority.draw(screen)
        add_button.draw(screen)
        cancel_button.draw(screen)

        pygame.display.flip()
        clock.tick(30)

def edit_task_menu(manager, filename, task_index):
    task = manager.tasks[task_index]
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Edit Task')

    font = pygame.font.Font(None, 36)
    input_box_title = InputBox(300, 150, 200, 50, task.title)
    input_box_desc = InputBox(300, 250, 200, 50, task.description)
    input_box_date = InputBox(300, 350, 200, 50, task.due_date)
    input_box_priority = InputBox(300, 450, 200, 50, task.priority)
    clock = pygame.time.Clock()

    def save_task():
        title = input_box_title.text
        description = input_box_desc.text
        due_date = input_box_date.text
        priority = input_box_priority.text
        if title:
            task.title = title
            task.description = description
            task.due_date = due_date
            task.priority = priority
            start_pygame_interface(manager, filename)

    def cancel():
        start_pygame_interface(manager, filename)

    save_button = Button(300, 520, 200, 50, 'Save', save_task)
    cancel_button = Button(300, 590, 200, 50, 'Cancel', cancel)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            input_box_title.handle_event(event)
            input_box_desc.handle_event(event)
            input_box_date.handle_event(event)
            input_box_priority.handle_event(event)

            save_button.handle_event(event)
            cancel_button.handle_event(event)

        screen.fill((255, 255, 255))

        input_box_title.update()
        input_box_desc.update()
        input_box_date.update()
        input_box_priority.update()
        input_box_title.draw(screen)
        input_box_desc.draw(screen)
        input_box_date.draw(screen)
        input_box_priority.draw(screen)
        save_button.draw(screen)
        cancel_button.draw(screen)

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    start_menu()
