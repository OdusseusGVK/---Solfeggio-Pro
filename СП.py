import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import random
import webbrowser
import winsound
import threading
import time

class SolfeggioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Сольфеджио-Про v1.0")
        self.root.geometry("1000x750")
        self.root.configure(bg='#2c3e50')
        
        # Стили для виджетов
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Настройка цветов
        self.colors = {
            'bg': '#2c3e50',
            'fg': '#ecf0f1',
            'accent': '#3498db',
            'success': '#2ecc71',
            'danger': '#e74c3c',
            'warning': '#f39c12',
            'card': '#34495e',
            'light_bg': '#ecf0f1',
            'dark_bg': '#1a252f'
        }
        
        # Настройка шрифтов
        self.fonts = {
            'title': ('Segoe UI', 24, 'bold'),
            'heading': ('Segoe UI', 16, 'bold'),
            'subheading': ('Segoe UI', 14, 'bold'),
            'normal': ('Segoe UI', 11),
            'small': ('Segoe UI', 9)
        }
        
        # Частоты для нот (в герцах)
        self.note_frequencies = {
            "До": 261.63,    # C4
            "Ре": 293.66,    # D4
            "Ми": 329.63,    # E4
            "Фа": 349.23,    # F4
            "Соль": 392.00,  # G4
            "Ля": 440.00,    # A4
            "Си": 493.88     # B4
        }
        
        # Словарь для отображения нот на русском с латинскими эквивалентами
        self.notes_dict = {
            "До": "C", "Ре": "D", "Ми": "E", 
            "Фа": "F", "Соль": "G", "Ля": "A", "Си": "B"
        }
        
        # Интервалы и их характеристики
        self.intervals = {
            "Прима (ч.1)": {"semitones": 0, "example": "До-До", "character": "Полное слияние"},
            "Малая секунда (м.2)": {"semitones": 1, "example": "До-Ре♭", "character": "Напряженно"},
            "Большая секунда (б.2)": {"semitones": 2, "example": "До-Ре", "character": "Уверенно"},
            "Малая терция (м.3)": {"semitones": 3, "example": "До-Ми♭", "character": "Грустно"},
            "Большая терция (б.3)": {"semitones": 4, "example": "До-Ми", "character": "Радостно"},
            "Чистая кварта (ч.4)": {"semitones": 5, "example": "До-Фа", "character": "Устойчиво"},
            "Тритон (ув.4/ум.5)": {"semitones": 6, "example": "До-Фа♯/Соль♭", "character": "Драматично"},
            "Чистая квинта (ч.5)": {"semitones": 7, "example": "До-Соль", "character": "Благозвучно"},
            "Малая секста (м.6)": {"semitones": 8, "example": "До-Ля♭", "character": "Лирично"},
            "Большая секста (б.6)": {"semitones": 9, "example": "До-Ля", "character": "Восторженно"},
            "Малая септима (м.7)": {"semitones": 10, "example": "До-Си♭", "character": "Напряженно"},
            "Большая септима (б.7)": {"semitones": 11, "example": "До-Си", "character": "Резко"},
            "Чистая октава (ч.8)": {"semitones": 12, "example": "До-До", "character": "Полное слияние"}
        }
        
        # Аккорды для упражнения (название, структура, описание)
        self.chords = {
            "Мажорное трезвучие": {
                "structure": "б.3 + м.3",
                "example": "До-Ми-Соль",
                "character": "Радостно, светло",
                "semitones": [0, 4, 7]
            },
            "Минорное трезвучие": {
                "structure": "м.3 + б.3",
                "example": "До-Ми♭-Соль",
                "character": "Грустно, темно",
                "semitones": [0, 3, 7]
            },
            "Увеличенное трезвучие": {
                "structure": "б.3 + б.3",
                "example": "До-Ми-Соль♯",
                "character": "Загадочно, напряженно",
                "semitones": [0, 4, 8]
            },
            "Уменьшенное трезвучие": {
                "structure": "м.3 + м.3",
                "example": "До-Ми♭-Соль♭",
                "character": "Тревожно, неустойчиво",
                "semitones": [0, 3, 6]
            },
            "Большой мажорный септаккорд": {
                "structure": "маж.трезв. + б.3",
                "example": "До-Ми-Соль-Си",
                "character": "Ярко, мечтательно",
                "semitones": [0, 4, 7, 11]
            },
            "Малый мажорный септаккорд": {
                "structure": "маж.трезв. + м.3",
                "example": "До-Ми-Соль-Си♭",
                "character": "Напряженно, ожидаемо",
                "semitones": [0, 4, 7, 10]
            },
            "Малый минорный септаккорд": {
                "structure": "мин.трезв. + м.3",
                "example": "До-Ми♭-Соль-Си♭",
                "character": "Лирично, меланхолично",
                "semitones": [0, 3, 7, 10]
            },
            "Уменьшенный септаккорд": {
                "structure": "ум.трезв. + м.3",
                "example": "До-Ми♭-Соль♭-Си♭♭",
                "character": "Тайнственно, драматично",
                "semitones": [0, 3, 6, 9]
            }
        }
        
        # Уровни сложности
        self.difficulty_levels = {
            "Начальный": ["Мажорное трезвучие", "Минорное трезвучие"],
            "Средний": ["Мажорное трезвучие", "Минорное трезвучие", 
                       "Увеличенное трезвучие", "Уменьшенное трезвучие"],
            "Продвинутый": list(self.chords.keys())
        }
        
        # Для упражнения по определению аккордов
        self.current_chord = None
        self.current_base_note = None
        self.current_difficulty = "Начальный"
        self.chord_score = 0
        self.chord_attempts = 0
        self.chord_game_active = False
        
        # Для упражнения по определению нот
        self.game_active = False
        self.score = 0
        self.total_attempts = 0
        self.current_note = None
        
        # Для упражнения по определению интервалов
        self.interval_game_active = False
        self.interval_score = 0
        self.interval_attempts = 0
        self.current_interval = None
        self.current_base_note_interval = None
        
        # Для ритмических упражнений
        self.rhythm_patterns = {
            "Начальный": [
                ("♩ ♩ ♩ ♩", "4 четверти, ровный пульс"),
                ("♩ 𝅗𝅥 ♩", "Четверть - половинная - четверть"),
                ("𝅗𝅥 ♩ ♩", "Половинная - две четверти"),
                ("♩ ♩ 𝅗𝅥", "Две четверти - половинная")
            ],
            "Средний": [
                ("♩ ♪♪ ♩ ♪♪", "Четверть - две восьмых - четверть - две восьмых"),
                ("♪♪ ♩ ♪♪ ♩", "Две восьмых - четверть - две восьмых - четверть"),
                ("♩ . ♪ ♩ ♪♪", "Четверть с точкой - восьмая - четверть - две восьмых"),
                ("♪♪ ♪♪ ♩ ♩", "Четыре восьмых - две четверти")
            ],
            "Продвинутый": [
                ("♬♬ ♪ ♩ ♪♪", "Четыре шестнадцатых - восьмая - четверть - две восьмых"),
                ("♩ ♪ ♬♬ ♪ ♩", "Четверть - восьмая - две шестнадцатых - восьмая - четверть"),
                ("♪. ♬ ♪ ♩", "Восьмая с точкой - шестнадцатая - восьмая - четверть"),
                ("♩ ♪ ♪ ♬♬ ♪", "Сложный синкопированный ритм")
            ]
        }
        self.current_rhythm_level = "Начальный"
        self.current_rhythm = None
        self.current_rhythm_explanation = None
        self.metronome_active = False
        self.metronome_tempo = 120  # BPM
        self.metronome_thread = None
        
        # Создание главного меню
        self.create_main_menu()
    
    def create_main_menu(self):
        """Создание главного меню"""
        self.clear_window()
        
        # Главный контейнер
        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Заголовок
        title_frame = tk.Frame(main_container, bg=self.colors['bg'])
        title_frame.pack(pady=(0, 30))
        
        title_label = tk.Label(title_frame, text="🎵 Сольфеджио-Про", 
                              font=self.fonts['title'], bg=self.colors['bg'], 
                              fg=self.colors['fg'])
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame, text="Обучение музыкальной грамоте", 
                                 font=self.fonts['normal'], bg=self.colors['bg'], 
                                 fg=self.colors['accent'])
        subtitle_label.pack()
        
        # Контейнер для кнопок
        buttons_container = tk.Frame(main_container, bg=self.colors['bg'])
        buttons_container.pack(pady=20, fill=tk.BOTH, expand=True)
        
        # Стиль для кнопок меню
        menu_buttons_style = {
            'font': self.fonts['subheading'],
            'width': 25,
            'height': 2,
            'bg': self.colors['accent'],
            'fg': self.colors['light_bg'],
            'activebackground': '#2980b9',
            'activeforeground': 'white',
            'relief': tk.RAISED,
            'bd': 0,
            'cursor': 'hand2'
        }
        
        # Кнопки для выбора раздела
        theory_btn = tk.Button(buttons_container, text="📚 Музыкальная теория", 
                              command=self.show_theory, **menu_buttons_style)
        theory_btn.pack(pady=15)
        
        ear_trainer_btn = tk.Button(buttons_container, text="🎧 Тренажер слуха", 
                                   command=self.show_ear_trainer, **menu_buttons_style)
        ear_trainer_btn.pack(pady=15)
        
        # Нижняя панель
        bottom_frame = tk.Frame(main_container, bg=self.colors['bg'])
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=20)
        
        # Кнопка "О программе"
        about_btn = tk.Button(bottom_frame, text="ℹ️ О программе", 
                             font=self.fonts['small'], bg=self.colors['card'], 
                             fg=self.colors['fg'], padx=15, pady=5,
                             command=self.show_about, cursor='hand2',
                             activebackground='#3d566e', activeforeground='white',
                             relief=tk.RAISED, bd=0)
        about_btn.pack(side=tk.LEFT)
        
        # Версия
        version_label = tk.Label(bottom_frame, text="v1.0", 
                                font=self.fonts['small'], bg=self.colors['bg'], 
                                fg=self.colors['accent'])
        version_label.pack(side=tk.RIGHT)
    
    def show_about(self):
        """Окно 'О программе'"""
        about_window = tk.Toplevel(self.root)
        about_window.title("О программе")
        about_window.geometry("500x600")
        about_window.configure(bg=self.colors['light_bg'])
        about_window.resizable(False, False)
        about_window.transient(self.root)
        about_window.grab_set()
        
        # Центрирование окна
        about_window.update_idletasks()
        x = (about_window.winfo_screenwidth() // 2) - (about_window.winfo_width() // 2)
        y = (about_window.winfo_screenheight() // 2) - (about_window.winfo_height() // 2)
        about_window.geometry(f"+{x}+{y}")
        
        # Содержание окна "О программе"
        content_frame = tk.Frame(about_window, bg=self.colors['light_bg'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Иконка и заголовок
        header_frame = tk.Frame(content_frame, bg=self.colors['light_bg'])
        header_frame.pack(pady=(0, 20))
        
        tk.Label(header_frame, text="🎵", font=("Arial", 40), 
                bg=self.colors['light_bg']).pack()
        
        tk.Label(header_frame, text="Сольфеджио-Про", 
                font=self.fonts['heading'], bg=self.colors['light_bg']).pack()
        
        tk.Label(header_frame, text="Версия: 1.0 (build t10e4i1)", 
                font=self.fonts['small'], bg=self.colors['light_bg'], 
                fg='#7f8c8d').pack()
        
        # Информация о программе
        info_frame = tk.Frame(content_frame, bg=self.colors['light_bg'])
        info_frame.pack(fill=tk.BOTH, expand=True)
        
        info_text = """Программа для обучения основам музыкальной грамоты 
и развития музыкального слуха.
Функции:
• Теория музыки (10 тем).
• Тренажер слуха (4 типа упражнений).
• Справочная информация.
• Статистика прогресса."""
        
        info_label = tk.Label(info_frame, text=info_text, 
                             font=self.fonts['normal'], bg=self.colors['light_bg'],
                             justify=tk.LEFT)
        info_label.pack(pady=10)
        
        # Автор
        author_frame = tk.Frame(content_frame, bg=self.colors['light_bg'])
        author_frame.pack(pady=10)
        
        tk.Label(author_frame, text="Разработчик: ", 
                font=self.fonts['normal'], bg=self.colors['light_bg']).pack(side=tk.LEFT)
        
        author_link = tk.Label(author_frame, text="OdusseusGVK", 
                              font=self.fonts['normal'], bg=self.colors['light_bg'],
                              fg=self.colors['accent'], cursor="hand2")
        author_link.pack(side=tk.LEFT)
        author_link.bind("<Button-1>", lambda e: self.open_author_link())
        
        # Кнопка закрытия
        close_btn = tk.Button(content_frame, text="Закрыть", 
                             font=self.fonts['normal'], bg=self.colors['accent'],
                             fg='white', padx=30, pady=8,
                             command=about_window.destroy,
                             cursor='hand2', relief=tk.RAISED, bd=0,
                             activebackground='#2980b9', activeforeground='white')
        close_btn.pack(pady=15)
    
    def open_author_link(self):
        """Открытие ссылки на автора"""
        webbrowser.open("https://github.com/OdusseusGVK")
    
    def show_theory(self):
        """Раздел музыкальной теории с кнопками тем"""
        self.clear_window()
        
        # Заголовок
        title_frame = tk.Frame(self.root, bg=self.colors['bg'])
        title_frame.pack(pady=(20, 10), fill=tk.X)
        
        tk.Label(title_frame, text="📚 Музыкальная теория", 
                font=self.fonts['title'], bg=self.colors['bg'], 
                fg=self.colors['fg']).pack()
        
        tk.Label(title_frame, text="Выберите тему для изучения:", 
                font=self.fonts['normal'], bg=self.colors['bg'], 
                fg=self.colors['accent']).pack()
        
        # Контейнер для кнопок тем
        topics_container = tk.Frame(self.root, bg=self.colors['bg'])
        topics_container.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)
        
        # Темы из учебника
        topics = [
            ("🎵 Основы звука", self.get_sound_basics_text),
            ("🎼 Ноты и нотный стан", self.get_notes_text),
            ("⏱️ Ритм и длительности", self.get_rhythm_text),
            ("📐 Интервалы", self.get_intervals_text),
            ("🎹 Аккорды", self.get_chords_text),
            ("🎶 Лад и тональность", self.get_modes_text),
            ("📝 Музыкальная форма", self.get_musical_form_text),
            ("🎻 Гармония", self.get_harmony_text),
            ("✍️ Музыкальный диктант", self.get_dictation_text),
            ("🎤 Сольфеджио", self.get_solfeggio_text)
        ]
        
        # Создаем кнопки для каждой темы
        for i, (topic_name, content_func) in enumerate(topics):
            btn_frame = tk.Frame(topics_container, bg=self.colors['bg'])
            btn_frame.grid(row=i//3, column=i%3, padx=10, pady=10, sticky="nsew")
            
            btn = tk.Button(btn_frame, text=topic_name, 
                          font=self.fonts['normal'], bg=self.colors['card'],
                          fg=self.colors['fg'], width=20, height=3,
                          command=lambda t=topic_name, c=content_func: self.show_topic(t, c),
                          cursor='hand2', relief=tk.RAISED, bd=0,
                          activebackground='#3d566e', activeforeground='white')
            btn.pack(fill=tk.BOTH, expand=True)
        
        # Настройка равномерного распределения колонок
        for i in range(3):
            topics_container.columnconfigure(i, weight=1)
        topics_container.rowconfigure(0, weight=1)
        topics_container.rowconfigure(1, weight=1)
        topics_container.rowconfigure(2, weight=1)
        topics_container.rowconfigure(3, weight=1)
        
        # Кнопка возврата
        back_frame = tk.Frame(self.root, bg=self.colors['bg'])
        back_frame.pack(pady=20)
        
        back_btn = tk.Button(back_frame, text="← Назад в главное меню", 
                            font=self.fonts['normal'], bg=self.colors['card'],
                            fg=self.colors['fg'], padx=20, pady=8,
                            command=self.create_main_menu, cursor='hand2',
                            relief=tk.RAISED, bd=0,
                            activebackground='#3d566e', activeforeground='white')
        back_btn.pack()
    
    def show_topic(self, topic_name, content_func):
        """Показать отдельную тему в новом окне"""
        topic_window = tk.Toplevel(self.root)
        topic_window.title(f"Музыкальная теория - {topic_name}")
        topic_window.geometry("900x700")
        topic_window.configure(bg=self.colors['light_bg'])
        topic_window.minsize(800, 600)
        
        # Заголовок темы
        header_frame = tk.Frame(topic_window, bg=self.colors['accent'])
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        
        tk.Label(header_frame, text=topic_name, 
                font=self.fonts['heading'], bg=self.colors['accent'], 
                fg='white', padx=20, pady=15).pack()
        
        # Текст темы с прокруткой
        text_frame = tk.Frame(topic_window, bg=self.colors['light_bg'])
        text_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Панель инструментов
        toolbar = tk.Frame(text_frame, bg=self.colors['light_bg'])
        toolbar.pack(fill=tk.X, padx=10, pady=10)
        
        # Кнопка копирования
        copy_btn = tk.Button(toolbar, text="📋 Копировать", 
                           font=self.fonts['small'], bg=self.colors['card'],
                           fg=self.colors['fg'], command=lambda: self.copy_to_clipboard(content_func()),
                           cursor='hand2', relief=tk.RAISED, bd=0, padx=10, pady=5,
                           activebackground='#3d566e', activeforeground='white')
        copy_btn.pack(side=tk.LEFT)
        
        # Кнопка печати
        print_btn = tk.Button(toolbar, text="🖨️ Печать", 
                            font=self.fonts['small'], bg=self.colors['card'],
                            fg=self.colors['fg'], command=lambda: self.print_content(topic_name, content_func()),
                            cursor='hand2', relief=tk.RAISED, bd=0, padx=10, pady=5,
                            activebackground='#3d566e', activeforeground='white')
        print_btn.pack(side=tk.LEFT, padx=5)
        
        # Текстовое поле
        text_container = tk.Frame(text_frame, bg=self.colors['light_bg'])
        text_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        text_widget = tk.Text(text_container, wrap=tk.WORD, font=("Segoe UI", 11), 
                             bg='white', fg='#2c3e50', padx=15, pady=15, 
                             spacing2=3, spacing3=5, relief=tk.FLAT, bd=2)
        
        scrollbar = tk.Scrollbar(text_container, command=text_widget.yview,
                                bg=self.colors['light_bg'])
        text_widget.config(yscrollcommand=scrollbar.set)
        
        # Вставляем текст
        content = content_func()
        text_widget.insert(tk.END, content)
        text_widget.config(state=tk.DISABLED)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Кнопка закрытия
        close_frame = tk.Frame(topic_window, bg=self.colors['light_bg'])
        close_frame.pack(pady=10)
        
        close_btn = tk.Button(close_frame, text="Закрыть", 
                             font=self.fonts['normal'], bg=self.colors['accent'],
                             fg='white', padx=30, pady=8,
                             command=topic_window.destroy, cursor='hand2',
                             relief=tk.RAISED, bd=0,
                             activebackground='#2980b9', activeforeground='white')
        close_btn.pack()
        
        # Центрирование окна
        topic_window.update_idletasks()
        x = (topic_window.winfo_screenwidth() // 2) - (topic_window.winfo_width() // 2)
        y = (topic_window.winfo_screenheight() // 2) - (topic_window.winfo_height() // 2)
        topic_window.geometry(f"+{x}+{y}")
    
    def copy_to_clipboard(self, text):
        """Копирование текста в буфер обмена"""
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        messagebox.showinfo("Копирование", "Текст скопирован в буфер обмена!")
    
    def print_content(self, title, content):
        """Имитация печати"""
        response = messagebox.askyesno("Печать", "Хотите сохранить текст в файл?")
        if response:
            filename = f"{title}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            messagebox.showinfo("Сохранение", f"Текст сохранен в файл: {filename}")
    
    def show_ear_trainer(self):
        """Тренажер слуха"""
        self.clear_window()
        
        # Заголовок
        title_frame = tk.Frame(self.root, bg=self.colors['bg'])
        title_frame.pack(pady=(20, 10), fill=tk.X)
        
        tk.Label(title_frame, text="🎧 Тренажер слуха", 
                font=self.fonts['title'], bg=self.colors['bg'], 
                fg=self.colors['fg']).pack()
        
        tk.Label(title_frame, text="Выберите тип упражнения:", 
                font=self.fonts['normal'], bg=self.colors['bg'], 
                fg=self.colors['accent']).pack()
        
        # Контейнер для упражнений
        exercises_container = tk.Frame(self.root, bg=self.colors['bg'])
        exercises_container.pack(fill=tk.BOTH, expand=True, padx=50, pady=30)
        
        # Упражнения
        exercises = [
            ("🎵 Определение нот", self.note_recognition_exercise),
            ("📐 Определение интервалов", self.interval_recognition_exercise),
            ("🎹 Определение аккордов", self.chord_recognition_exercise),
            ("⏱️ Ритмические упражнения", self.rhythm_exercise)
        ]
        
        for text, command in exercises:
            btn_frame = tk.Frame(exercises_container, bg=self.colors['bg'])
            btn_frame.pack(pady=10)
            
            btn = tk.Button(btn_frame, text=text, font=self.fonts['subheading'],
                          bg=self.colors['accent'], fg='white', width=30, height=2,
                          command=command, cursor='hand2', relief=tk.RAISED, bd=0,
                          activebackground='#2980b9', activeforeground='white')
            btn.pack(fill=tk.BOTH, expand=True)
        
        # Кнопка возврата
        back_frame = tk.Frame(self.root, bg=self.colors['bg'])
        back_frame.pack(pady=20)
        
        back_btn = tk.Button(back_frame, text="← Назад в главное меню", 
                            font=self.fonts['normal'], bg=self.colors['card'],
                            fg=self.colors['fg'], padx=20, pady=8,
                            command=self.create_main_menu, cursor='hand2',
                            relief=tk.RAISED, bd=0,
                            activebackground='#3d566e', activeforeground='white')
        back_btn.pack()
    
    def play_note_sound(self, note_name, duration=1000):
        """Воспроизведение звука ноты"""
        if note_name in self.note_frequencies:
            frequency = int(self.note_frequencies[note_name])
            
            # Создаем отдельный поток для воспроизведения звука
            sound_thread = threading.Thread(
                target=lambda: winsound.Beep(frequency, duration)
            )
            sound_thread.daemon = True
            sound_thread.start()
    
    def play_interval_sound(self, base_note, interval_name):
        """Воспроизведение интервала (две ноты последовательно)"""
        if interval_name in self.intervals:
            semitones = self.intervals[interval_name]["semitones"]
            
            base_freq = self.note_frequencies[base_note]
            second_freq = base_freq * (2 ** (semitones / 12))
            
            def play_sequence():
                winsound.Beep(int(base_freq), 1000)
                time.sleep(0.2)
                winsound.Beep(int(second_freq), 1000)
            
            sound_thread = threading.Thread(target=play_sequence)
            sound_thread.daemon = True
            sound_thread.start()
    
    def play_chord_sound(self, base_note, chord_name, arpeggio=True):
        """Воспроизведение аккорда"""
        if chord_name in self.chords:
            base_freq = self.note_frequencies[base_note]
            semitones = self.chords[chord_name]["semitones"]
            
            frequencies = []
            for semitone in semitones:
                freq = base_freq * (2 ** (semitone / 12))
                frequencies.append(int(freq))
            
            def play_chord():
                if arpeggio:
                    for i, freq in enumerate(frequencies):
                        duration = 500
                        winsound.Beep(freq, duration)
                        time.sleep(0.1)
                else:
                    duration = 1500
                    interval = 50
                    cycles = duration // (interval * len(frequencies))
                    for _ in range(cycles):
                        for freq in frequencies:
                            winsound.Beep(freq, interval)
                            time.sleep(0.01)
            
            sound_thread = threading.Thread(target=play_chord)
            sound_thread.daemon = True
            sound_thread.start()
    
    def show_note_reference(self):
        """Показать справочную информацию по нотам"""
        ref_window = tk.Toplevel(self.root)
        ref_window.title("Справка: Ноты и частоты")
        ref_window.geometry("500x400")
        ref_window.configure(bg=self.colors['light_bg'])
        
        # Заголовок
        header = tk.Frame(ref_window, bg=self.colors['accent'])
        header.pack(fill=tk.X)
        tk.Label(header, text="Частоты нот (первая октава)", 
                font=self.fonts['subheading'], bg=self.colors['accent'], 
                fg='white', padx=20, pady=10).pack()
        
        # Содержимое
        content = tk.Frame(ref_window, bg=self.colors['light_bg'])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Таблица частот
        table_frame = tk.Frame(content, bg='white', relief=tk.SUNKEN, bd=1)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовки таблицы
        headers = ["Нота (рус.)", "Нота (лат.)", "Частота (Гц)"]
        for col, header in enumerate(headers):
            tk.Label(table_frame, text=header, font=self.fonts['normal'], 
                    bg=self.colors['card'], fg='white', 
                    padx=10, pady=5).grid(row=0, column=col, sticky="ew", padx=1, pady=1)
        
        # Данные таблицы
        for row, (note_ru, freq) in enumerate(self.note_frequencies.items(), start=1):
            note_lat = self.notes_dict[note_ru]
            
            # Чередование цветов строк
            bg_color = '#f8f9fa' if row % 2 == 0 else 'white'
            
            tk.Label(table_frame, text=note_ru, font=self.fonts['normal'], 
                    bg=bg_color, padx=10, pady=5).grid(row=row, column=0, sticky="ew", padx=1, pady=1)
            tk.Label(table_frame, text=note_lat, font=self.fonts['normal'], 
                    bg=bg_color, padx=10, pady=5).grid(row=row, column=1, sticky="ew", padx=1, pady=1)
            tk.Label(table_frame, text=f"{freq:.2f}", font=self.fonts['normal'], 
                    bg=bg_color, padx=10, pady=5).grid(row=row, column=2, sticky="ew", padx=1, pady=1)
        
        # Настройка веса колонок
        for i in range(3):
            table_frame.columnconfigure(i, weight=1)
    
    def show_interval_reference(self):
        """Показать справочную информацию по интервалам"""
        ref_window = tk.Toplevel(self.root)
        ref_window.title("Справка: Интервалы")
        ref_window.geometry("700x500")
        ref_window.configure(bg=self.colors['light_bg'])
        
        # Заголовок
        header = tk.Frame(ref_window, bg=self.colors['accent'])
        header.pack(fill=tk.X)
        tk.Label(header, text="Характеристики интервалов", 
                font=self.fonts['subheading'], bg=self.colors['accent'], 
                fg='white', padx=20, pady=10).pack()
        
        # Содержимое
        content = tk.Frame(ref_window, bg=self.colors['light_bg'])
        content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Создаем Treeview для таблицы
        tree_frame = tk.Frame(content, bg=self.colors['light_bg'])
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        tree_scroll = tk.Scrollbar(tree_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, 
                           selectmode="extended", height=15)
        tree.pack(fill=tk.BOTH, expand=True)
        tree_scroll.config(command=tree.yview)
        
        # Определяем колонки
        tree['columns'] = ("interval", "semitones", "example", "character")
        tree.column("#0", width=0, stretch=tk.NO)
        tree.column("interval", anchor=tk.W, width=200)
        tree.column("semitones", anchor=tk.CENTER, width=100)
        tree.column("example", anchor=tk.W, width=150)
        tree.column("character", anchor=tk.W, width=250)
        
        # Заголовки
        tree.heading("#0", text="", anchor=tk.W)
        tree.heading("interval", text="Интервал", anchor=tk.W)
        tree.heading("semitones", text="Полутоны", anchor=tk.CENTER)
        tree.heading("example", text="Пример от До", anchor=tk.W)
        tree.heading("character", text="Характер звучания", anchor=tk.W)
        
        # Добавляем данные
        for interval_name, info in self.intervals.items():
            tree.insert("", tk.END, values=(
                interval_name,
                info["semitones"],
                info["example"],
                info["character"]
            ))
        
        # Стиль для четных/нечетных строк
        style = ttk.Style()
        style.configure("Treeview", 
                       background=self.colors['light_bg'],
                       foreground='black',
                       rowheight=25,
                       fieldbackground=self.colors['light_bg'])
        style.map('Treeview', background=[('selected', self.colors['accent'])])
    
    def show_chord_reference(self):
        """Показать справочную информацию по аккордам"""
        ref_window = tk.Toplevel(self.root)
        ref_window.title("Справка: Аккорды")
        ref_window.geometry("800x500")
        ref_window.configure(bg=self.colors['light_bg'])
        
        # Заголовок
        header = tk.Frame(ref_window, bg=self.colors['accent'])
        header.pack(fill=tk.X)
        tk.Label(header, text="Характеристики аккордов", 
                font=self.fonts['subheading'], bg=self.colors['accent'], 
                fg='white', padx=20, pady=10).pack()
        
        # Содержимое
        content = tk.Frame(ref_window, bg=self.colors['light_bg'])
        content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Создаем Treeview для таблицы
        tree_frame = tk.Frame(content, bg=self.colors['light_bg'])
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        tree_scroll = tk.Scrollbar(tree_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, 
                           selectmode="extended", height=15)
        tree.pack(fill=tk.BOTH, expand=True)
        tree_scroll.config(command=tree.yview)
        
        # Определяем колонки
        tree['columns'] = ("chord", "structure", "example", "character")
        tree.column("#0", width=0, stretch=tk.NO)
        tree.column("chord", anchor=tk.W, width=250)
        tree.column("structure", anchor=tk.W, width=150)
        tree.column("example", anchor=tk.W, width=200)
        tree.column("character", anchor=tk.W, width=200)
        
        # Заголовки
        tree.heading("#0", text="", anchor=tk.W)
        tree.heading("chord", text="Аккорд", anchor=tk.W)
        tree.heading("structure", text="Структура", anchor=tk.W)
        tree.heading("example", text="Пример от До", anchor=tk.W)
        tree.heading("character", text="Характер звучания", anchor=tk.W)
        
        # Добавляем данные
        for chord_name, info in self.chords.items():
            tree.insert("", tk.END, values=(
                chord_name,
                info["structure"],
                info["example"],
                info["character"]
            ))
        
        # Стиль
        style = ttk.Style()
        style.configure("Treeview", 
                       background=self.colors['light_bg'],
                       foreground='black',
                       rowheight=25,
                       fieldbackground=self.colors['light_bg'])
        style.map('Treeview', background=[('selected', self.colors['accent'])])
    
    def note_recognition_exercise(self):
        """Упражнение на распознавание нот"""
        self.clear_window()
        
        # Главный контейнер
        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Заголовок
        header_frame = tk.Frame(main_container, bg=self.colors['bg'])
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(header_frame, text="🎵 Определение нот", 
                font=self.fonts['title'], bg=self.colors['bg'], 
                fg=self.colors['fg']).pack()
        
        # Описание
        desc_frame = tk.Frame(main_container, bg=self.colors['card'], 
                             relief=tk.RAISED, bd=1)
        desc_frame.pack(fill=tk.X, pady=(0, 20), padx=10)
        
        desc_text = """Слушайте звучащую ноту и выбирайте соответствующую ноту из списка.
        Ноты представлены в диапазоне первой октавы."""
        
        tk.Label(desc_frame, text=desc_text, font=self.fonts['normal'], 
                bg=self.colors['card'], fg=self.colors['fg'], 
                wraplength=600, justify=tk.LEFT, padx=15, pady=10).pack()
        
        # Панель управления
        control_frame = tk.Frame(main_container, bg=self.colors['bg'])
        control_frame.pack(fill=tk.X, pady=20)
        
        # Кнопка справки
        help_btn = tk.Button(control_frame, text="📖 Справка по нотам", 
                           font=self.fonts['small'], bg=self.colors['card'],
                           fg=self.colors['fg'], command=self.show_note_reference,
                           cursor='hand2', relief=tk.RAISED, bd=0, padx=15, pady=8,
                           activebackground='#3d566e', activeforeground='white')
        help_btn.pack(side=tk.LEFT, padx=5)
        
        # Кнопка для проигрывания ноты
        self.play_button = tk.Button(control_frame, text="🎵 Проиграть ноту", 
                                    font=self.fonts['normal'], bg=self.colors['accent'],
                                    fg='white', width=15, height=1,
                                    command=lambda: self.play_note_sound(self.current_note),
                                    cursor='hand2', relief=tk.RAISED, bd=0,
                                    activebackground='#2980b9', activeforeground='white')
        self.play_button.pack(side=tk.LEFT, padx=5)
        self.play_button.config(state=tk.DISABLED)
        
        # Кнопки управления
        start_btn = tk.Button(control_frame, text="▶ Начать упражнение", 
                             font=self.fonts['normal'], bg=self.colors['success'],
                             fg='white', width=15, height=1,
                             command=self.start_exercise, cursor='hand2',
                             relief=tk.RAISED, bd=0,
                             activebackground='#27ae60', activeforeground='white')
        start_btn.pack(side=tk.LEFT, padx=5)
        
        stop_btn = tk.Button(control_frame, text="■ Остановить", 
                            font=self.fonts['normal'], bg=self.colors['danger'],
                            fg='white', width=15, height=1,
                            command=self.stop_exercise, cursor='hand2',
                            relief=tk.RAISED, bd=0,
                            activebackground='#c0392b', activeforeground='white')
        stop_btn.pack(side=tk.LEFT, padx=5)
        
        # Результат
        self.result_label = tk.Label(main_container, text="Нажмите 'Начать упражнение'", 
                                    font=self.fonts['subheading'], bg=self.colors['bg'], 
                                    fg=self.colors['accent'], pady=10)
        self.result_label.pack()
        
        # Статистика
        stats_frame = tk.Frame(main_container, bg=self.colors['card'], 
                              relief=tk.SUNKEN, bd=1)
        stats_frame.pack(pady=10, padx=50, fill=tk.X)
        
        self.stats_label = tk.Label(stats_frame, text="Правильно: 0/0 (0%)", 
                                   font=self.fonts['normal'], bg=self.colors['card'], 
                                   fg=self.colors['fg'], padx=20, pady=10)
        self.stats_label.pack()
        
        # Кнопки с нотами
        notes_frame = tk.Frame(main_container, bg=self.colors['bg'])
        notes_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        notes = list(self.note_frequencies.keys())
        
        # Создаем кнопки в сетке 2x4
        for i, note in enumerate(notes):
            row = i // 4
            col = i % 4
            
            btn_frame = tk.Frame(notes_frame, bg=self.colors['bg'])
            btn_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            
            btn_text = f"{note}\n({self.notes_dict[note]})"
            btn = tk.Button(btn_frame, text=btn_text, 
                          font=self.fonts['heading'], bg=self.colors['card'],
                          fg=self.colors['fg'], width=8, height=3,
                          command=lambda n=note: self.check_note_answer(n),
                          cursor='hand2', relief=tk.RAISED, bd=0,
                          activebackground='#3d566e', activeforeground='white')
            btn.pack(fill=tk.BOTH, expand=True)
        
        # Настройка сетки
        for i in range(2):
            notes_frame.rowconfigure(i, weight=1)
        for i in range(4):
            notes_frame.columnconfigure(i, weight=1)
        
        # Панель навигации
        nav_frame = tk.Frame(main_container, bg=self.colors['bg'])
        nav_frame.pack(fill=tk.X, pady=20)
        
        back_btn = tk.Button(nav_frame, text="← Назад к выбору", 
                            font=self.fonts['normal'], bg=self.colors['card'],
                            fg=self.colors['fg'], padx=20, pady=8,
                            command=self.show_ear_trainer, cursor='hand2',
                            relief=tk.RAISED, bd=0,
                            activebackground='#3d566e', activeforeground='white')
        back_btn.pack(side=tk.LEFT, padx=5)
        
        home_btn = tk.Button(nav_frame, text="🏠 Главное меню", 
                           font=self.fonts['normal'], bg=self.colors['card'],
                           fg=self.colors['fg'], padx=20, pady=8,
                           command=self.create_main_menu, cursor='hand2',
                           relief=tk.RAISED, bd=0,
                           activebackground='#3d566e', activeforeground='white')
        home_btn.pack(side=tk.LEFT, padx=5)
        
        # Инициализация состояния упражнения
        self.game_active = False
        self.current_note = None
    
    def generate_random_note(self):
        """Генерация случайной ноты"""
        notes = list(self.note_frequencies.keys())
        return random.choice(notes)
    
    def check_note_answer(self, selected_note):
        """Проверка ответа в упражнении по определению нот"""
        if not self.game_active or self.current_note is None:
            return
        
        self.total_attempts += 1
        
        if selected_note == self.current_note:
            self.score += 1
            self.result_label.config(text="✓ Правильно!", fg=self.colors['success'])
            threading.Thread(
                target=lambda: winsound.Beep(800, 300)
            ).start()
        else:
            self.result_label.config(
                text=f"✗ Неправильно! Правильный ответ: {self.current_note} ({self.notes_dict[self.current_note]})", 
                fg=self.colors['danger']
            )
            threading.Thread(
                target=lambda: winsound.Beep(400, 500)
            ).start()
        
        self.update_statistics()
        self.root.after(1500, self.next_round)
    
    def next_round(self):
        """Начало следующего раунда"""
        if self.game_active:
            self.current_note = self.generate_random_note()
            self.result_label.config(text="Слушайте ноту...", fg=self.colors['accent'])
            self.play_button.config(state=tk.NORMAL)
    
    def update_statistics(self):
        """Обновление статистики"""
        if self.total_attempts > 0:
            accuracy = (self.score / self.total_attempts) * 100
            self.stats_label.config(
                text=f"Правильно: {self.score}/{self.total_attempts} ({accuracy:.1f}%)"
            )
    
    def start_exercise(self):
        """Начало упражнения"""
        self.game_active = True
        self.score = 0
        self.total_attempts = 0
        self.update_statistics()
        self.next_round()
    
    def stop_exercise(self):
        """Остановка упражнения"""
        self.game_active = False
        self.result_label.config(text="Упражнение остановлено", fg=self.colors['warning'])
        self.play_button.config(state=tk.DISABLED)
    
    def interval_recognition_exercise(self):
        """Упражнение на распознавание интервалов"""
        self.clear_window()
        
        # Главный контейнер
        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Заголовок
        header_frame = tk.Frame(main_container, bg=self.colors['bg'])
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(header_frame, text="📐 Определение интервалов", 
                font=self.fonts['title'], bg=self.colors['bg'], 
                fg=self.colors['fg']).pack()
        
        # Описание
        desc_frame = tk.Frame(main_container, bg=self.colors['card'], 
                             relief=tk.RAISED, bd=1)
        desc_frame.pack(fill=tk.X, pady=(0, 20), padx=10)
        
        desc_text = """Слушайте звучащий интервал и выбирайте соответствующий интервал из списка.
        Интервалы представлены от примы до октавы."""
        
        tk.Label(desc_frame, text=desc_text, font=self.fonts['normal'], 
                bg=self.colors['card'], fg=self.colors['fg'], 
                wraplength=600, justify=tk.LEFT, padx=15, pady=10).pack()
        
        # Панель управления
        control_frame = tk.Frame(main_container, bg=self.colors['bg'])
        control_frame.pack(fill=tk.X, pady=20)
        
        # Кнопка справки
        help_btn = tk.Button(control_frame, text="📖 Справка по интервалам", 
                           font=self.fonts['small'], bg=self.colors['card'],
                           fg=self.colors['fg'], command=self.show_interval_reference,
                           cursor='hand2', relief=tk.RAISED, bd=0, padx=15, pady=8,
                           activebackground='#3d566e', activeforeground='white')
        help_btn.pack(side=tk.LEFT, padx=5)
        
        # Кнопка для проигрывания интервала
        self.interval_play_button = tk.Button(control_frame, text="🎵 Проиграть интервал", 
                                             font=self.fonts['normal'], bg=self.colors['accent'],
                                             fg='white', width=18, height=1,
                                             command=lambda: self.play_interval_sound(
                                                 self.current_base_note_interval, self.current_interval),
                                             cursor='hand2', relief=tk.RAISED, bd=0,
                                             activebackground='#2980b9', activeforeground='white')
        self.interval_play_button.pack(side=tk.LEFT, padx=5)
        self.interval_play_button.config(state=tk.DISABLED)
        
        # Кнопки управления
        start_btn = tk.Button(control_frame, text="▶ Начать упражнение", 
                             font=self.fonts['normal'], bg=self.colors['success'],
                             fg='white', width=18, height=1,
                             command=self.start_interval_exercise, cursor='hand2',
                             relief=tk.RAISED, bd=0,
                             activebackground='#27ae60', activeforeground='white')
        start_btn.pack(side=tk.LEFT, padx=5)
        
        stop_btn = tk.Button(control_frame, text="■ Остановить", 
                            font=self.fonts['normal'], bg=self.colors['danger'],
                            fg='white', width=18, height=1,
                            command=self.stop_interval_exercise, cursor='hand2',
                            relief=tk.RAISED, bd=0,
                            activebackground='#c0392b', activeforeground='white')
        stop_btn.pack(side=tk.LEFT, padx=5)
        
        # Результат
        self.interval_result_label = tk.Label(main_container, 
                                             text="Нажмите 'Начать упражнение'", 
                                             font=self.fonts['subheading'], bg=self.colors['bg'], 
                                             fg=self.colors['accent'], pady=10)
        self.interval_result_label.pack()
        
        # Статистика
        stats_frame = tk.Frame(main_container, bg=self.colors['card'], 
                              relief=tk.SUNKEN, bd=1)
        stats_frame.pack(pady=10, padx=50, fill=tk.X)
        
        self.interval_stats_label = tk.Label(stats_frame, text="Правильно: 0/0 (0%)", 
                                            font=self.fonts['normal'], bg=self.colors['card'], 
                                            fg=self.colors['fg'], padx=20, pady=10)
        self.interval_stats_label.pack()
        
        # Кнопки с интервалами
        intervals_frame = tk.Frame(main_container, bg=self.colors['bg'])
        intervals_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        interval_names = list(self.intervals.keys())
        
        # Создаем кнопки в сетке 4x4
        for i, interval in enumerate(interval_names):
            row = i // 4
            col = i % 4
            
            btn_frame = tk.Frame(intervals_frame, bg=self.colors['bg'])
            btn_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            
            btn = tk.Button(btn_frame, text=interval, 
                          font=self.fonts['normal'], bg=self.colors['card'],
                          fg=self.colors['fg'], width=15, height=2,
                          command=lambda i=interval: self.check_interval_answer(i),
                          cursor='hand2', relief=tk.RAISED, bd=0,
                          activebackground='#3d566e', activeforeground='white',
                          wraplength=150)
            btn.pack(fill=tk.BOTH, expand=True)
        
        # Настройка сетки
        for i in range(4):
            intervals_frame.rowconfigure(i, weight=1)
        for i in range(4):
            intervals_frame.columnconfigure(i, weight=1)
        
        # Панель навигации
        nav_frame = tk.Frame(main_container, bg=self.colors['bg'])
        nav_frame.pack(fill=tk.X, pady=20)
        
        back_btn = tk.Button(nav_frame, text="← Назад к выбору", 
                            font=self.fonts['normal'], bg=self.colors['card'],
                            fg=self.colors['fg'], padx=20, pady=8,
                            command=self.show_ear_trainer, cursor='hand2',
                            relief=tk.RAISED, bd=0,
                            activebackground='#3d566e', activeforeground='white')
        back_btn.pack(side=tk.LEFT, padx=5)
        
        home_btn = tk.Button(nav_frame, text="🏠 Главное меню", 
                           font=self.fonts['normal'], bg=self.colors['card'],
                           fg=self.colors['fg'], padx=20, pady=8,
                           command=self.create_main_menu, cursor='hand2',
                           relief=tk.RAISED, bd=0,
                           activebackground='#3d566e', activeforeground='white')
        home_btn.pack(side=tk.LEFT, padx=5)
        
        # Инициализация состояния упражнения
        self.interval_game_active = False
        self.current_interval = None
        self.current_base_note_interval = None
        
    def generate_random_interval(self):
        """Генерация случайного интервала"""
        intervals = list(self.intervals.keys())
        base_note = random.choice(list(self.note_frequencies.keys()))
        return random.choice(intervals), base_note
    
    def check_interval_answer(self, selected_interval):
        """Проверка ответа в упражнении по определению интервалов"""
        if not self.interval_game_active or self.current_interval is None:
            return
        
        self.interval_attempts += 1
        
        if selected_interval == self.current_interval:
            self.interval_score += 1
            self.interval_result_label.config(text="✓ Правильно!", fg=self.colors['success'])
            threading.Thread(
                target=lambda: winsound.Beep(800, 300)
            ).start()
        else:
            interval_info = self.intervals[self.current_interval]
            self.interval_result_label.config(
                text=f"✗ Неправильно! Правильный ответ: {self.current_interval}\n"
                     f"Пример: {interval_info['example']}\n"
                     f"Характер: {interval_info['character']}", 
                fg=self.colors['danger']
            )
            threading.Thread(
                target=lambda: winsound.Beep(400, 500)
            ).start()
        
        self.update_interval_statistics()
        self.root.after(2000, self.next_interval_round)
    
    def next_interval_round(self):
        """Начало следующего раунда в упражнении с интервалами"""
        if self.interval_game_active:
            self.current_interval, self.current_base_note_interval = self.generate_random_interval()
            self.interval_result_label.config(text="Слушайте интервал...", fg=self.colors['accent'])
            self.interval_play_button.config(state=tk.NORMAL)
    
    def update_interval_statistics(self):
        """Обновление статистики для упражнения с интервалами"""
        if self.interval_attempts > 0:
            accuracy = (self.interval_score / self.interval_attempts) * 100
            self.interval_stats_label.config(
                text=f"Правильно: {self.interval_score}/{self.interval_attempts} ({accuracy:.1f}%)"
            )
    
    def start_interval_exercise(self):
        """Начало упражнения с интервалами"""
        self.interval_game_active = True
        self.interval_score = 0
        self.interval_attempts = 0
        self.update_interval_statistics()
        self.next_interval_round()
    
    def stop_interval_exercise(self):
        """Остановка упражнения с интервалами"""
        self.interval_game_active = False
        self.interval_result_label.config(text="Упражнение остановлено", fg=self.colors['warning'])
        self.interval_play_button.config(state=tk.DISABLED)
    
    def generate_random_chord(self, difficulty=None):
        """Генерация случайного аккорда"""
        if difficulty is None:
            difficulty = self.current_difficulty
        
        available_chords = self.difficulty_levels[difficulty]
        chord_name = random.choice(available_chords)
        base_note = random.choice(list(self.note_frequencies.keys()))
        
        return chord_name, base_note
    
    def check_chord_answer(self, selected_chord):
        """Проверка ответа в упражнении по определению аккордов"""
        if not self.chord_game_active or self.current_chord is None:
            return
        
        self.chord_attempts += 1
        
        if selected_chord == self.current_chord:
            self.chord_score += 1
            self.chord_result_label.config(text="✓ Правильно!", fg=self.colors['success'])
            threading.Thread(
                target=lambda: winsound.Beep(800, 300)
            ).start()
        else:
            chord_info = self.chords[self.current_chord]
            self.chord_result_label.config(
                text=f"✗ Неправильно! Правильный ответ: {self.current_chord}\n"
                     f"Структура: {chord_info['structure']}\n"
                     f"Характер: {chord_info['character']}", 
                fg=self.colors['danger']
            )
            threading.Thread(
                target=lambda: winsound.Beep(400, 500)
            ).start()
        
        self.update_chord_statistics()
        self.root.after(2000, self.next_chord_round)
    
    def next_chord_round(self):
        """Начало следующего раунда в упражнении с аккордами"""
        if self.chord_game_active:
            self.current_chord, self.current_base_note = self.generate_random_chord()
            self.chord_result_label.config(text="Слушайте аккорд...", fg=self.colors['accent'])
            self.chord_play_button.config(state=tk.NORMAL)
    
    def update_chord_statistics(self):
        """Обновление статистики для упражнения с аккордами"""
        if self.chord_attempts > 0:
            accuracy = (self.chord_score / self.chord_attempts) * 100
            self.chord_stats_label.config(
                text=f"Правильно: {self.chord_score}/{self.chord_attempts} ({accuracy:.1f}%)"
            )
    
    def start_chord_exercise(self):
        """Начало упражнения с аккордами"""
        self.chord_game_active = True
        self.chord_score = 0
        self.chord_attempts = 0
        self.update_chord_statistics()
        self.next_chord_round()
    
    def stop_chord_exercise(self):
        """Остановка упражнения с аккордами"""
        self.chord_game_active = False
        self.chord_result_label.config(text="Упражнение остановлено", fg=self.colors['warning'])
        self.chord_play_button.config(state=tk.DISABLED)
    
    def set_difficulty(self, difficulty):
        """Установка уровня сложности"""
        self.current_difficulty = difficulty
        difficulty_text = f"Текущий уровень: {difficulty}"
        self.difficulty_label.config(text=difficulty_text)
        
        if self.chord_game_active:
            self.next_chord_round()
    
    def chord_recognition_exercise(self):
        """Упражнение на распознавание аккордов"""
        self.clear_window()
        
        # Главный контейнер
        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Заголовок
        header_frame = tk.Frame(main_container, bg=self.colors['bg'])
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(header_frame, text="🎹 Определение аккордов", 
                font=self.fonts['title'], bg=self.colors['bg'], 
                fg=self.colors['fg']).pack()
        
        # Описание
        desc_frame = tk.Frame(main_container, bg=self.colors['card'], 
                             relief=tk.RAISED, bd=1)
        desc_frame.pack(fill=tk.X, pady=(0, 20), padx=10)
        
        desc_text = """Слушайте звучащий аккорд и определяйте его тип.
        Аккорды представлены в основном виде от различных базовых нот.
        Уровень сложности определяет, какие типы аккордов будут использоваться."""
        
        tk.Label(desc_frame, text=desc_text, font=self.fonts['normal'], 
                bg=self.colors['card'], fg=self.colors['fg'], 
                wraplength=600, justify=tk.LEFT, padx=15, pady=10).pack()
        
        # Уровень сложности
        difficulty_frame = tk.Frame(main_container, bg=self.colors['bg'])
        difficulty_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(difficulty_frame, text="Уровень сложности:", 
                font=self.fonts['normal'], bg=self.colors['bg'], 
                fg=self.colors['fg']).pack(side=tk.LEFT, padx=5)
        
        difficulties = ["Начальный", "Средний", "Продвинутый"]
        for diff in difficulties:
            btn = tk.Button(difficulty_frame, text=diff, font=self.fonts['small'],
                          command=lambda d=diff: self.set_difficulty(d),
                          bg=self.colors['card'], fg=self.colors['fg'],
                          cursor='hand2', relief=tk.RAISED, bd=0, padx=10, pady=5,
                          activebackground='#3d566e', activeforeground='white')
            btn.pack(side=tk.LEFT, padx=2)
        
        # Метка текущего уровня сложности
        self.difficulty_label = tk.Label(main_container, 
                                        text=f"Текущий уровень: {self.current_difficulty}",
                                        font=self.fonts['normal'], bg=self.colors['bg'], 
                                        fg=self.colors['accent'])
        self.difficulty_label.pack(pady=5)
        
        # Панель управления
        control_frame = tk.Frame(main_container, bg=self.colors['bg'])
        control_frame.pack(fill=tk.X, pady=20)
        
        # Кнопка справки
        help_btn = tk.Button(control_frame, text="📖 Справка по аккордам", 
                           font=self.fonts['small'], bg=self.colors['card'],
                           fg=self.colors['fg'], command=self.show_chord_reference,
                           cursor='hand2', relief=tk.RAISED, bd=0, padx=15, pady=8,
                           activebackground='#3d566e', activeforeground='white')
        help_btn.pack(side=tk.LEFT, padx=5)
        
        # Кнопка для проигрывания аккорда
        self.chord_play_button = tk.Button(control_frame, text="🎵 Проиграть аккорд", 
                                          font=self.fonts['normal'], bg=self.colors['accent'],
                                          fg='white', width=18, height=1,
                                          command=lambda: self.play_chord_sound(
                                              self.current_base_note, self.current_chord),
                                          cursor='hand2', relief=tk.RAISED, bd=0,
                                          activebackground='#2980b9', activeforeground='white')
        self.chord_play_button.pack(side=tk.LEFT, padx=5)
        self.chord_play_button.config(state=tk.DISABLED)
        
        # Кнопки управления
        start_btn = tk.Button(control_frame, text="▶ Начать упражнение", 
                             font=self.fonts['normal'], bg=self.colors['success'],
                             fg='white', width=18, height=1,
                             command=self.start_chord_exercise, cursor='hand2',
                             relief=tk.RAISED, bd=0,
                             activebackground='#27ae60', activeforeground='white')
        start_btn.pack(side=tk.LEFT, padx=5)
        
        stop_btn = tk.Button(control_frame, text="■ Остановить", 
                            font=self.fonts['normal'], bg=self.colors['danger'],
                            fg='white', width=18, height=1,
                            command=self.stop_chord_exercise, cursor='hand2',
                            relief=tk.RAISED, bd=0,
                            activebackground='#c0392b', activeforeground='white')
        stop_btn.pack(side=tk.LEFT, padx=5)
        
        # Результат
        self.chord_result_label = tk.Label(main_container, text="Нажмите 'Начать упражнение'", 
                                          font=self.fonts['subheading'], bg=self.colors['bg'], 
                                          fg=self.colors['accent'], pady=10)
        self.chord_result_label.pack()
        
        # Статистика
        stats_frame = tk.Frame(main_container, bg=self.colors['card'], 
                              relief=tk.SUNKEN, bd=1)
        stats_frame.pack(pady=10, padx=50, fill=tk.X)
        
        self.chord_stats_label = tk.Label(stats_frame, text="Правильно: 0/0 (0%)", 
                                         font=self.fonts['normal'], bg=self.colors['card'], 
                                         fg=self.colors['fg'], padx=20, pady=10)
        self.chord_stats_label.pack()
        
        # Кнопки с аккордами
        chords_frame = tk.Frame(main_container, bg=self.colors['bg'])
        chords_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        chord_names = list(self.chords.keys())
        
        # Создаем кнопки в сетке 4x2
        for i, chord in enumerate(chord_names):
            row = i // 2
            col = i % 2
            
            btn_frame = tk.Frame(chords_frame, bg=self.colors['bg'])
            btn_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            
            btn = tk.Button(btn_frame, text=chord, 
                          font=self.fonts['normal'], bg=self.colors['card'],
                          fg=self.colors['fg'], width=25, height=2,
                          command=lambda c=chord: self.check_chord_answer(c),
                          cursor='hand2', relief=tk.RAISED, bd=0,
                          activebackground='#3d566e', activeforeground='white',
                          wraplength=200)
            btn.pack(fill=tk.BOTH, expand=True)
        
        # Настройка сетки
        for i in range(4):
            chords_frame.rowconfigure(i, weight=1)
        for i in range(2):
            chords_frame.columnconfigure(i, weight=1)
        
        # Панель навигации
        nav_frame = tk.Frame(main_container, bg=self.colors['bg'])
        nav_frame.pack(fill=tk.X, pady=20)
        
        back_btn = tk.Button(nav_frame, text="← Назад к выбору", 
                            font=self.fonts['normal'], bg=self.colors['card'],
                            fg=self.colors['fg'], padx=20, pady=8,
                            command=self.show_ear_trainer, cursor='hand2',
                            relief=tk.RAISED, bd=0,
                            activebackground='#3d566e', activeforeground='white')
        back_btn.pack(side=tk.LEFT, padx=5)
        
        home_btn = tk.Button(nav_frame, text="🏠 Главное меню", 
                           font=self.fonts['normal'], bg=self.colors['card'],
                           fg=self.colors['fg'], padx=20, pady=8,
                           command=self.create_main_menu, cursor='hand2',
                            relief=tk.RAISED, bd=0,
                            activebackground='#3d566e', activeforeground='white')
        home_btn.pack(side=tk.LEFT, padx=5)
        
        # Инициализация состояния упражнения
        self.chord_game_active = False
        self.current_chord = None
        self.current_base_note = None
        self.difficulty_label.config(text=f"Текущий уровень: {self.current_difficulty}")
    
    def rhythm_exercise(self):
        """Ритмические упражнения"""
        self.clear_window()
        
        # Главный контейнер
        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Заголовок
        header_frame = tk.Frame(main_container, bg=self.colors['bg'])
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(header_frame, text="⏱️ Ритмические упражнения", 
                font=self.fonts['title'], bg=self.colors['bg'], 
                fg=self.colors['fg']).pack()
        
        # Описание
        desc_frame = tk.Frame(main_container, bg=self.colors['card'], 
                             relief=tk.RAISED, bd=1)
        desc_frame.pack(fill=tk.X, pady=(0, 20), padx=10)
        
        desc_text = """Простучите ритмический рисунок, показанный на экране.
        Начните с простых ритмов и постепенно переходите к более сложным.
        Вы можете использовать метроном для поддержания темпа."""
        
        tk.Label(desc_frame, text=desc_text, font=self.fonts['normal'], 
                bg=self.colors['card'], fg=self.colors['fg'], 
                wraplength=600, justify=tk.LEFT, padx=15, pady=10).pack()
        
        # Уровень сложности
        difficulty_frame = tk.Frame(main_container, bg=self.colors['bg'])
        difficulty_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(difficulty_frame, text="Уровень сложности:", 
                font=self.fonts['normal'], bg=self.colors['bg'], 
                fg=self.colors['fg']).pack(side=tk.LEFT, padx=5)
        
        difficulties = ["Начальный", "Средний", "Продвинутый"]
        self.rhythm_difficulty = tk.StringVar(value="Начальный")
        
        for diff in difficulties:
            rb = tk.Radiobutton(difficulty_frame, text=diff, 
                               variable=self.rhythm_difficulty, value=diff,
                               font=self.fonts['small'], bg=self.colors['bg'],
                               fg=self.colors['fg'], selectcolor=self.colors['accent'],
                               activebackground=self.colors['bg'],
                               activeforeground=self.colors['fg'],
                               command=self.change_rhythm_difficulty)
            rb.pack(side=tk.LEFT, padx=5)
        
        # Отображение ритма
        rhythm_display_frame = tk.Frame(main_container, bg='white', 
                                       relief=tk.SUNKEN, bd=2)
        rhythm_display_frame.pack(pady=20, padx=50, fill=tk.BOTH, expand=True)
        
        self.rhythm_display = tk.Label(rhythm_display_frame, text="", 
                                       font=("Segoe UI", 36, "bold"),
                                       bg='white', fg='black')
        self.rhythm_display.pack(expand=True)
        
        # Пояснение ритма
        self.rhythm_explanation = tk.Label(main_container, text="", 
                                          font=self.fonts['normal'], bg=self.colors['bg'], 
                                          fg=self.colors['accent'])
        self.rhythm_explanation.pack(pady=5)
        
        # Панель управления
        control_frame = tk.Frame(main_container, bg=self.colors['bg'])
        control_frame.pack(fill=tk.X, pady=20)
        
        # Кнопки управления
        generate_btn = tk.Button(control_frame, text="Новый ритм", 
                                font=self.fonts['normal'], bg=self.colors['accent'],
                                fg='white', width=15, height=1,
                                command=self.generate_new_rhythm, cursor='hand2',
                                relief=tk.RAISED, bd=0,
                                activebackground='#2980b9', activeforeground='white')
        generate_btn.pack(side=tk.LEFT, padx=5)
        
        play_btn = tk.Button(control_frame, text="🎵 Проиграть ритм", 
                            font=self.fonts['normal'], bg=self.colors['accent'],
                            fg='white', width=15, height=1,
                            command=self.play_rhythm_pattern, cursor='hand2',
                            relief=tk.RAISED, bd=0,
                            activebackground='#2980b9', activeforeground='white')
        play_btn.pack(side=tk.LEFT, padx=5)
        
        metronome_btn = tk.Button(control_frame, text="⏱️ Метроном", 
                                 font=self.fonts['normal'], bg=self.colors['card'],
                                 fg=self.colors['fg'], width=15, height=1,
                                 command=self.toggle_metronome, cursor='hand2',
                                 relief=tk.RAISED, bd=0,
                                 activebackground='#3d566e', activeforeground='white')
        self.metronome_active = False
        self.metronome_btn = metronome_btn
        metronome_btn.pack(side=tk.LEFT, padx=5)
        
        # Панель навигации
        nav_frame = tk.Frame(main_container, bg=self.colors['bg'])
        nav_frame.pack(fill=tk.X, pady=20)
        
        back_btn = tk.Button(nav_frame, text="← Назад к выбору", 
                            font=self.fonts['normal'], bg=self.colors['card'],
                            fg=self.colors['fg'], padx=20, pady=8,
                            command=self.show_ear_trainer, cursor='hand2',
                            relief=tk.RAISED, bd=0,
                            activebackground='#3d566e', activeforeground='white')
        back_btn.pack(side=tk.LEFT, padx=5)
        
        home_btn = tk.Button(nav_frame, text="🏠 Главное меню", 
                           font=self.fonts['normal'], bg=self.colors['card'],
                           fg=self.colors['fg'], padx=20, pady=8,
                           command=self.create_main_menu, cursor='hand2',
                           relief=tk.RAISED, bd=0,
                           activebackground='#3d566e', activeforeground='white')
        home_btn.pack(side=tk.LEFT, padx=5)
        
        # Инициализация упражнения
        self.current_rhythm_level = "Начальный"
        self.generate_new_rhythm()
        
    def change_rhythm_difficulty(self):
        """Изменение уровня сложности ритмических упражнений"""
        self.current_rhythm_level = self.rhythm_difficulty.get()
        self.generate_new_rhythm()
        
    def generate_new_rhythm(self):
        """Генерация нового ритмического рисунка"""
        if self.current_rhythm_level == "Начальный":
            patterns = self.rhythm_patterns["Начальный"]
        elif self.current_rhythm_level == "Средний":
            patterns = self.rhythm_patterns["Средний"]
        else:  # Продвинутый
            patterns = self.rhythm_patterns["Продвинутый"]
        
        rhythm_pattern, explanation = random.choice(patterns)
        
        self.rhythm_display.config(text=rhythm_pattern)
        self.rhythm_explanation.config(text=explanation)
        
        self.current_rhythm = rhythm_pattern
        self.current_rhythm_explanation = explanation
        
    def play_rhythm_pattern(self):
        """Воспроизведение ритмического рисунка"""
        if not hasattr(self, 'current_rhythm'):
            return
            
        frequency = int(self.note_frequencies["До"])
        duration_map = {
            "𝅝": 1600,  # Целая нота
            "𝅗𝅥": 800,   # Половинная
            "♩": 400,   # Четвертная
            "♪": 200,   # Восьмая
            "♬": 100,   # Шестнадцатая
            ".": 0,     # Точка (пауза)
        }
        
        def play_rhythm():
            if self.metronome_active:
                for i in range(4):
                    winsound.Beep(800, 100)
                    time.sleep(60 / self.metronome_tempo - 0.1)
            
            for char in self.current_rhythm:
                if char in duration_map and duration_map[char] > 0:
                    winsound.Beep(frequency, duration_map[char])
                    time.sleep(0.05)
                elif char == " ":
                    time.sleep(0.1)
        
        sound_thread = threading.Thread(target=play_rhythm)
        sound_thread.daemon = True
        sound_thread.start()
        
    def toggle_metronome(self):
        """Включение/выключение метронома"""
        self.metronome_active = not self.metronome_active
        
        if self.metronome_active:
            self.metronome_btn.config(text="⏱️ Стоп метроном", bg=self.colors['success'], fg='white')
            self.start_metronome()
        else:
            self.metronome_btn.config(text="⏱️ Метроном", bg=self.colors['card'], fg=self.colors['fg'])
            self.stop_metronome()
            
    def start_metronome(self):
        """Запуск метронома"""
        def metronome_loop():
            while self.metronome_active:
                winsound.Beep(1000, 50)
                time.sleep(60 / self.metronome_tempo - 0.05)
                
                for _ in range(3):
                    winsound.Beep(800, 50)
                    time.sleep(60 / self.metronome_tempo - 0.05)
        
        if self.metronome_thread is None or not self.metronome_thread.is_alive():
            self.metronome_thread = threading.Thread(target=metronome_loop)
            self.metronome_thread.daemon = True
            self.metronome_thread.start()
            
    def stop_metronome(self):
        """Остановка метронома"""
        self.metronome_active = False
    
    def clear_window(self):
        """Очистка окна"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    # Методы для получения текста теории из учебника (остаются без изменений)
    def get_sound_basics_text(self):
        return """ОСНОВЫ МУЗЫКАЛЬНОГО ЗВУКА

Введение в мир музыкальных звуков
Добро пожаловать в удивительный мир музыки! Сегодня мы начнем наше путешествие с самого фундамента - с понимания того, что такое музыкальный звук и чем он отличается от обычного шума.

1. Что такое звук?
Звук - это физическое явление, которое возникает в результате колебаний какого-либо упругого тела. Представьте себе гитарную струну - когда вы ее дергаете, она начинает вибрировать, создавая звуковые волны, которые достигают наших ушей.

Все звуки делятся на две большие категории:

Музыкальные звуки:
Имеют определенную высоту
Обладают ясным тембром
Могут быть точно воспроизведены
Примеры: звук фортепиано, скрипки, человеческого голоса

Шумовые звуки:
Не имеют определенной высоты
Характеризуются нерегулярными колебаниями
Примеры: стук молотко, шум дождя, шелест листьев

2. Четыре главных свойства музыкального звука
У каждого музыкального звука есть четыре основных характеристики, которые делают его уникальным:

🎯 ВЫСОТА ЗВУКА
Что это? Свойство, которое позволяет нам различать высокие и низкие звуки.

От чего зависит? От частоты колебаний:
Высокие звуки = высокая частота (быстрые колебания)
Низкие звуки = низкая частота (медленные колебания)

Практический пример:
Женский голос обычно выше мужского
Писк мыши - высокий звук, рычание льва - низкий

Диапазон человеческого слуха: от 16 до 20 000 колебаний в секунду (Герц)

⏱️ ДЛИТЕЛЬНОСТЬ
Что это? Продолжительность звучания во времени.

Как измеряется? В музыкальных долях:
Целые ноты
Половинные
Четвертные
Восьмые и т.д.

Практическое значение: Длительности создают ритм - сердцебиение музыки.

🔊 ГРОМКОСТЬ
Что это? Сила звучания, интенсивность звука.

От чего зависит? От амплитуды колебаний:
Большая амплитуда = громкий звук
Малая амплитуда = тихий звук

Музыкальные обозначения:
p (piano) - тихо
f (forte) - громко
mp (mezzo piano) - умеренно тихо
mf (mezzo forte) - умеренно громко

🎨 ТЕМБР
Что это? Окраска звука, его "оттенок".

Почему важен? Позволяет отличать звучание разных инструментов, даже когда они играют одну и ту же ноту.

Пример: Нота "До" на фортепиано и на скрипке звучит по-разному именно из-за тембра.

3. Звукоряд и октавы
Что такое звукоряд?
Это последовательность музыкальных звуков, расположенных по высоте - от низких к высоким.

Октава - основная единица
Октава - это интервал между двумя звуками, частота второго из которых в два раза больше частоты первого.

На фортепиано октава включает 12 звуков (7 основных и 5 производных)

Система октав:
Субконтроктава (самые низкие звуки)
Контроктава
Большая октава
Малая октава
Первая октава
Вторая октава
Третья октава
Четвертая октава
Пятая октава (самые высокие звуки)

4. Полутон и целый тон
Полутон
Самое маленькое расстояние между звуками в европейской музыке
На фортепиано: расстояние между двумя соседними клавишами
Пример: от "До" до "До-диез"

Целый тон
Состоит из двух полутонов
Пример: от "До" до "Ре"

5. Знаки альтерации - изменяем высоту звуков
Знаки альтерации - это специальные символы, которые изменяют высоту нот:

# ДИЕЗ
Повышает звук на полтона
Пример: "До" → "До-диез"

b БЕМОЛЬ
Понижает звук на полтона
Пример: "Ре" → "Ре-бемоль"

× ДУБЛЬ-ДИЕЗ
Повышает звук на целый тон
Пример: "До" → "До-дубль-диез" (звучит как "Ре")

bb ДУБЛЬ+БЕМОЛЬ
Понижает звук на целый тон
Пример: "Ре" → "Ре-дубль-бемоль" (звучит как "До")

♮ БЕКАР
Отменяет действие любого знака альтерации
Возвращает звук к его основной высоте

Заключение
Понимание основ музыкального звука - это первый и самый важный шаг в изучении музыки. Помните:

Музыкальный звук имеет четыре свойства: высоту, длительность, громкость и тембр
Звукоряд организует звуки по высоте
Октава - основная единица измерения
Полутон - минимальное расстояние между звуками
Знаки альтерации помогают создавать разнообразие в музыке

На следующей лекции мы познакомимся с нотами и нотным станом - языком, на котором говорят музыканты!"""

    def get_notes_text(self):
        return """НОТЫ И СИСТЕМА НОТНОЙ ЗАПИСИ

Введение в музыкальную грамоту
Сегодня мы познакомимся с удивительным изобретением человечества - нотной грамотой! Это универсальный язык, который позволяет записывать, хранить и передавать музыку через века и континенты.

1. Что такое ноты и зачем они нужны?
Нота - это графический знак для записи музыкального звука. Представьте, что ноты - это буквы в музыкальном алфавите!

Зачем нужны ноты?
✅ Сохранять музыку для будущих поколений
✅ Передавать музыкальные идеи другим музыкантам
✅ Изучать и анализировать музыкальные произведения
✅ Исполнять музыку точно так, как задумал композитор

2. Нотный стан - дом для нот
Нотный стан (или нотоносец) - это система из пяти параллельных линий, на которых и между которыми пишутся ноты.

Структура нотного стана🎼 :
   5-я линия ────────
   4-я линие ────────
   3-я линия ────────  
   2-я линия ────────
   1-я линия ────────

Линии нумеруются снизу вверх (1-я - самая нижняя)
Промежутки между линиями тоже используются для записи нот
Всего: 5 линий + 4 промежутка = 9 позиций для нот

Добавочные линии
Когда нот не хватает места на основных линиях, мы используем добавочные линии - короткие линии выше или ниже нотного стана.

3. Строение ноты - из чего она состоит?
Каждая нота состоит из нескольких элементов:

 Головка ноты
Овал (может быть пустым или закрашенным)
Определяет высоту звука

📏 Штиль
Вертикальная палочка
Направление: вверх (справа) или вниз (слева)
Обычно от 3-й линии: ноты выше - штиль вниз, ноты ниже - штиль вверх

🎏 Флажок (хвост)
Изогнутая линия от штиля
Определяет длительность ноты
Может быть один, два или больше флажков

4. Ключи - ключ к пониманию нот
Ключи определяют, каким нотам соответствуют линии и промежутки нотного стана.

Скрипичный ключ (Ключ Соль) 𝄞
- Определяет положение ноты Соль первой октавы
- Записывается на второй линии
- Используется для высоких голосов и инструментов
- Самый распространенный ключ

Басовый ключ (Ключ Фа) 𝄢
- Определяет положение ноты Фа малой октавы
- Записывается на четвертой линии
- Используется для низких голосов и инструментов

5. Система названий нот
Основные 7 нот: До - Ре - Ми - Фа - Соль - Ля - Си
Латинские обозначения: C - D - E - F - G - A - B (или H в некоторых странах)

6. Расположение нот на нотном стане
В скрипичном ключе:
До - на 1-й добавочной
Ре - под 1-й линией
Ми - на 1-й линии
Фа - в 1-м промежутке
Соль - на 2-й линии  ← ключевая нота!
Ля - во 2-м промежутке  
Си - на 3-й линии

В басовом ключе:
Соль - на 1-й линии
Ля - в 1-м промежутке
Си - на 2-й линии
До - во 2-м промежутке
Ре - на 3-й линии
Ми - в 3-м промежутке
Фа - на 4-й линии  ← ключевая нота!

7. Длительности нот - ритмическая азбука
Основные длительности:
Целая нота ○
Самый долгий звук
Пустая головка без штиля

Половинная нота [○ со штилем]
Вдвое короче целой
Пустая головка со штилем

Четвертная нота ♩
В 4 раза короче целой
Закрашенная головка со штилем

Восьмая нота ♪
В 8 раз короче целой
Закрашенная головка с флажком

Шестнадцатая нота [♩ с двумя флажками]
В 16 раз короче целой
Закрашенная головка с двумя флажками

8. Паузы - музыкальное молчание
Паузы - это знаки перерывов в звучании. У каждой длительности ноты есть соответствующая пауза:

Целая пауза  - висит под четвертой линией
Половинная пауза  - сидит на третьей линии
Четвертная пауза  - зигзагообразный знак
Восьмая пауза  - похожа на цифру 7
Шестнадцатая пауза  - с двумя флажками

Советы для начинающих
Запоминайте постепенно - не пытайтесь выучить все сразу
Практикуйтесь регулярно - лучше по 10 минут каждый день, чем 2 часа раз в неделю
Используйте ассоциации - придумайте образы для запоминания нот
Слушайте и читайте одновременно - это поможет связать зрительный образ со звуком
Не бойтесь ошибок - они естественная часть обучения!

Заключение
Поздравляю! Вы сделали важный шаг в изучении музыкального языка. Теперь вы знаете:

📝 Что такое ноты и нотный стан
🎼 Как устроены скрипичный и басовый ключи
🎵 Основные длительности нот и пауз
🎹 Расположение нот на нотном стане
"""

    def get_rhythm_text(self):
        return """РИТМ, МЕТР И ДЛИТЕЛЬНОСТИ

Введение в музыкальное время
Добро пожаловать в мир ритма - сердцебиения музыки! Сегодня мы изучим, как организовано время в музыке, и научимся понимать её внутренний пульс.

1. Основные понятия: что такое ритм, метр и такт?
🎵 РИТМ
Ритм - это душа музыки! Это организация звуков во времени, последовательность различных длительностей.

Простая аналогия: Представьте, что вы идете:
Равномерные шаги: "ТАК-ТАК-ТАК-ТАК" - это ровный ритм
Переменные шаги: "ТАК-та-та-ТАК-та" - это сложный ритм

⏰ МЕТР
Метр - это равномерное чередование сильных и слабых долей, своеобразный "скелет" ритма.

Примеры метра:
Марш: "РАЗ-два, РАЗ-два" (сильная-слабая)
Вальс: "РАЗ-два-три" (сильная-слабая1-слабая2)

📦 ТАКТ
Такт - это отрезок музыки между двумя сильными долями. Представьте, что такты - это кирпичики, из которых строится музыкальное здание.

2. Музыкальный размер - правила игры
Размер - это цифровое обозначение метра, который записывается в начале нотного стана.

Как читать размер?
Верхняя цифра: сколько долей в такте
Нижняя цифра: какая длительность считается одной долей

Основные размеры:
Двудольные размеры:
2/4 - "две четверти" (марш)
2/2 - "две половинки"

Трехдольные размеры:
3/4 - "три четверти" (вальс)
3/8 - "три восьмые"

Четверодольные размеры:
4/4 - "четыре четверти" (самый распространенный)
C - тоже означает 4/4

3. Система длительностей - музыкальная математика
Длительности нот связаны математическими соотношениями:

СИСТЕМА ДЛИТЕЛЬНОСТЕЙ НОТ И ПАУЗ
ЦЕЛАЯ НОТА
Соотношение: 1 (базовая длительность)
Внешний вид ноты: белый овал без штиля
Пауза: черный прямоугольник под четвертой линией
Длительность звучания: самая продолжительная

ПОЛОВИННАЯ НОТА
Соотношение: 1/2 от целой
Внешний вид ноты: белый овал со штилем
Пауза: черный прямоугольник на третьей линии
Длительность звучания: в два раза короче целой

ЧЕТВЕРТНАЯ НОТА
Соотношение: 1/4 от целой
Внешний вид ноты: черный овал со штилем
Пауза: зигзагообразный знак
Длительность звучания: в четыре раза короче целой

ВОСЬМАЯ НОТА
Соотношение: 1/8 от целой
Внешний вид ноты: черный овал со штилем и одним флажком
Пауза: знак, похожий на цифру 7 с одним флажком
Длительность звучания: в восемь раз короче целой

ШЕСТНАДЦАТАЯ НОТА
Соотношение: 1/16 от целой
Внешний вид ноты: черный овал со штилем и двумя флажками
Пауза: знак с двумя флажками
Длительность звучания: в шестнадцать раз короче целой

ОТНОШЕНИЯ МЕЖДУ ДЛИТЕЛЬНОСТЯМИ:
1 целая = 2 половинных
1 целая = 4 четвертных  
1 целая = 8 восьмых
1 целая = 16 шестнадцатых
1 половинная = 2 четвертных
1 четвертная = 2 восьмых
1 восьмая = 2 шестнадцатых

4. Знаки для увеличения длительностей
ТОЧКА РЯДОМ С НОТОЙ ●.
Точка увеличивает длительность ноты наполовину:
Четвертная с точкой = четвертная + восьмая
Половина с точкой = половина + четверть
Целая с точкой = целая + половина

ЛИГА ⁀
Лига - это дуга, соединяющая две ноты одинаковой высоты:
Объединяет их длительности
Создает непрерывное звучание
Пример: ♪ ⁀ ♪ = ♫ (две четверти = половинная)

5. Особые ритмические фигуры
ТРИОЛЬ [3]
Три ноты вместо двух на протяжении одной доли:
Обозначается цифрой 3
♪♪♪ (триоль) = ♫ (две восьмые)
Создает ощущение плавности

СИНКОПА ⤴⤵
Синкопа - это смещение акцента с сильной доли на слабую:
Примеры синкопы:
Звук на слабой доле, а на сильной - пауза
Долгий звук начинается на слабой доле и переходит на сильную
Создает эффект неожиданности, "качания"

6. Темп - скорость музыки
Темп определяет, насколько быстро или медленно звучит музыка:

Основные обозначения темпа:
Медленные темпы:
Largo (ларго) - очень медленно, широко
Adagio (адажио) - спокойно, медленно

Умеренные темпы:
Andante (анданте) - спокойно, "шагом"
Moderato (модерато) - умеренно

Быстрые темпы:
Allegro (аллегро) - быстро, весело
Presto (престо) - очень быстро

7. Динамические оттенки - громкость звучания
Динамика показывает, насколько громко или тихо нужно играть:

Основные обозначения:
p - пиано (тихо)
f - форте (громко)
pp - пианиссимо (очень тихо)
ff - фортиссимо (очень громко)
mp - меццо-пиано (умеренно тихо)
mf - меццо-форте (умеренно громко)

Изменения громкости:
Crescendo (крещендо) - постепенное усиление
Decrescendo (декрещендо) - постепенное ослабление

Советы для успешного освоения ритма
✅ Слушайте внимательно - развивайте внутренний слух
✅ Считайте вслух - это помогает держать темп
✅ Используйте метроном - ваш лучший друг в работе с ритмом
✅ Начинайте медленно - сначала точность, потом скорость
✅ Хлопайте и топайте - подключайте всё тело к ощущению ритма

Заключение
Поздравляю! Теперь вы понимаете язык музыкального времени. Вы узнали:

🎯 Что такое ритм, метр и такт
🎯 Как читать музыкальные размеры
🎯 Систему длительностей нот и пауз
🎯 Особые ритмические фигуры
🎯 Как темп и динамика влияют на характер музыки

Помните: ритм - это не просто счёт, это живое дыхание музыки. Практикуйтесь регулярно, и скоро вы будете чувствовать ритм интуитивно!
"""

    def get_intervals_text(self):
        return """ИНТЕРВАЛЫ

Введение в мир интервалов
Сегодня мы изучим одну из самых важных тем в музыке - интервалы! Это строительные блоки, из которых состоят все мелодии и аккорды. Представьте, что интервалы - это слова в языке музыки.

1. Что такое интервал?
Интервал - это расстояние между двумя звуками.

Два типа интервалов:
Мелодический интервал - звуки берутся последовательно (один за другим)
До → Ре (восходящий)
До → Си (нисходящий)

Гармонический интервал - звуки берутся одновременно
До + Ре (звучат вместе)

2. Из чего состоит название интервала?
Каждый интервал имеет две характеристики:

Количественная (сколько ступеней охватывает)
Прима (1) - одна ступень
Секунда (2) - две ступени
Терция (3) - три ступени
Кварта (4) - четыре ступени
Квинта (5) - пять ступеней
Секста (6) - шесть ступеней
Септима (7) - семь ступеней
Октава (8) - восемь ступеней

Качественная (точное количество тонов)
Чистые (прима, кварта, квинта, октава)
Малые (секунда, терция, секста, септима)
Большие (секунда, терция, секста, септима)
Увеличенные (любые интервалы)
Уменьшенные (любые интервалы)

3. Подробная таблица простых интервалов
Интервал        Тонов    Пример от До   Характер звучания
Чистая прима    0        До-До          Полное слияние
Малая секунда   0.5      До-Ре♭         Напряженно
Большая секунда 1        До-Ре          Уверенно
Малая терция    1.5      До-Ми♭         Грустно
Большая терция  2        До-Ми          Радостно
Чистая кварта   2.5      До-Фа          Устойчиво
Тритон          3        До-Фа♯         Драматично
Чистая квинта   3.5      До-Соль        Благозвучно
Малая секста    4        До-Ля♭         Лирично
Большая секста  4.5      До-Ля          Восторженно
Малая септима   5        До-Си♭         Напряженно
Большая септима 5.5      До-Си          Резко
Чистая октава   6        До-До          Полное слияние

4. Тритоны - самые загадочные интервалы
Тритон - это интервал в 3 тона, который делит октаву пополам.

Два вида тритонов:
Увеличенная кварта (3 тона) - До-Фа♯
Уменьшенная квинта (3 тона) - До-Соль♭

Особенности тритонов:
Самые неустойчивые интервалы
Сильно тяготеют к разрешению
В средневековье назывались "диаболус ин музика" (дьявол в музыке)

5. Обращение интервалов
Обращение - это перенос нижнего звука на октаву вверх или верхнего звука на октаву вниз.

Правила обращения:
Количество ступеней: 9 - исходный интервал = обращенный
Качество меняется на противоположное

Таблица обращений:
Прима (1)  ↔ Октава (8)
Секунда (2) ↔ Септима (7)
Терция (3)  ↔ Секста (6)
Кварта (4)  ↔ Квинта (5)

6. Консонансы и диссонансы
Консонансы - благозвучные интервалы
Абсолютные консонансы (полное слияние):
Чистая прима
Чистая октава
Чистая квинта

Относительные консонансы (приятное звучание):
Большие и малые терции
Большие и малые сексты

Диссонансы - напряженные интервалы
Резкие диссонансы:
Все секунды
Все септимы
Все тритоны

7. Разрешение диссонансов
Диссонансы стремятся перейти в консонансы - это называется разрешением.

Основные правила разрешения:
Диссонанс → Консонанс
Неустойчивые звуки → Устойчивые звуки
Движение по тонам лада

Примеры разрешений:
Малая секунда До-Ре♭ → Большая терция До-Ми♭
Тритон До-Фа♯ → Большая терция Ми-Соль

Интервалы в музыке
Характерные музыкальные примеры:
Большая секста - начало песни "Jingle Bells"
Чистая кварта - начало гимна "Боже, царя храни"
Большая терция - мажорное трезвучие
Малая терция - минорное трезвучие

Эмоциональная окраска интервалов:
Большие интервалы - светлые, радостные
Малые интервалы - темные, грустные
Тритоны - таинственные, напряженные

Таблица для быстрого запоминания
Простые интервалы от ноты До:
Прима      - До-До      (0 тонов)
Секунда    - До-Ре      (1 тон)
Терция     - До-Ми      (2 тона)
Кварта     - До-Фа      (2.5 тона)
Квинта     - До-Соль    (3.5 тона)
Секста     - До-Ля      (4.5 тона)
Септима    - До-Си      (5.5 тонов)
Октава     - До-До      (6 тонов)

Заключение
Поздравляю! Теперь вы понимаете язык музыкальных расстояний. Вы узнали:

🎯 Что такое интервалы и их виды
🎯 Все простые интервалы от примы до октавы
🎯 Правила обращения интервалов
🎯 Разницу между консонансами и диссонансами
🎯 Как разрешать напряженные интервалы

Интервалы - это фундамент всей музыки. Понимая их, вы сможете анализировать любые музыкальные произведения, сочинять собственные мелодии и развивать свой слух!"""

    def get_chords_text(self):
        return """АККОРДЫ: СТРОЕНИЕ И ВИДЫ

Введение в гармонию
Добро пожаловать в мир аккордов - магических сочетаний звуков, которые создают гармонию! Сегодня мы изучим, как из отдельных нот рождаются аккорды, и познакомимся с их удивительным разнообразием.

1. Что такое аккорд?
Аккорд - это сочетание трех или более звуков, взятых одновременно.

Простая аналогия:
Одна нота - это слово
Интервал - это фраза
Аккорд - это целое предложение!

Основные характеристики аккорда:
Состоит минимум из 3 звуков
Звуки располагаются по терциям
Создает гармоническую основу музыки

2. Трезвучия - фундамент гармонии
Трезвучие - это аккорд из трех звуков, расположенных по терциям.

Строение трезвучия:
Нижний звук - основной тон (прима)
Средний звук - терция от основного тона
Верхний звук - квинта от основного тона

3. Четыре основных вида трезвучий
МАЖОРНОЕ ТРЕЗВУЧИЕ (б.3 + м.3)
Строение: большая терция + малая терция
Звучание: светлое, радостное, устойчивое
Обозначение: буквой (C, D, G) или словом "dur"
Пример от До: До-Ми-Соль

МИНОРНОЕ ТРЕЗВУЧИЕ (м.3 + б.3)
Строение: малая терция + большая терция
Звучание: темное, грустное, мечтательное
Обозначение: буквой с "m" (Cm, Dm, Gm) или словом "moll"
Пример от До: До-Ми-бемоль-Соль

УМЕНЬШЕННОЕ ТРЕЗВУЧИЕ (м.3 + м.3)
Строение: малая терция + малая терция
Звучание: напряженное, тревожное, неустойчивое
Обозначение: dim или маленьким кружком (Cdim, C°)
Пример от До: До-Ми-бемоль-Соль-бемоль

УВЕЛИЧЕННОЕ ТРЕЗВУЧИЕ (б.3 + б.3)
Строение: большая терция + большая терция
Звучание: фантастическое, загадочное, неустойчивое
Обозначение: aug или плюсом (Caug, C+)
Пример от До: До-Ми-Соль-диез

4. Обращения трезвучий
Обращение - это изменение порядка звуков в аккорде, когда нижним звуком становится не основной тон.

СЕКСТАККОРД (6)
Строение: терцовый тон в басу
Обозначение: цифрой 6 (C6, Dm6)
Звучание: менее устойчивое, чем основное трезвучие
Пример от До мажора: Ми-Соль-До

КВАРТСЕКСТАККОРД (6/4)
Строение: квинтовый тон в басу
Обозначение: цифрой 6/4 (C6/4, Dm6/4)
Звучание: наименее устойчивое из всех обращений
Пример от До мажора: Соль-До-Ми

5. Септаккорды - аккорды с напряжением
Септаккорд - это аккорд из четырех звуков, расположенных по терциям.

МАЛЫЙ МАЖОРНЫЙ СЕПТАККОРД (ДОМИНАНТСЕПТАККОРД)
Строение: мажорное трезвучие + малая терция
Обозначение: цифрой 7 (C7, G7)
Звучание: напряженное, сильно тяготеет к разрешению
Пример от Соль: Соль-Си-Ре-Фа

МАЛЫЙ МИНОРНЫЙ СЕПТАККОРД
Строение: минорное трезвучие + малая терция
Обозначение: m7 (Cm7, Dm7)
Звучание: мягкое, меланхоличное
Пример от До: До-Ми-бемоль-Соль-Си-бемоль

УМЕНЬШЕННЫЙ СЕПТАККОРД
Строение: уменьшенное трезвучие + малая терция
Обозначение: dim7 или °7 (Cdim7, C°7)
Звучание: очень напряженное, таинственное
Пример от До: До-Ми-бемоль-Соль-бемоль-Си-дубль-бемоль

БОЛЬШОЙ МАЖОРНЫЙ СЕПТАККОРД
Строение: мажорное трезвучие + большая терция
Обозначение: maj7 (Cmaj7)
Звучание: яркое, "небесное"
Пример от До: До-Ми-Соль-Си

6. Главные трезвучия в тональности
В каждой тональности есть три основных аккорда, которые определяют ее гармоническую структуру:

ТОНИЧЕСКОЕ ТРЕЗВУЧИЕ (T/t)
Ступень: I (первая)
Функция: устойчивая, точка покоя
Пример в До мажоре: До-Ми-Соль
Пример в ля миноре: Ля-До-Ми

СУБДОМИНАНТОВОЕ ТРЕЗВУЧИЕ (S/s)
Ступень: IV (четвертая)
Функция: предыктовая, создает движение
Пример в До мажоре: Фа-Ля-До
Пример в ля миноре: Ре-Фа-Ля

ДОМИНАНТОВОЕ ТРЕЗВУЧИЕ (D)
Ступень: V (пятая)
Функция: неустойчивая, сильно тяготеет к тонике
Пример в До мажоре: Соль-Си-Ре
Пример в ля миноре: Ми-Соль-диез-Си

7. Аккордовые последовательности
Аккорды редко используются по отдельности - они объединяются в последовательности:

Основная последовательность:
T → S → D → T
(тоника → субдоминанта → доминанта → тоника)

Таблица для быстрого запоминания
Основные трезвучия от ноты До:
До мажор: До-Ми-Соль (б.3 + м.3)
До минор: До-Ми-бемоль-Соль (м.3 + б.3)
До уменьшенное: До-Ми-бемоль-Соль-бемоль (м.3 + м.3)
До увеличенное: До-Ми-Соль-диез (б.3 + б.3)

Главные трезвучия в До мажоре:
Tonic (T): До-Ми-Соль
Subdominant (S): Фа-Ля-До
Dominant (D): Соль-Си-Ре

Заключение
Поздравляю! Теперь вы понимаете язык музыкальной гармонии. Вы узнали:

🎹 Что такое аккорды и трезвучия
🎹 Четыре основных вида трезвучий
🎹 Обращения аккордов
🎹 Септаккорды и их напряжение
🎹 Главные аккорды тональности
🎹 Основные аккордовые последовательности

Аккорды - это краски, которыми композитор рисует музыкальные картины. Понимая их, вы сможете не только анализировать музыку, но и создавать свою собственную!
"""

    def get_modes_text(self):
        return """ЛАД, ТОНАЛЬНОСТЬ И СИСТЕМА ЗВУКОВОЙ ОРГАНИЗАЦИИ

Введение в ладовую систему
Сегодня мы познакомимся с фундаментальными понятиями музыки - ладом и тональностью. Это те принципы, которые превращают набор звуков в осмысленную музыкальную речь, наполненную чувствами и эмоциями.

1. Основные понятия
ЛАД
Лад - это система взаимоотношений между звуками, где один звук становится центральным (тоникой), а остальные находятся в определенной зависимости от него.

Простая аналогия: Представьте солнечную систему:
- Тоника - это Солнце (центр)
- Остальные звуки - это планеты, которые вращаются вокруг него

ТОНАЛЬНОСТЬ
Тональность - это конкретное высотное положение лада. Она определяется:
- Тоникой - главным, центральным звуком
- Ладовым наклонением - мажором или минором

2. Ступени лада и их функции
В каждом ладе 7 основных ступеней, каждая из которых имеет свое функциональное значение:

I ступень - ТОНИКА (T/t)
- Центр тяготения, точка покоя
- Наиболее устойчивый звук
- Определяет название тональности

IV ступень - СУБДОМИНАНТА (S/s)
- Нижняя опора, "предыктовая" функция
- Создает движение от тоники
- Подготавливает появление доминанты

V ступень - ДОМИНАНТА (D)
- Верхняя опора, главная неустойчивая функция
- Сильнее всего тяготеет к тонике
- Создает наибольшее напряжение

II и VII ступени - ВВОДНЫЕ ЗВУКИ
- Наиболее неустойчивые звуки
- Сильно тяготеют к тонике
- VII ступень называется "восходящий вводный звук"
- II ступень называется "нисходящий вводный звук"

III и VI ступени - МЕДИАНТЫ
- Заполняют пространство между главными функциями
- III ступень определяет мажор/минор
- Создают плавность голосоведения

3. Основные лады: мажор и минор
МАЖОР (Dur)
- Звучание: светлое, радостное, торжественное
- Эмоциональная окраска: уверенность, оптимизм, ясность
- Строение: Тон-Тон-Полутон-Тон-Тон-Тон-Полутон

МИНОР (moll)
- Звучание: темное, грустное, меланхоличное
- Эмоциональная окраска: печаль, размышление, глубина
- Строение: Тон-Полутон-Тон-Тон-Полутон-Тон-Тон

4. Виды мажора и минор
НАТУРАЛЬНЫЙ МАЖОР
- Естественное строение без изменений
- Устойчивое, ясное звучание
- Пример: До-Ре-Ми-Фа-Соль-Ля-Си-До

ГАРМОНИЧЕСКИЙ МАЖОР
- Пониженная VI ступень
- Усиленное тяготение к доминанте
- Появляется восточный, драматический оттенок
- Пример: До-Ре-Ми-Фа-Соль-Ля-бемоль-Си-До

МЕЛОДИЧЕСКИЙ МАЖОР
- При движении вверх - натуральный
- При движении вниз - пониженные VI и VII ступени
- Плавное, певучее звучание

НАТУРАЛЬНЫЙ МИНОР
- Естественное строение
- Строгое, сдержанное звучание
- Пример: Ля-Си-До-Ре-Ми-Фа-Соль-Ля

ГАРМОНИЧЕСКИЙ МИНОР
- Повышенная VII ступень
- Усиленное тяготение к тонике
- Более напряженное, драматичное звучание
- Пример: Ля-Си-До-Ре-Ми-Фа-Соль-диез-Ля

МЕЛОДИЧЕСКИЙ МИНОР
- При движении вверх - повышенные VI и VII ступени
- При движении вниз - натуральный
- Более светлое, лирическое звучание

5. Система тональностей
ПАРАЛЛЕЛЬНЫЕ ТОНАЛЬНОСТИ
- Мажор и минор, имеющие одинаковые ключевые знаки
- Тоники находятся на расстоянии малой терции
- Общие звуки, общие аккорды
- Пример: До мажор (0 знаков) и Ля минор (0 знаков)

ОДНОИМЕННЫЕ ТОНАЛЬНОСТИ
- Мажор и минор с общей тоникой
- Различаются тремя ступенями: III, VI, VII
- Пример: До мажор (0 знаков) и До минор (3 бемоля)

6. Квинтовый круг тональностей
Квинтовый круг - это схематическое представление всех мажорных и параллельных им минорных тональностей, показывающее степень их родства.

ДИЕЗНЫЕ ТОНАЛЬНОСТИ:
До мажор (0#) 
→ Соль мажор (1#) 
→ Ре мажор (2#) 
→ Ля мажор (3#) 
→ Ми мажор (4#) 
→ Си мажор (5#) 
→ Фа-диез мажор (6#) 
→ До-диез мажор (7#)

БЕМОЛЬНЫЕ ТОНАЛЬНОСТИ:
До мажор (0♭) 
→ Фа мажор (1♭) 
→ Си-бемоль мажор (2♭) 
→ Ми-бемоль мажор (3♭) 
→ Ля-бемоль мажор (4♭) 
→ Ре-бемоль мажор (5♭) 
→ Соль-бемоль мажор (6♭) 
→ До-бемоль мажор (7♭)

ПОРЯДОК ДИЕЗОВ:
Фа-До-Соль-Ре-Ля-Ми-Си

ПОРЯДОК БЕМОЛЕЙ:
Си-Ми-Ля-Ре-Соль-До-Фа

Заключение
Лад и тональность - это фундаментальные принципы, которые организуют музыкальное пространство и время. Они превращают хаотичный набор звуков в осмысленную, эмоционально насыщенную речь.

Понимание ладовой системы позволяет:
- Анализировать музыкальные произведения
- Предсказывать развитие музыкальной мысли
- Создавать собственные композиции
- Глубоко понимать эмоциональное содержание музыки

От простых народных напевов до сложных симфонических полотен - всю музыку объединяет единый принцип ладовой организации, который делает ее универсальным языком человеческих чувств."""

    def get_musical_form_text(self):
        return """МУЗЫКАЛЬНАЯ ФОРМА И АНАЛИЗ

Введение в музыкальную форму
Музыкальная форма - это структура музыкального произведения, способ организации его частей во времени. Понимание формы помогает нам анализировать музыку, исполнять ее осознанно и создавать собственные композиции.

1. Период и предложение
Период
- Это законченная музыкальная мысль, которая представляет собой целостное построение
- Обычно состоит из 8-16 тактов
- Делится на два предложения
- Имеет четкую тональную структуру
- Завершается полной каденцией

Предложение
- Это часть периода, обладающая относительной самостоятельностью
- Первое предложение заканчивается на половинной каденции (часто на доминанте)
- Второе предложение заканчивается на полной каденции (на тонике)
- Каждое предложение обычно состоит из 4-8 тактов
- Предложения могут быть симметричными или асимметричными

2. Простые музыкальные формы
Одночастная форма (A)
- Самая простая музыкальная форма, состоящая из одного периода
- Не делится на самостоятельные разделы
- Часто используется в народных песнях и романсах
- Пример: русская народная песня "Во поле береза стояла"

Двухчастная форма (A-B)
- Форма, состоящая из двух контрастных частей
- Виды: без репризы и с репризой
- Используется в песнях, танцах, инструментальных пьесах

Трехчастная форма (A-B-A)
- Классическая форма с репризой, самая распространенная в музыке
- Структура: экспозиция - контрастная часть - реприза
- Особенности: часть A устойчивая, B неустойчивая, реприза возвращает устойчивость

3. Сложные музыкальные формы
Форма рондо (A-B-A-C-A...)
- Форма, в которой основная тема многократно повторяется
- Рефрен чередуется с контрастными эпизодами
- Создает ощущение движения по кругу
- Часто используется в финалах сонат и симфоний

Форма вариаций (A-A1-A2-A3...)
- Форма, основанная на последовательном изменении основной тема
- Типы: строгие (сохраняют гармонию) и свободные вариации
- Этапы: первые вариации близки к теме, средние - максимальный контраст, финальные - возвращение

Сонатная форма
- Самая развитая и сложная форма классической музыке
- Основные разделы: экспозиция, разработка, реприза
- Характерен конфликт и его разрешение
- Используется в первых частях сонат, симфоний, концертов

4. Анализ музыкальных произведений
Этапы музыкального анализа:
- Общее знакомство: жанр, структура, тематические блоки
- Гармонический анализ: тональный план, каденции, модуляции
- Тематический анализ: мелодические и ритмические особенности
- Фактурный анализ: голосоведение, текстура, инструментовка

Методы анализа:
- Целостный - произведение как единый организм
- Сравнительный - сопоставление разных частей
- Стилистический - особенности стиля композитора

Заключение
Музыкальная форма - это живой организм, развивающийся по своим законам. Понимание формы позволяет видеть логику музыкального развития и создавать целостные произведения."""

    def get_harmony_text(self):
        return """ГАРМОНИЯ И ГОЛОСОВЕДЕНИЕ

Введение в гармонию
Гармония - это фундаментальная дисциплина в музыке, изучающая сочетание звуков в вертикали (аккорды) и их последовательности. Голосоведение - это искусство ведения отдельных голосов в многоголосной музыке.

1. Гармонические последовательности
Определение гармонической последовательности
- Это закономерная смена аккордов, создающая ощущение движения и развития
- Основные типы: автентические, плагальные, полные каденционные

Основные типы последовательностей
Автентические последовательности:
- Доминанта → Тоника (D → T)
- Создают энергичное, решительное движение
- Характерны для классической музыки

Плагальные последовательности:
- Субдоминанта → Тоника (S → T)
- Мягкое, спокойное звучание
- Часто используются в церковной музыке

Полные каденционные последовательности:
- Тоника → Субдоминанта → Доминанта → Тоника (T → S → D → T)
- Наиболее полное и завершенное звучание
- Классическая формула завершения музыкальной мысли

2. Правила голосоведения
Основные принципы движения голосов
Параллельное движение:
- Голоса движутся в одном направлении
- Параллельные октавы и квинты запрещены
- Параллельные терции и сексты разрешены

Противодвижение:
- Голоса движутся в противоположных направлениях
- Создает богатую и независимую фактуру
- Наиболее предпочтительный вид движения

Косвенное движение:
- Один голос остается на месте, другой движется
- Создает плавные переходы между аккордами
- Часто используется в каденциях

3. Каденции и их виды
Определение каденции
- Это гармонический оборот, завершающий музыкальную мысль или ее часть

Основные виды каденций
Полная каденция:
- Доминанта → Тоника (D → T)
- Завершенное, окончательное звучание

Половинная каденция:
- Оканчивается на доминанте
- Создает ощущение вопроса, незавершенности

Плагальная каденция:
- Субдоминанта → Тоника (S → T)
- Мягкое, умиротворенное окончание

Прерванная каденция:
- Доминанта → Не тоника (D → VI ступень)
- Неожиданный поворот, драматический эффект

Заключение
Гармония и голосоведение - это искусство создания выразительного и логичного музыкального целого. Понимание гармонии позволяет анализировать произведения и создавать осмысленные композиции."""

    def get_dictation_text(self):
        return """МУЗЫКАЛЬНЫЙ ДИКТАНТ

Введение в музыкальный диктант
Музыкальный диктант - это важнейший вид работы на уроках сольфеджио, развивающий музыкальный слух, память и мышление. Это процесс записи нотами музыкального материала, воспринимаемого на слух.

1. Одноголосный диктант
Что такое одноголосный диктант
- Это запись одноголосной мелодии, проигрываемой преподавателем
- Базовый навык для любого музыканта

Этапы работы над одноголосным диктантом
Первое прослушивание:
- Определение общего характера мелодии
- Запоминание ритмического рисунка
- Определение размера и темпа
- Выявление тональности и лада

Второе прослушивание:
- Уточнение метроритмической структуры
- Запись ритма без нот
- Определение фразировки и цезур
- Выявление кульминационных точек

Третье и последующие прослушивания:
- Постепенное заполнение нотами
- Проверка интервальных соотношений
- Контроль за точностью записи
- Уточнение деталей

2. Методы развития слуха для диктанта
Систематические тренировки
- Регулярное написание диктантов
- Поэтапное усложнение материала
- Разнообразие тональностей и размеров

Вспомогательные упражнения
- Сольфеджирование - пение с называнием нот
- Определение интервалов и аккордов на слух
- Ритмические упражнения

3. Практические советы
Для начинающих
- Начинайте с простых мелодий в одной тональности
- Сначала записывайте ритм, потом высоту
- Используйте внутреннее слуховое представление

Общие рекомендаций
- Сохранение спокойствия и концентрации
- Создание комфортных условий для работы
- Систематичность занятий

Заключение
Музыкальный диктант - это мощный инструмент развития музыкального сознания. Регулярная работа над диктантом позволяет развить тонкий музыкальный слух и научиться быстро анализировать музыку."""

    def get_solfeggio_text(self):
        return """СОЛЬФЕДЖИО И ВОКАЛИЗЫ

Введение в сольфеджио и вокализы
Сольфеджио и вокализы - это фундаментальные дисциплины в музыкальном образовании, развивающие слух, голос и музыкальное мышление. Они формируют основу профессиональной подготовки музыканта любого направления.

1. Пение интервалов и аккордов
Основные интервалы для пения
Чистые интервалы:
- Прима - повторение одного звука
- Кварта - устойчивый, спокойный интервал
- Квинта - пустой, гармоничный интервал
- Октава - полное слияние звуков

Большие и малые интервалы:
- Секунды - шаговое движение
- Терции - основа мажора и минор
- Сексты - широкие, мелодичные
- Септимы - напряженные, диссонирующие

2. Чтение с листа
Что такое чтение с листа
- Это навык исполнения незнакомой музыки с первого прочтения нотного текста
- Комплексное умение, сочетающее зрительное восприятие и слуховой контроль

Этапы обучения чтению с листа
Начальный уровень:
- Простые мелодии в одной тональности
- Основные длительности без сложных ритмов
- Пение с тактированием

Средний уровень:
- Модуляции и отклонения
- Сложные ритмические фигуры
- Хроматические последования

Продвинутый уровень:
- Полифонические произведения
- Современная нотация
- Транспонирование

3. Интонационные упражнения
Цель интонационных упражнений
- Развитие точности интонирования
- Воспитание ладового чувства
- Совершенствование музыкального слуха

Виды интонационных упражнений
- Упражнения на устойчивые ступени
- Упражнения на вводные тоны
- Хроматические упражнения

Заключение
Сольфеджио и вокализы формируют тонкий музыкальный слух, технически оснащенный голос и глубокое понимание музыкальной структуры. Регулярная работа открывает путь к свободному владению музыкальным языком."""


def main():
    root = tk.Tk()
    
    # Устанавливаем иконку (если есть файл)
    try:
        root.iconbitmap('icon.ico')
    except:
        pass
    
    # Центрируем окно
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    app = SolfeggioApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
