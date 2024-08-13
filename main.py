import pygame
import sys
import os
from datetime import datetime
from task_manager import TaskManager
from ui_components import InputBox, Button, DatePicker, Dropdown

def start_menu():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Task Manager - Start Menu')

    pixel_font = pygame.font.Font('grand9k_pixel/grand9k_pixel.ttf', 18)
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

        input_box = InputBox(300, 150, 200, 50, 'Enter list name', pixel_font)
        clock = pygame.time.Clock()

        def confirm_name():
            if input_box.text:
                callback(input_box.text)

        def go_back():
            start_menu()

        confirm_button = Button(300, 250, 200, 50, 'Confirm', confirm_name, pixel_font)
        back_button = Button(300, 350, 200, 50, 'Back', go_back, pixel_font)

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

    load_button = Button(300, 200, 200, 50, 'Load To-Do List', load_tasks, pixel_font)
    new_button = Button(300, 300, 200, 50, 'Create New List', create_new_list, pixel_font)
    exit_button = Button(300, 400, 200, 50, 'Exit', exit_app, pixel_font)

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

    pixel_font = pygame.font.Font('grand9k_pixel/grand9k_pixel.ttf', 18)
    clock = pygame.time.Clock()
    buttons = []

    for i, file in enumerate(files):
        button = Button(300, 200 + i * 50, 200, 50, file[:-5], lambda f=file: callback(f), pixel_font)
        buttons.append(button)

    back_button = Button(300, 200 + len(files) * 50, 200, 50, 'Back', start_menu, pixel_font)
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

def task_input_menu(manager, filename):
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Add Task')

    pixel_font = pygame.font.Font('grand9k_pixel/grand9k_pixel.ttf', 18)
    
    title_input = InputBox(50, 50, 200, 50, 'Task Title', pixel_font)
    description_input = InputBox(50, 120, 200, 50, 'Description', pixel_font)
    due_date_picker = DatePicker(300, 50, 200, 50, pixel_font)  # Moved to right side
    priority_dropdown = Dropdown(50, 190, 200, 50, ['low', 'medium', 'high'], pixel_font)

    def add_task():
        title = title_input.text
        description = description_input.text
        due_date = due_date_picker.date.strftime("%Y-%m-%d")
        priority = priority_dropdown.selected
        if title:
            manager.add_task(title, description, due_date, priority)
            start_pygame_interface(manager, filename)

    def cancel():
        start_pygame_interface(manager, filename)

    add_button = Button(50, 260, 200, 50, 'Add Task', add_task, pixel_font)
    cancel_button = Button(50, 330, 200, 50, 'Cancel', cancel, pixel_font)

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            title_input.handle_event(event)
            description_input.handle_event(event)
            add_button.handle_event(event)
            cancel_button.handle_event(event)

            # Handle DatePicker and Dropdown events last
            if due_date_picker.handle_event(event):
                continue
            if priority_dropdown.handle_event(event):
                continue

        screen.fill((255, 255, 255))

        # Draw all elements
        title_input.draw(screen)
        description_input.draw(screen)
        add_button.draw(screen)
        cancel_button.draw(screen)

        # Draw DatePicker and Dropdown last to ensure they're on top
        due_date_picker.draw(screen)
        priority_dropdown.draw(screen)

        pygame.display.flip()
        clock.tick(30)

def edit_task_menu(manager, filename, task_index):
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Edit Task')

    pixel_font = pygame.font.Font('grand9k_pixel/grand9k_pixel.ttf', 18)
    
    task = manager.tasks[task_index]

    title_input = InputBox(50, 50, 200, 50, task.title, pixel_font)
    description_input = InputBox(50, 120, 200, 50, task.description, pixel_font)
    due_date_picker = DatePicker(300, 50, 200, 50, pixel_font)  # Moved to right side
    
    if task.due_date:
        try:
            due_date = datetime.strptime(task.due_date, "%Y-%m-%d").date()
        except ValueError:
            due_date = datetime.now().date()
    else:
        due_date = datetime.now().date()
    
    due_date_picker.date = due_date
    
    priority_dropdown = Dropdown(50, 190, 200, 50, ['low', 'medium', 'high'], pixel_font)
    priority_dropdown.selected = task.priority

    def save_task():
        title = title_input.text
        description = description_input.text
        due_date = due_date_picker.date.strftime("%Y-%m-%d")
        priority = priority_dropdown.selected
        if title:
            task.title = title
            task.description = description
            task.due_date = due_date
            task.priority = priority
            start_pygame_interface(manager, filename)

    def cancel():
        start_pygame_interface(manager, filename)

    save_button = Button(50, 260, 200, 50, 'Save Changes', save_task, pixel_font)
    cancel_button = Button(50, 330, 200, 50, 'Cancel', cancel, pixel_font)

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if priority_dropdown.handle_event(event):
                continue
            if due_date_picker.handle_event(event):
                continue

            title_input.handle_event(event)
            description_input.handle_event(event)
            save_button.handle_event(event)
            cancel_button.handle_event(event)

        screen.fill((255, 255, 255))

        # Draw all elements
        title_input.draw(screen)
        description_input.draw(screen)
        save_button.draw(screen)
        cancel_button.draw(screen)
        due_date_picker.draw(screen)

        # Draw Dropdown last to ensure it's on top
        priority_dropdown.draw(screen)

        pygame.display.flip()
        clock.tick(30)

