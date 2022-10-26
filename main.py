import requests
import json
from datetime import datetime
from os import rename,path,mkdir, renames


#Парсинг json api
users = requests.get("https://json.medrating.org/users").json()
tasks = requests.get("https://json.medrating.org/todos").json()

#Создание папки, если её нет
def make_dir():
    if path.exists("tasks") != True:
        mkdir("tasks")

#Переименование файла
def rename_file(now, data):
    now = f"{now.year}-{now.month}-{now.day}T{now.hour};{now.minute}"
    if path.exists(f"tasks/{data['username']}.txt") == True:
        renames(f"tasks/{data['username']}.txt",f"tasks/old_{data['username']}_{now}.txt") 

#Наполнение файла
def filling_file(now, data):
    now = f"{now.day}.{now.month}.{now.year} {now.hour}:{now.minute}"
    with open(f"tasks/{data['username']}.txt", "w", encoding='utf=8') as file:
        file.write(f"# Отчёт для {data['company']['name']}.\n{data['name']} <{data['email']}> {now}\n")

    total_tasks  = []
    total_completed_tasks  = []
    total_not_completed_tasks  = []

    for task in tasks:
        try:
            if task['userId'] == data['id']:
                total_tasks.append(task)
                if task['completed'] == True:
                    total_completed_tasks.append(task)
                else:
                    total_not_completed_tasks.append(task)
        except: pass

    with open(f"tasks/{data['username']}.txt", "a", encoding='utf=8') as file:
        if len(total_tasks) == 0:
            file.write("У пользователя нет задач\n")
        else:
            file.write(f'Всего задач: {len(total_tasks)}\n\n## Актуальные задачи ({len(total_not_completed_tasks)}):\n')
            for not_completed_tasks in total_not_completed_tasks:
                title = not_completed_tasks['title']
                if len(title) > 46:
                    file.write(f'- {title[:46]}...\n')
                else:
                    file.write(f'- {title}\n')

            file.write(f'\n## Завершённые задачи ({len(total_completed_tasks)}):\n')
            for completed_tasks in total_completed_tasks:
                title = completed_tasks['title']
                if len(title) > 46:
                    file.write(f'- {title[:46]}...\n')
                else:
                    file.write(f'- {title}\n')

def main():
    now = datetime.now()
    make_dir()
    for i in range(len(users)):
        data = users[i]
        rename_file(now, data)
        filling_file(now, data)

if __name__ == "__main__":
    main()