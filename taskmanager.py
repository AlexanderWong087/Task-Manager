from datetime import datetime
import pygame
import sys
import pytz

pygame.init()
try:
    user_img = pygame.transform.scale(
        pygame.image.load('/Users/alexanderwong/Desktop/long_term/Piyush Projects/User.png'),
        (75, 100)
    )
except Exception as e:
    print("Failed to load user image:", e)
    user_img = pygame.Surface((75, 100))
    user_img.fill((80, 140, 220))

californiatimezone = pytz.timezone('America/Los_Angeles')
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Task Manager")
clock = pygame.time.Clock()

tasks = []

def st(msg, x, y, color, size=25):
    fontobj = pygame.font.SysFont(None, size)
    msgobj = fontobj.render(msg, True, color)
    text_rect = msgobj.get_rect(center=(x, y))
    screen.blit(msgobj, text_rect.topleft)
def add_tasks(task_name, due_date, description):
    tasks.append([task_name, description, due_date, 'incomplete', 'not urgent', -1])
def mark_complete(task_name):
    for task in tasks:
        if task[0] == task_name:
            task[3] = 'complete'
            task[5] = 300
            break

def save_task():
    try:
        with open('Tasks.txt', 'w') as file:
            for task in tasks:
                file.write(f"{task[0]}: {task[1]}, Status: {task[3]}, Due Date: {task[2]}\n")
        print("Tasks saved to Tasks.txt")
    except Exception as e:
        print(f"Error saving tasks: {e}")

def display_tasks(tasklist):
    today = datetime.now(californiatimezone).strftime('%Y-%m-%d')
    to_remove = []
    for task in tasklist:
        if isinstance(task[5], int) and task[5] >= 0:
            task[5] -= 1
            if task[5] <= 0:
                to_remove.append(task)
    for index, task in enumerate(tasklist):
        task_display = f"{task[0]}: {task[1]}, Status: {task[3]}, Due Date: {task[2]}"
        if task[3] == 'complete':
            color = (0, 255, 0)
        elif today == task[2]:
            color = (255, 0, 0)
        else:
            color = (255, 255, 255)
        st(task_display, 400, index * 30 + 50, color)
    for task in to_remove:
        if task in tasklist:
            tasklist.remove(task)

def take_input():
    action = input('Would you like to add a task, mark a task complete, or save your current task list? (add/complete/save) ').strip().lower()
    if action == 'add':
        name = input('Input the name of the task: ').strip()
        description = input('Input the description: ').strip()
        due_date = input('Set a due date (YYYY-MM-DD): ').strip()
        try:
            datetime.strptime(due_date, '%Y-%m-%d')
            add_tasks(name, due_date, description)
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
    elif action == 'complete':
        name = input('Input the name of the task that you want to mark complete: ').strip()
        mark_complete(name)
    elif action == 'save':
        save_task()
    else:
        print('That is not a valid action.')

class userclass:
    def __init__(self, name, password, tasks):
        self.name = name
        self.password = password
        self.tasks = tasks

    def login(self, attempt):
        global logged_in, logged_in_user
        if attempt == self.password:
            print('Successfully logged in')
            logged_in = True
            logged_in_user = self.name
        else:
            print("Incorrect Password!")

    def logout(self):
        global logged_in, logged_in_user
        logged_in = False
        logged_in_user = 'None'

    def change_password(self, new_password=None):
        old = input("Input the old password: ")
        if old == self.password:
            if new_password is None:
                new_password = input("Input the new password: ")
            self.password = new_password
            print("Password changed.")
        else:
            print("I don't think that's you, "+self.name+" ...")

def create_user(name,password):
    users.append(userclass(name,password,[]))

def logged_out_interface():
    for i in range(len(users)):
        x = 50
        y = 50 + i * 125
        screen.blit(user_img, (x, y))
        st(users[i].name, x + 37, y + 125, (255, 255, 255))

users=[userclass('Anonymous', '859762a', [])]
logged_in=False
logged_in_user='None'
frame_count=120
input_interval=300
running=True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        elif event.type==pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y=event.pos
            if 50 <= mouse_x <= 50 + 75 and 50 <= mouse_y <= 50 + 100:
                users[0].login(input('Enter password: '))

    screen.fill((0, 0, 0))
    if logged_in:
        if frame_count>=input_interval:
            take_input()
            frame_count=0
        else:
            frame_count+=1

        display_tasks(tasks)
        st(f"Logged in: {logged_in_user}", 400, 20, (200, 200, 200), size=28)
    else:
        logged_out_interface()
        st("Click the avatar to login", 400, 20, (200, 200, 200), size=28)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
