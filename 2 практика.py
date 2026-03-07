# Практическая 2.1

## Задание 1 (Анализ текстового файла)
```python
import os

def main():
    filename = "text.txt"
    lines_to_write = [
        "Первая строка текста.\n",
        "Вторая, немного более длинная строка.\n",
        "Короткая.\n",
        "Самая длинная строка в этом текстовом файле для проверки.\n",
        "Конец файла.\n"
    ]
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.writelines(lines_to_write)

    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    lines_count = len(lines)
    words_count = sum(len(line.split()) for line in lines)
    longest_line = max(lines, key=lambda x: len(x.strip())).strip()

    print(f"Количество строк: {lines_count}")
    print(f"Количество слов: {words_count}")
    print(f"Самая длинная строка: '{longest_line}'")

if __name__ == "__main__":
    main()
```

## Задание 2 (Обработка оценок студентов)
```python
import os

def main():
    input_file = "students.txt"
    output_file = "result.txt"
    
    # Создание тестового файла
    if not os.path.exists(input_file):
        with open(input_file, 'w', encoding='utf-8') as f:
            f.write("Иванов Иван:5,4,3,5\nПетров Петр:4,3,4,4\nСидорова Мария:5,5,5,5\nСмирнов Алексей:3,3,4,3\n")
            
    highest_avg = 0.0
    best_student = ""
    good_students = []

    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            if ':' not in line: continue
            name, grades_str = line.strip().split(':')
            grades = [int(g) for g in grades_str.split(',')]
            avg_grade = sum(grades) / len(grades)
            
            if avg_grade > 4.0:
                good_students.append((name, avg_grade))
                
            if avg_grade > highest_avg:
                highest_avg = avg_grade
                best_student = name

    with open(output_file, 'w', encoding='utf-8') as f:
        for name, avg in good_students:
            f.write(f"{name} - Средний балл: {avg:.2f}\n")
            
    print(f"Хорошисты сохранены в {output_file}")
    print(f"Лучший студент: {best_student} ({highest_avg:.2f})")

if __name__ == "__main__":
    main()
```

## Задание 3 (Работа с CSV)
```python
import csv
import os

FILENAME = "products.csv"

def init_file():
    if not os.path.exists(FILENAME):
        with open(FILENAME, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Название", "Цена", "Количество"])
            writer.writerows([["Яблоки", 100, 50], ["Молоко", 120, 20]])

def main():
    init_file()
    while True:
        print("\n1. Просмотр  2. Добавить  3. Поиск  4. Общая стоимость  5. Выход")
        choice = input("Действие: ")
        
        with open(FILENAME, mode='r', encoding='utf-8') as f:
            data = list(csv.DictReader(f))
            
        if choice == '1':
            for row in data: print(row)
        elif choice == '2':
            name = input("Название: ")
            price = input("Цена: ")
            qty = input("Количество: ")
            with open(FILENAME, mode='a', encoding='utf-8', newline='') as f:
                csv.writer(f).writerow([name, price, qty])
        elif choice == '3':
            q = input("Поиск: ").lower()
            for row in data:
                if q in row['Название'].lower(): print(row)
        elif choice == '4':
            total = sum(float(row['Цена']) * int(row['Количество']) for row in data)
            print(f"Общая стоимость: {total}")
        elif choice == '5':
            break

if __name__ == "__main__":
    main()
```

## Задание 4 (Калькулятор с логами)
```python
import datetime

def log_operation(record):
    with open("calculator.log", 'a', encoding='utf-8') as f:
        f.write(record + "\n")

def main():
    while True:
        num1_str = input("Введите первое число (или 'q' для выхода): ")
        if num1_str.lower() == 'q': break
        op = input("Введите операцию (+, -, *, /): ")
        num2_str = input("Введите второе число: ")

        try:
            num1, num2 = float(num1_str), float(num2_str)
            if op == '+': res = num1 + num2
            elif op == '-': res = num1 - num2
            elif op == '*': res = num1 * num2
            elif op == '/': res = num1 / num2
            else: continue
            
            print(f"Результат: {res}")
            dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_operation(f"[{dt}] {num1} {op} {num2} = {res}")
        except Exception as e:
            print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()
```

