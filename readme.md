# Документация по DiskAnalyzeTool

**В папке `Python_version`, находится исходный код. В папке `Exe_version` находится исполняемый файл, приложение**

### Введение и обзор

**Асмысл?**

Данная утилита, считывать количество ГБ на системном диске C:

Это будет полезно, если вам необходимо знать, в какое время
ваше хранилище стало свободнее или забито всяким мусором, после различных чисток 
через ```C: -> Свойства -> Очистка диска``` или других любых способов.

**Что необходимо?**

Скачайте ```Python``` последней версии по ссылке: [Скачать](https://www.python.org/downloads/release/python-3135/)

### Установка модулей:

Нам понадобится всего два **модуля**:

```bash
pip install psutil
```

```bash
pip install tkinter
```

Модуль ```psutil``` осуществляет работу с диском.
Возможно его установка и не нужна так как может быть предустановлен в Python

``tkinter`` популярная и простая библиотека для создания простого пользовательского интерфейса

### Код:

Сперва, импортируем все необходимые нам модули.

```python
import datetime # Работа с временем
import psutil  # для работы с дисками
import tkinter as tk  # Используем Tkinter в качестве GUI-библиотеки
from tkinter import ttk, messagebox # Для вывода сообщений
```

Реализуем наше приложение **классом** ```DiskAnalyzerApp```:

```python
class DiskAnalyzerApp:
    def __init__(self, root):  # Конструктор класса
        self.root = root  # Создаем наше окно
        self.root.resizable(False, False)
        self.root.title("Disk Analyze Tool")  # Название для окна
        self.root.geometry("500x300")  # Размер окна
        self.setup_ui()  # Вызываем функцию-обёртку, которая будет 'красить' наше приложение (она будет ниже)
        # Автоматическое обновление информации при запуске
        self.update_disk_info()  # Обновляем информацию о диске
```

Про функции ``setup_ui()`` и ``update_disk_info()`` будет сказано ниже.

Приступаем к созданию **функции** "```setup_ui```":

```python
    def setup_ui(self):  # 'Функция обёртка'
        style = ttk.Style()  # Задаем стили
        # Задаем стили для заднег фона
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=(
            'Arial', 10))  # Задаем стили для заднего фона текста
        style.configure('TButton', font=('Arial', 10))  # Кнопка
        style.configure('Header.TLabel', font=(
            'Arial', 12, 'bold'))  # Название

        main_frame = ttk.Frame(self.root, padding="10")  # Основной фрейм
        main_frame.pack(fill=tk.BOTH, expand=True)

        header = ttk.Label(main_frame, text="Анализ диска C:",
                           style='Header.TLabel')  # Заголовок
        header.pack(pady=(0, 10))

        info_frame = ttk.Frame(main_frame)  # Фрейм с информацией о диске
        info_frame.pack(fill=tk.X, pady=5)

        self.disk_info_labels = {  # Название состояния диска
            'total': ttk.Label(info_frame, text="Всего: -"),
            'used': ttk.Label(info_frame, text="Использовано: -"),
            'free': ttk.Label(info_frame, text="Свободно: -"),
            'percent': ttk.Label(info_frame, text="Заполнено: -")
        }

        for label in self.disk_info_labels.values():  # Перебираем все состояния диска и выводим их
            label.pack(anchor=tk.W)

        self.progress = ttk.Progressbar( # Реализуем прогресс-бар
            main_frame, orient=tk.HORIZONTAL, length=400, mode='determinate')  # Прогресс-бар
        self.progress.pack(pady=10)

        button_frame = ttk.Frame(main_frame)  # Кнопки управления
        button_frame.pack(fill=tk.X, pady=10)

        ttk.Button(button_frame, text="Обновить",
                   command=self.update_disk_info).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Записать в лог",
                   command=self.write_log).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="О проекте",
                   command=self.show_notification).pack(side=tk.LEFT, padx=5)

        self.status_bar = ttk.Label( # Оформление статус бара
            main_frame, text="Готово", relief=tk.SUNKEN)  # Статус бар
        self.status_bar.pack(fill=tk.X, pady=(10, 0))
```

Следующим этапом, создаем **функцию** которая будет получать данные о диске:

```python
    def get_disk_usage(self):  # Получает информацию о диске C:
        try:  # Пробуем 'считать' диск C:
            # Переменная, в которую мы вызываем методом
            disk = psutil.disk_usage('C:')
            # psutil.disk_usage('С:'), вместо C: может быть любой другой диск
            return {  # Возвращаем словарь:
                'total': disk.total,  # Общий размер диска
                'used': disk.used,  # Используемый объём
                'free': disk.free,  # Свободное место на диске
                'percent': disk.percent  # Перевод в проценты
            }
        except Exception as e:  # Отлавилваем ошибки
            return {'error': str(e)}
```

Нам необходимо **постоянно обновлять данные** о ***диске*** при нажатии кнопки или открытия приложения:

```python
    def update_disk_info(self):  # Обновляем информацию о диске
        disk_info = self.get_disk_usage() # Создаем переменную которая сперва будет получать новые данные о диске

        if 'error' in disk_info:  # Если произошла ошибка:
            # Возвращаем ошибку
            messagebox.showerror("Ошибка", disk_info['error'])
            # И возвращаем Feedback о том что не удалось считать диск
            self.status_bar.config(
                text="Ошибка при получении информации о диске")
            return

        total_gb = disk_info['total'] / (1024 ** 3) # Обновляем информацию на экране
        used_gb = disk_info['used'] / (1024 ** 3)
        free_gb = disk_info['free'] / (1024 ** 3)

        self.disk_info_labels['total'].config(text=f"Всего: {total_gb:.2f} GB") # Оформляем вывод информации в виде текстов
        self.disk_info_labels['used'].config(
            text=f"Использовано: {used_gb:.2f} GB")
        self.disk_info_labels['free'].config(
            text=f"Свободно: {free_gb:.2f} GB")
        self.disk_info_labels['percent'].config(
            text=f"Заполнено: {disk_info['percent']}%")

        self.progress['value'] = disk_info['percent'] # Обновляем прогресс-бар

        self.current_disk_info = disk_info # Сохраняем текущую информацию для использования в других методах
        self.status_bar.config(
            text=f"Информация обновлена: {datetime.datetime.now().strftime('%H:%M:%S')}")
```

**Функция** записи **лога**:

```python
    def write_log(self):  # disk_info будет ниже
        # Записывает информацию в лог-файл
        # Если мы изначально не считали информацию о диске:
        if not hasattr(self, 'current_disk_info'):
            # То в логи записывать нечего
            messagebox.showwarning(
                "Предупреждение", "Сначала получите информацию о диске")
            return

        disk_info = self.current_disk_info  # Передаем информацию о диске
        log_file = 'storage.log'  # Создаем лог-файл
        timestamp = datetime.datetime.now().strftime(
            '%Y-%m-%d %H:%M:%S')  # Задаем временной формат

        try:
            # Сама логика логирования начинается здесь
            with open(log_file, 'a', encoding='utf-8') as f:
                # Конвертируем байты в гигабайты для удобства чтения
                total_gb = disk_info['total'] / \
                    (1024 ** 3)  # Общий размер диска
                used_gb = disk_info['used'] / (1024 ** 3)  # Используемый объём
                free_gb = disk_info['free'] / \
                    (1024 ** 3)  # Свободное место на диске

                f.write(  # Возвращаем списком всю информацию
                    f"{timestamp} - Диск C: | Всего: {total_gb:.2f} GB | "
                    f"Использовано: {used_gb:.2f} GB ({disk_info['percent']}%) | "
                    f"Свободно: {free_gb:.2f} GB\n"
                )

            # Передаем в статус бар действие: запись лога
            self.status_bar.config(text=f"Лог записан: {timestamp}")
            messagebox.showinfo(
                "Успех", "Информация успешно записана в лог-файл")
        except Exception as e:  # Если произошла ошибка:
            messagebox.showerror(
                "Ошибка", f"Не удалось записать лог: {str(e)}")
            # Обновляем статус бар с ошибкой
            self.status_bar.config(text="Ошибка при записи лога")
```

Показываем информацию **о проекте** когда пользователь нажимает на одноимённую кнопку:

```python
    def show_notification(self):  # Показываем информацию о проекте в виде уведомления
        current_version = '2.0.0'  # ТЕКУЩАЯ ВЕРСИЯ ПРОЕКТА
        info = f"Данная утлита поможет вам записывать состояние диска\nВерсия - {current_version}"
        # Показываем уведомление
        messagebox.showinfo("Информация о проекте", info)
        self.status_bar.config(text="Информация показана")
```

И наконец, **точка входа в приложение**:

```python
if __name__ == "__main__":  # Точка входа
    root = tk.Tk()
    app = DiskAnalyzerApp(root)  # Инициализируем приложение
    root.mainloop()
```

### Как использовать?

Поместите **ярлык** ```main.pyw``` в папку "Автозагрузка":

1. Нажмите Win+R, введите ```shell:startup`` и нажмите Enter
2. Перетащите ярлык в открывшуюся папку

Кнопка ```Обновить``` обновляет информацию о диске

Кнопка ```Запись в лог``` документирует текущее состояние диска, и отправляет в лог-файл

Кнопка ```О проекте``` показывает информацию о проекте

P.S:

Вы также можете просто открывать программу сколько угодно, без надобности в перемещении ярлыка
в автозагрузку, как вам удобно.

Пользуйтесь!

### Источники:

[Python](https://www.python.org/)

[psutil](https://pypi.org/project/psutil/)

[Tkinter](https://docs.python.org/3/library/tkinter.html)

[Tkinter (на русском языке)](https://metanit.com/python/tkinter/)