def start_pygame_interface(manager, filename):
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Task Manager')

    pixel_font = pygame.font.Font('grand9k_pixel/grand9k_pixel.ttf', 18)
    clock = pygame.time.Clock()

    buttons = []
    ui_components = []

    def add_task_prompt():
        task_input_menu(manager, filename)

    def edit_task_prompt(task_index):
        edit_task_menu(manager, filename, task_index)

    def save_tasks():
        manager.save_tasks(filename)
        print(f"Tasks saved to {filename}")

    def go_back():
        start_menu()

    add_button = Button(20, 550, 120, 32, 'Add Task', add_task_prompt, pixel_font)
    save_button = Button(150, 550, 120, 32, 'Save Tasks', save_tasks, pixel_font)
    back_button = Button(280, 550, 120, 32, 'Back', go_back, pixel_font)

    def truncate_text(text, max_width):
        while pixel_font.size(text)[0] > max_width:
            text = text[:-1]
        return text + '...' if len(text) < len(text) else text

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            add_button.handle_event(event)
            save_button.handle_event(event)
            back_button.handle_event(event)
            for component in ui_components:
                if component.handle_event(event):
                    # If a component handles the event, bring it to the front
                    ui_components.remove(component)
                    ui_components.append(component)
                    break

        screen.fill((255, 255, 255))

        tasks = manager.tasks
        buttons = []
        ui_components = []
        for i, task in enumerate(tasks):
            y_pos = 30 + i * 60

            title = truncate_text(f"Title: {task.title}", 200)
            description = truncate_text(f"Desc: {task.description}", 200)
            due_date = truncate_text(f"Due: {task.due_date}", 150)
            priority = truncate_text(f"Priority: {task.priority}", 150)
            status = 'Complete' if task.complete else 'Incomplete'

            task_text = pixel_font.render(title, True, (0, 0, 0))
            screen.blit(task_text, (20, y_pos))
            task_text = pixel_font.render(description, True, (0, 0, 0))
            screen.blit(task_text, (20, y_pos + 20))
            task_text = pixel_font.render(due_date, True, (0, 0, 0))
            screen.blit(task_text, (250, y_pos))
            task_text = pixel_font.render(priority, True, (0, 0, 0))
            screen.blit(task_text, (250, y_pos + 20))
            task_text = pixel_font.render(status, True, (0, 0, 0))
            screen.blit(task_text, (430, y_pos))

            def mark_complete(idx=i):
                return lambda: manager.mark_task_complete(idx)

            def delete_task(idx=i):
                return lambda: manager.delete_task(idx)

            complete_button = Button(500, y_pos, 80, 25, 'Complete', mark_complete(), pixel_font)
            delete_button = Button(590, y_pos, 80, 25, 'Delete', delete_task(), pixel_font)
            edit_button = Button(680, y_pos, 80, 25, 'Edit', lambda idx=i: edit_task_prompt(idx), pixel_font)
            
            buttons.extend([complete_button, delete_button, edit_button])

            date_picker = DatePicker(250, y_pos, 150, 25, pixel_font)
            priority_dropdown = Dropdown(250, y_pos + 20, 150, 25, ['low', 'medium', 'high'], pixel_font)
            
            ui_components.extend([date_picker, priority_dropdown])

        for button in buttons:
            button.draw(screen)

        add_button.draw(screen)
        save_button.draw(screen)
        back_button.draw(screen)

        # Draw UI components in order (last is on top)
        for component in ui_components:
            component.draw(screen)

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    print("Starting the application")
    start_menu()