## Задание 5 (Управление библиотекой JSON)
```python
import json
import os

FILE_NAME = 'library.json'

def load_data():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_data(data):
    with open(FILE_NAME, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def main():
    books = load_data()
    while True:
        print("\n1. Просмотр  2. Поиск  3. Добавить  4. Изменить статус  5. Удалить  0. Выход")
        choice = input("Выбор: ")
        
        if choice == '1':
            for b in books: print(b)
        elif choice == '2':
            q = input("Поиск: ").lower()
            for b in books:
                if q in b['title'].lower() or q in b['author'].lower(): print(b)
        elif choice == '3':
            b_id = max([b.get('id', 0) for b in books], default=0) + 1
            books.append({"id": b_id, "title": input("Название: "), "author": input("Автор: "), "available": True})
            save_data(books)
        elif choice == '4':
            b_id = int(input("ID книги: "))
            for b in books:
                if b['id'] == b_id:
                    b['available'] = not b['available']
                    save_data(books)
        elif choice == '5':
            b_id = int(input("ID книги: "))
            books = [b for b in books if b['id'] != b_id]
            save_data(books)
        elif choice == '0':
            break

if __name__ == "__main__":
    main()
```

---

# Практическая 2.2 (Консольные скрипты)

## Задание 1 (Сетевые запросы)
```python
import urllib.request
import urllib.error

def main():
    urls = ["https://github.com/", "https://www.binance.com/en", "https://tomtit.tomsk.ru/", "https://jsonplaceholder.typicode.com/", "https://moodle.tomtit-tomsk.ru/"]
    for url in urls:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            resp = urllib.request.urlopen(req, timeout=5)
            print(f"{url} - доступен - {resp.getcode()}")
        except urllib.error.HTTPError as e:
            print(f"{url} - ошибка {e.code}")
        except Exception as e:
            print(f"{url} - недоступен")

if __name__ == "__main__":
    main()
```

## Задание 2 (Системный монитор без psutil)
```python
import subprocess
import shutil
import platform

def main():
    sys_os = platform.system()
    
    total, used, free = shutil.disk_usage("C:\\" if sys_os == "Windows" else "/")
    print(f"Диск: {(used/total)*100:.1f}%")
    
    if sys_os == "Windows":
        cpu_out = subprocess.check_output('wmic cpu get loadpercentage', shell=True).decode().split()
        if len(cpu_out) > 1: print(f"CPU: {cpu_out[1]}%")
        
        ram_out = subprocess.check_output('wmic OS get FreePhysicalMemory,TotalVisibleMemorySize', shell=True).decode().split()
        if len(ram_out) > 2:
            free_ram, total_ram = int(ram_out[1]), int(ram_out[2])
            print(f"RAM: {((total_ram-free_ram)/total_ram)*100:.1f}%")

if __name__ == "__main__":
    main()
```

## Задание 3 (Курсы валют)
```python
import urllib.request
import json
import os

SAVE_FILE = 'save.json'

def main():
    req = urllib.request.Request("https://www.cbr-xml-daily.ru/daily_json.js", headers={'User-Agent': 'Mozilla'})
    data = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))['Valute']
    
    groups = json.load(open(SAVE_FILE, 'r')) if os.path.exists(SAVE_FILE) else {}
    
    while True:
        print("\n1. Все валюты  2. Поиск  3. Создать группу  4. Группы  5. Добавить в группу  0. Выход")
        c = input("Команда: ")
        
        if c == '1':
            for code, info in data.items(): print(f"{code}: {info['Value']} руб.")
        elif c == '2':
            code = input("Код: ").upper()
            if code in data: print(f"{code}: {data[code]['Value']} руб.")
        elif c == '3':
            groups[input("Имя группы: ")] = []
            json.dump(groups, open(SAVE_FILE, 'w'))
        elif c == '4':
            print(groups)
        elif c == '5':
            g = input("Группа: ")
            if g in groups:
                groups[g].append(input("Код валюты: ").upper())
                json.dump(groups, open(SAVE_FILE, 'w'))
        elif c == '0':
            break

if __name__ == "__main__":
    main()
```

