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

    load_button = Button(300, 150, 200, 50, 'Load To-Do List', load_tasks, pixel_font)
    new_button = Button(300, 250, 200, 50, 'Create New List', create_new_list, pixel_font)
    exit_button = Button(300, 350, 200, 50, 'Exit', exit_app, pixel_font)

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

    def delete_file(filename):
        try:
            os.remove(filename)
            print(f"Deleted file: {filename}")
            # Refresh the file list
            updated_files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.json')]
            if not updated_files:
                start_menu()
            else:
                file_selection_menu(updated_files, callback)
        except OSError as e:
            print(f"Error deleting file {filename}: {e}")

    # Calculate the total height of all buttons
    button_height = 50
    total_height = len(files) * (button_height + 20)  # 20px extra gap between buttons
    start_y = (600 - total_height) // 2  # Center the buttons vertically

    for i, file in enumerate(files):
        y_position = start_y + i * (button_height + 20)
        load_button = Button(200, y_position, 200, 50, file[:-5], lambda f=file: callback(f), pixel_font)
        delete_button = Button(420, y_position, 100, 50, 'Delete', lambda f=file: delete_file(f), pixel_font)
        buttons.extend([load_button, delete_button])

    back_button = Button(300, 530, 200, 50, 'Back', start_menu, pixel_font)
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
    due_date_picker = DatePicker(300, 50, 200, 50, pixel_font)
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

    add_button = Button(50, 420, 200, 50, 'Add Task', add_task, pixel_font)
    cancel_button = Button(50, 490, 200, 50, 'Cancel', cancel, pixel_font)

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
    due_date_picker = DatePicker(300, 50, 200, 50, pixel_font)
    
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

    def add_task_prompt():
        task_input_menu(manager, filename)

    def save_tasks():
        manager.save_tasks(filename)
        print(f"Tasks saved to {filename}")

    def go_back():
        start_menu()

    def view_task_details(task_index):
        task_detail_screen(manager, filename, task_index)

    add_button = Button(20, 550, 120, 32, 'Add Task', add_task_prompt, pixel_font)
    save_button = Button(150, 550, 120, 32, 'Save Tasks', save_tasks, pixel_font)
    back_button = Button(280, 550, 120, 32, 'Back', go_back, pixel_font)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            add_button.handle_event(event)
            save_button.handle_event(event)
            back_button.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, task in enumerate(manager.tasks):
                    y_pos = 30 + i * 40
                    task_button_rect = pygame.Rect(20, y_pos, 760, 32)
                    if task_button_rect.collidepoint(event.pos):
                        view_task_details(i)

        screen.fill((255, 255, 255))

        for i, task in enumerate(manager.tasks):
            y_pos = 30 + i * 40
            task_button = Button(20, y_pos, 760, 32, task.title, lambda idx=i: view_task_details(idx), pixel_font)
            task_button.draw(screen)

        add_button.draw(screen)
        save_button.draw(screen)
        back_button.draw(screen)

        pygame.display.flip()
        clock.tick(30)

def task_detail_screen(manager, filename, task_index):
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Task Details')

    pixel_font = pygame.font.Font('grand9k_pixel/grand9k_pixel.ttf', 18)
    clock = pygame.time.Clock()

    task = manager.tasks[task_index]

    def save_task():
        manager.save_tasks(filename)
        print(f"Tasks saved to {filename}")

    def edit_task():
        edit_task_menu(manager, filename, task_index)

    def delete_task():
        manager.delete_task(task_index)
        start_pygame_interface(manager, filename)

    def go_back():
        start_pygame_interface(manager, filename)

    save_button = Button(20, 550, 120, 32, 'Save', save_task, pixel_font)
    edit_button = Button(150, 550, 120, 32, 'Edit', edit_task, pixel_font)
    delete_button = Button(280, 550, 120, 32, 'Delete', delete_task, pixel_font)
    back_button = Button(410, 550, 120, 32, 'Back', go_back, pixel_font)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            save_button.handle_event(event)
            edit_button.handle_event(event)
            delete_button.handle_event(event)
            back_button.handle_event(event)

        screen.fill((255, 255, 255))

        # Display task details
        title_text = pixel_font.render(f"Title: {task.title}", True, (0, 0, 0))
        description_text = pixel_font.render(f"Description: {task.description}", True, (0, 0, 0))
        due_date_text = pixel_font.render(f"Due Date: {task.due_date}", True, (0, 0, 0))
        priority_text = pixel_font.render(f"Priority: {task.priority}", True, (0, 0, 0))
        status_text = pixel_font.render(f"Status: {'Complete' if task.complete else 'Incomplete'}", True, (0, 0, 0))

        screen.blit(title_text, (20, 30))
        screen.blit(description_text, (20, 70))
        screen.blit(due_date_text, (20, 110))
        screen.blit(priority_text, (20, 150))
        screen.blit(status_text, (20, 190))

        save_button.draw(screen)
        edit_button.draw(screen)
        delete_button.draw(screen)
        back_button.draw(screen)

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    print("Starting the application")
    start_menu()