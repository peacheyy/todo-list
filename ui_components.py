import pygame
import calendar
from datetime import date, timedelta

class InputBox:
    def __init__(self, x, y, w, h, text='', font=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.text = text
        self.initial_text = text  # Store the initial text
        self.font = font or pygame.font.Font(None, 36)
        self.txt_surface = self.font.render(text, True, pygame.Color('lightskyblue3'))
        self.active = False
        self.first_click = True  # Always true initially

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
                if self.first_click:
                    self.text = ''
                    self.first_click = False
            else:
                self.active = False
                if self.text == '':  # If the box is empty, reset to initial text
                    self.text = self.initial_text
                    self.first_click = True
            self.color = self.color_active if self.active else self.color_inactive
            self.txt_surface = self.font.render(self.text, True, pygame.Color('lightskyblue3'))
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    text = self.text
                    if text == '':  # If the box is empty, reset to initial text
                        self.text = self.initial_text
                        self.first_click = True
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, pygame.Color('lightskyblue3'))
        return None

    def update(self):
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

class Button:
    def __init__(self, x, y, w, h, text, callback, font=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = pygame.Color('lightskyblue3')
        self.text = text
        self.callback = callback
        self.font = font or pygame.font.Font(None, 24)
        self.txt_surface = self.font.render(text, True, self.color)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback()

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

class DatePicker:
    def __init__(self, x, y, w, h, font=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.font = font or pygame.font.Font(None, 24)
        self.date = date.today()
        self.txt_surface = self.font.render(self.date.strftime("%Y-%m-%d"), True, self.color)
        self.active = False
        self.expanded = False
        self.calendar_rect = pygame.Rect(x, y + h, w * 2, h * 7)  # Increased height for better visibility
        self.prev_month_rect = pygame.Rect(x, y + h, w // 2, h)
        self.next_month_rect = pygame.Rect(x + w * 1.5, y + h, w // 2, h)
        self.month_year_rect = pygame.Rect(x + w // 2, y + h, w, h)
        self.prev_year_rect = pygame.Rect(x, y + h * 2, w // 2, h // 2)
        self.next_year_rect = pygame.Rect(x + w * 1.5, y + h * 2, w // 2, h // 2)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.expanded = not self.expanded
                return True
            elif self.expanded:
                if self.calendar_rect.collidepoint(event.pos):
                    x, y = event.pos
                    if self.prev_month_rect.collidepoint(event.pos):
                        self.change_month(-1)
                        return True
                    elif self.next_month_rect.collidepoint(event.pos):
                        self.change_month(1)
                        return True
                    elif self.prev_year_rect.collidepoint(event.pos):
                        self.change_year(-1)
                        return True
                    elif self.next_year_rect.collidepoint(event.pos):
                        self.change_year(1)
                        return True
                    else:
                        day = self.get_clicked_day(x, y)
                        if day:
                            self.date = self.date.replace(day=day)
                            self.expanded = False
                            self.txt_surface = self.font.render(self.date.strftime("%Y-%m-%d"), True, self.color)
                    return True
        return False

    def change_month(self, delta):
        year = self.date.year
        month = self.date.month + delta
        if month > 12:
            month = 1
            year += 1
        elif month < 1:
            month = 12
            year -= 1
        self.date = self.date.replace(year=year, month=month, day=1)
        self.txt_surface = self.font.render(self.date.strftime("%Y-%m-%d"), True, self.color)

    def change_year(self, delta):
        year = self.date.year + delta
        if year < 1:
            year = 9999
        elif year > 9999:
            year = 1
        self.date = self.date.replace(year=year)
        self.txt_surface = self.font.render(self.date.strftime("%Y-%m-%d"), True, self.color)

    def update(self):
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)
        if self.expanded:
            self.draw_calendar(screen)

    def draw_calendar(self, screen):
        pygame.draw.rect(screen, pygame.Color('white'), self.calendar_rect)
        pygame.draw.rect(screen, self.color, self.calendar_rect, 2)
        
        cell_width = self.calendar_rect.width // 7
        cell_height = (self.calendar_rect.height - self.rect.height * 2) // 6

        # Draw month and year navigation
        pygame.draw.rect(screen, self.color_inactive, self.prev_month_rect)
        pygame.draw.rect(screen, self.color_inactive, self.next_month_rect)
        pygame.draw.rect(screen, self.color_inactive, self.month_year_rect)
        pygame.draw.rect(screen, self.color_inactive, self.prev_year_rect)
        pygame.draw.rect(screen, self.color_inactive, self.next_year_rect)
        
        prev_month_text = self.font.render("<", True, pygame.Color('black'))
        next_month_text = self.font.render(">", True, pygame.Color('black'))
        month_year_text = self.font.render(self.date.strftime("%B %Y"), True, pygame.Color('black'))
        prev_year_text = self.font.render("<<", True, pygame.Color('black'))
        next_year_text = self.font.render(">>", True, pygame.Color('black'))
        
        screen.blit(prev_month_text, (self.prev_month_rect.centerx - prev_month_text.get_width()//2, self.prev_month_rect.centery - prev_month_text.get_height()//2))
        screen.blit(next_month_text, (self.next_month_rect.centerx - next_month_text.get_width()//2, self.next_month_rect.centery - next_month_text.get_height()//2))
        screen.blit(month_year_text, (self.month_year_rect.centerx - month_year_text.get_width()//2, self.month_year_rect.centery - month_year_text.get_height()//2))
        screen.blit(prev_year_text, (self.prev_year_rect.centerx - prev_year_text.get_width()//2, self.prev_year_rect.centery - prev_year_text.get_height()//2))
        screen.blit(next_year_text, (self.next_year_rect.centerx - next_year_text.get_width()//2, self.next_year_rect.centery - next_year_text.get_height()//2))

        # Draw calendar days
        cal = calendar.monthcalendar(self.date.year, self.date.month)
        for i, week in enumerate(cal):
            for j, day in enumerate(week):
                if day != 0:
                    day_rect = pygame.Rect(self.calendar_rect.x + j * cell_width, self.calendar_rect.y + (i + 2) * cell_height, cell_width, cell_height)
                    pygame.draw.rect(screen, pygame.Color('lightgray'), day_rect)
                    pygame.draw.rect(screen, self.color, day_rect, 1)
                    text = self.font.render(str(day), True, pygame.Color('black'))
                    screen.blit(text, (day_rect.centerx - text.get_width()//2, day_rect.centery - text.get_height()//2))

    def get_clicked_day(self, x, y):
        cell_width = self.calendar_rect.width // 7
        cell_height = (self.calendar_rect.height - self.rect.height * 2) // 6
        cal = calendar.monthcalendar(self.date.year, self.date.month)
        for i, week in enumerate(cal):
            for j, day in enumerate(week):
                if day != 0:
                    day_rect = pygame.Rect(self.calendar_rect.x + j * cell_width, self.calendar_rect.y + (i + 2) * cell_height, cell_width, cell_height)
                    if day_rect.collidepoint(x, y):
                        return day
        return None
    
class Dropdown:
    def __init__(self, x, y, w, h, options, font=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.font = font or pygame.font.Font(None, 24)
        self.options = options
        self.selected = options[0]
        self.txt_surface = self.font.render(self.selected, True, pygame.Color('lightskyblue3'))
        self.active = False
        self.expanded = False
        self.option_rects = []

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.expanded = not self.expanded
                return True
            elif self.expanded:
                for i, option_rect in enumerate(self.option_rects):
                    if option_rect.collidepoint(event.pos):
                        self.selected = self.options[i]
                        self.expanded = False
                        self.txt_surface = self.font.render(self.selected, True, pygame.Color('lightskyblue3'))
                        return True
                self.expanded = False
            return False
        return False

    def update(self):
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        pygame.draw.rect(screen, pygame.Color('white'), self.rect)
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)
        if self.expanded:
            self.option_rects = []
            for i, option in enumerate(self.options):
                option_rect = pygame.Rect(self.rect.x, self.rect.y + (i+1)*self.rect.height, self.rect.width, self.rect.height)
                self.option_rects.append(option_rect)
                pygame.draw.rect(screen, pygame.Color('white'), option_rect)
                txt_surface = self.font.render(option, True, pygame.Color('lightskyblue3'))
                screen.blit(txt_surface, (option_rect.x + 5, option_rect.y + 5))
                pygame.draw.rect(screen, self.color, option_rect, 2)

    def needs_to_be_drawn_last(self):
        return self.expanded