## Задание 4 (GitHub API)
```python
import urllib.request
import urllib.parse
import json

def gh_req(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Python'})
    try: return json.loads(urllib.request.urlopen(req).read().decode())
    except: return None

def main():
    while True:
        print("\n1. Профиль  2. Репозитории  3. Поиск  0. Выход")
        c = input("Команда: ")
        if c == '1':
            user = input("Ник: ")
            data = gh_req(f"https://api.github.com/users/{user}")
            if data: print(f"Имя: {data.get('name')}, Репо: {data.get('public_repos')}")
        elif c == '2':
            user = input("Ник: ")
            data = gh_req(f"https://api.github.com/users/{user}/repos")
            if data:
                for r in data: print(f"{r['name']} - {r['language']}")
        elif c == '3':
            q = urllib.parse.quote(input("Поиск: "))
            data = gh_req(f"https://api.github.com/search/repositories?q={q}")
            if data:
                for r in data['items'][:5]: print(f"{r['full_name']} - Звезд: {r['stargazers_count']}")
        elif c == '0':
            break

if __name__ == "__main__":
    main()
```

---

# Практическая 2.3

## Задание (GUI для Практической 2.2)


```python
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import urllib.request
import json

class App2_3(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Практическая 2.3")
        self.geometry("600x400")
        
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True)
        
        self.tab_currency = ttk.Frame(self.notebook)
        self.tab_github = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_currency, text="Валюты ЦБ")
        self.notebook.add(self.tab_github, text="GitHub API")
        
        self.init_currency()
        self.init_github()

    def init_currency(self):
        ttk.Button(self.tab_currency, text="Загрузить ЦБ РФ", command=self.load_curr).pack(pady=10)
        self.txt_curr = tk.Text(self.tab_currency)
        self.txt_curr.pack(fill='both', expand=True)

    def load_curr(self):
        req = urllib.request.Request("https://www.cbr-xml-daily.ru/daily_json.js", headers={'User-Agent': 'Mozilla'})
        data = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))['Valute']
        self.txt_curr.delete(1.0, tk.END)
        for c, i in data.items():
            self.txt_curr.insert(tk.END, f"{c}: {i['Value']} руб.\n")

    def init_github(self):
        frame = ttk.Frame(self.tab_github)
        frame.pack(pady=10)
        ttk.Label(frame, text="Username:").pack(side='left')
        self.gh_entry = ttk.Entry(frame)
        self.gh_entry.pack(side='left')
        ttk.Button(frame, text="Найти", command=self.load_gh).pack(side='left')
        self.txt_gh = tk.Text(self.tab_github)
        self.txt_gh.pack(fill='both', expand=True)

    def load_gh(self):
        user = self.gh_entry.get()
        req = urllib.request.Request(f"https://api.github.com/users/{user}", headers={'User-Agent': 'Python'})
        try:
            data = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
            self.txt_gh.delete(1.0, tk.END)
            self.txt_gh.insert(tk.END, f"Имя: {data.get('name')}\nРепозиториев: {data.get('public_repos')}")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

if __name__ == "__main__":
    app = App2_3()
    app.mainloop()
```

---
# Практическая 2.4
#ПОГОДА
import tkinter as tk
from tkinter import messagebox
import urllib.request
import urllib.parse
import json
import base64

# ВСТАВЬТЕ СЮДА СВОЙ КЛЮЧ ОТ OPENWEATHERMAP
API_KEY = "ВАШ_КЛЮЧ_ОТ_OPENWEATHER"

