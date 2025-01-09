from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
import sqlite3

class ToDoApp(App):
    def build(self):
        self.tasks = []
        self.init_db()
        
        self.main_layout = BoxLayout(orientation='vertical')
        
        self.input_box = TextInput(hint_text='Enter task')
        self.main_layout.add_widget(self.input_box)
        
        self.category_box = TextInput(hint_text='Category')
        self.main_layout.add_widget(self.category_box)
        
        self.due_date_box = TextInput(hint_text='Due Date (YYYY-MM-DD)')
        self.main_layout.add_widget(self.due_date_box)
        
        self.add_button = Button(text='Add Task', on_press=self.add_task)
        self.main_layout.add_widget(self.add_button)
        
        self.task_list = BoxLayout(orientation='vertical', size_hint_y=None)
        self.task_list.bind(minimum_height=self.task_list.setter('height'))
        self.scroll_view = ScrollView(size_hint=(1, None), size=(400, 600))
        self.scroll_view.add_widget(self.task_list)
        
        self.main_layout.add_widget(self.scroll_view)
        
        self.display_tasks()
        
        return self.main_layout

    def init_db(self):
        conn = sqlite3.connect('todo.db')
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            category TEXT,
            due_date TEXT,
            completed BOOLEAN NOT NULL DEFAULT 0
        )
        ''')
        conn.commit()
        conn.close()

    def add_task(self, instance):
        task_text = self.input_box.text
        category_text = self.category_box.text
        due_date_text = self.due_date_box.text
        if task_text:
            conn = sqlite3.connect('todo.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO todos (task, category, due_date) VALUES (?, ?, ?)", (task_text, category_text, due_date_text))
            conn.commit()
            conn.close()
            self.display_tasks()
            self.input_box.text = ''
            self.category_box.text = ''
            self.due_date_box.text = ''

    def display_tasks(self):
        self.task_list.clear_widgets()
        
        conn = sqlite3.connect('todo.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM todos")
        rows = cursor.fetchall()
        conn.close()
        
        for row in rows:
            task_label = Label(text=row[1], size_hint_y=None, height=40)
            self.task_list.add_widget(task_label)
            if row[2]:
                category_label = Label(text=f"Category: {row[2]}", size_hint_y=None, height=20)
                self.task_list.add_widget(category_label)
            if row[3]:
                due_date_label = Label(text=f"Due: {row[3]}", size_hint_y=None, height=20)
                self.task_list.add_widget(due_date_label)

if __name__ == '__main__':
    ToDoApp().run()
