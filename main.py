import tkinter as tk
from tkinter import ttk, messagebox
import json

class TodoListApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("────୨ TO-DO ৎ────")
        self.geometry("400x450")
        self.configure(bg="#FFC0CB")
        
        # Configurar estilo
        style = ttk.Style()
        style.theme_use('clam')
        
        # Personalizar botones
        style.configure('TButton', 
                       background="#D8BDC2",
                       foreground='#000000',
                       borderwidth=1,
                       focuscolor='none',
                       padding=5)
        style.map('TButton',
                 background=[('active', '#FFB6C1')])

        # Frame principal con color de fondo
        main_frame = tk.Frame(self, bg="#FFFFFF", padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # El campo input para agregar las tareas
        self.task_input = tk.Entry(main_frame, font=("Arial", 14), width=35,
                                    bg="#FFFFFF", fg="#000000",
                                    insertbackground="#000000",
                                    borderwidth=2, relief="solid")
        self.task_input.pack(pady=10)

        # Placeholder
        self.task_input.insert(0, "Ingresa tu pendiente aqui...")
        self.task_input.config(foreground="gray")
        self.task_input.bind("<FocusIn>", self.clear_placeholder)
        self.task_input.bind("<FocusOut>", self.restore_placeholder)
        self.task_input.bind("<Return>", lambda e: self.add_task())

        # Boton para agregar las tareas
        ttk.Button(main_frame, text="➕ Agregar Tarea", 
                   command=self.add_task).pack(pady=5)

        # Frame para la lista
        list_frame = tk.Frame(main_frame, bg="#FFFFFF")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Scrollbar
        scrollbar = tk.Scrollbar(list_frame, bg="#FFC0CB", troughcolor="#FFFFFF")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Crear la lista para poner las tareas
        self.task_list = tk.Listbox(list_frame, font=("Arial", 12), 
                                     height=12, selectmode=tk.SINGLE,
                                     yscrollcommand=scrollbar.set,
                                     bg="#FFFFFF", fg="#000000",
                                     selectbackground="#FFC0CB",
                                     selectforeground="#000000",
                                     borderwidth=2, relief="solid")
        self.task_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.task_list.yview)

        # Frame para botones
        button_frame = tk.Frame(main_frame, bg="#FFFFFF")
        button_frame.pack(fill=tk.X, pady=5)

        # Botones
        ttk.Button(button_frame, text="✓ Completar", 
                   command=self.mark_done).pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        ttk.Button(button_frame, text="✗ Eliminar", 
                   command=self.delete_task).pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        ttk.Button(button_frame, text="☆ Estadísticas", 
                   command=self.view_stats).pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
        self.load_tasks()

    def view_stats(self):
        done_count = 0
        total_count = self.task_list.size()
        for i in range(total_count):
            if self.task_list.itemcget(i, "fg") == "#FFC0CB":
                done_count += 1
        
        pending = total_count - done_count
        message = f"౨ৎ Total de Tareas: {total_count}\n✓ Completas: {done_count}\n⚠︎ Pendientes: {pending}"
        messagebox.showinfo("Estadísticas", message)
    
    def add_task(self):
        task = self.task_input.get()
        if task != "Ingresa tu pendiente aqui..." and task.strip():
            self.task_list.insert(tk.END, task)
            self.task_list.itemconfig(tk.END, fg="#000000")
            self.task_input.delete(0, tk.END)
            self.restore_placeholder(None)
            self.save_tasks()

    def mark_done(self):
        task_index = self.task_list.curselection()
        if task_index:
            self.task_list.itemconfig(task_index, fg="#FFC0CB")
            self.save_tasks()
        else:
            messagebox.showwarning("Aviso", "Selecciona una tarea primero")

    def delete_task(self):
        task_index = self.task_list.curselection()
        if task_index:
            self.task_list.delete(task_index)
            self.save_tasks()
        else:
            messagebox.showwarning("Aviso", "Selecciona una tarea primero")
    
    def clear_placeholder(self, event):
        if self.task_input.get() == "Ingresa tu pendiente aqui...":
            self.task_input.delete(0, tk.END)
            self.task_input.config(foreground="#000000")
    
    def restore_placeholder(self, event):
        if self.task_input.get() == "":
            self.task_input.insert(0, "Ingresa tu pendiente aqui...")
            self.task_input.config(foreground="gray")
    
    def load_tasks(self):
        try:
            with open("tasks.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                for task in data:
                    self.task_list.insert(tk.END, task["text"])
                    self.task_list.itemconfig(tk.END, fg=task["color"])
        except FileNotFoundError:
            pass
    
    def save_tasks(self):
        data = []
        for i in range(self.task_list.size()):
            text = self.task_list.get(i)
            color = self.task_list.itemcget(i, "fg")
            data.append({"text": text, "color": color})
        with open("tasks.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    app = TodoListApp()
    app.mainloop()