class WeatherApp(tk.Tk):
  def __init__(self):
    super().__init__()
    self.title("Метео-Станция (Задание 2.4 - Часть 1)")
    self.geometry("400x300")

    frame = tk.LabelFrame(self, text="Погода OpenWeather", font=("Arial", 12))
    frame.pack(fill='both', expand=True, padx=20, pady=20)
    
    self.city_entry = tk.Entry(frame, font=("Arial", 12))
    self.city_entry.pack(pady=10)
    self.city_entry.insert(0, "Moscow")
    
    tk.Button(frame, text="Узнать погоду", command=self.get_weather, font=("Arial", 10)).pack(pady=5)
    
    self.lbl_temp = tk.Label(frame, text="-- °C", font=("Arial", 14, "bold"))
    self.lbl_temp.pack(pady=10)
    
    self.lbl_icon = tk.Label(frame)
    self.lbl_icon.pack()

  def get_weather(self):
    city = urllib.parse.quote(self.city_entry.get())
    if API_KEY == "ТВОЙ_КЛЮЧ_ОТ_OPENWEATHER":
      messagebox.showwarning("Внимание", "Ты забыл вставить API ключ в код!")
      return
      
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=ru"
    try:
      req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
      data = json.loads(urllib.request.urlopen(req).read().decode())
      
      temp = data['main']['temp']
      desc = data['weather'][0]['description'].capitalize()
      self.lbl_temp.config(text=f"{temp} °C\n({desc})")
      
      icon = data['weather'][0]['icon']
      icon_url = f"http://openweathermap.org/img/wn/{icon}@2x.png"
      
      icon_req = urllib.request.Request(icon_url, headers={'User-Agent': 'Mozilla/5.0'})
      icon_data = urllib.request.urlopen(icon_req).read()
      
      self.img_w = tk.PhotoImage(data=base64.b64encode(icon_data))
      self.lbl_icon.config(image=self.img_w)
    except Exception as e:
      messagebox.showerror("Ошибка Погоды", str(e))

if __name__ == "__main__":
  app = WeatherApp()
  app.mainloop()
    
#ЖИВОТНЫЕ

import tkinter as tk
from tkinter import messagebox
import urllib.request
import json
import base64
import os
import sys

class AnimalsApp(tk.Tk):
  def __init__(self):
    super().__init__()
    self.title("Генератор Животных (Задание 2.4 - Часть 2)")
    self.geometry("500x500")

    frame = tk.LabelFrame(self, text="Случайные Коты и Собаки", font=("Arial", 12))
    frame.pack(fill='both', expand=True, padx=20, pady=20)
    
    btn_frame = tk.Frame(frame)
    btn_frame.pack(pady=10)
    
    tk.Button(btn_frame, text="Получить Кота (PNG)", command=self.get_cat, font=("Arial", 10)).pack(side='left', padx=10)
    tk.Button(btn_frame, text="Получить Собаку (JPG)", command=self.get_dog, font=("Arial", 10)).pack(side='left', padx=10)
    
    self.lbl_anim = tk.Label(frame, text="Нажми кнопку.\nJPG откроются во внешней программе.", font=("Arial", 10))
    self.lbl_anim.pack(expand=True)

  def get_cat(self):
    url = "https://api.thecatapi.com/v1/images/search?mime_types=png"
    try:
      req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
      img_url = json.loads(urllib.request.urlopen(req).read().decode())[0]['url']
      img_req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
      img_data = urllib.request.urlopen(img_req).read()
      
      self.img_c = tk.PhotoImage(data=base64.b64encode(img_data))
      self.lbl_anim.config(image=self.img_c, text="")
    except Exception as e:
      messagebox.showerror("Ошибка Кота", str(e))

  def get_dog(self):
    url = "https://dog.ceo/api/breeds/image/random"
    try:
      req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
      img_url = json.loads(urllib.request.urlopen(req).read().decode())['message']
      
      ext = img_url.split('.')[-1].lower()
      fname = "temp_dog." + ext
      
      urllib.request.urlretrieve(img_url, fname)
      
      if ext in ['png', 'gif']:
        self.img_d = tk.PhotoImage(file=fname)
        self.lbl_anim.config(image=self.img_d, text="")
      else:
        self.lbl_anim.config(image='', text=f"API выдало формат {ext.upper()}.\nОткрываю системным просмотрщиком...")
        if sys.platform == "win32":
          os.startfile(fname)
        elif sys.platform == "darwin":
          import subprocess
          subprocess.call(["open", fname])
        else:
          import subprocess
          subprocess.call(["xdg-open", fname])
    except Exception as e:
      messagebox.showerror("Ошибка Собаки", str(e))

if __name__ == "__main__":
  app = AnimalsApp()
  app.mainloop()
