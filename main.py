import tkinter as tk
from tkinter import ttk, PhotoImage, messagebox
import os

class Pomodoro:
    def __init__(self, root):
        self.root = root
        self.root.title("Relógio Pomodoro")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        self.time_options = {
            "Clássico (25/5)": (25, 5),
            "Focado (45/15)": (45, 15),
            "Extensivo (50/10)": (50, 10),
            "Personalizado": None
        }

        self.initial_study_time = 25 * 60
        self.initial_break_time = 5 * 60
        self.current_time = self.initial_study_time
        self.is_study_time = True
        self.is_running = False
        self.timer_id = None

        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(script_dir, "bg-img.jpg")
            self.bg_image = PhotoImage(file=image_path)
            self.bg_label = ttk.Label(self.root, image=self.bg_image)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except tk.TclError:
            print('Erro ao carregar a imagem de fundo. Certifique-se de que o arquivo "bg-img.png" está no diretório correto.')

            self.root.configure(bg="#2c3e50")
        
        
        controls_frame = tk.Frame(root, bg="#34495e", bd=5)
        controls_frame.place(relx=0.5, rely=0.1, anchor="n")

        time_label = tk.Label(controls_frame, text="Selecione um ciclo: ", font=("Inter", 12), bg="#34495e", fg="white")
        time_label.pack(pady=5)

        self.time_select = ttk.Combobox(controls_frame, values=list(self.time_options.keys()), state="readonly", font=("Inter", 10))
        self.time_select.current(0)
        self.time_select.pack(pady=5)
        self.time_select.bind("<<ComboboxSelected>>", self.update_time_selection)

        self.custom_time_frame= tk.Frame(controls_frame, bg="#34495e")
        self.custom_study_label = tk.Label(self.custom_time_frame, text="Estudo (min):", font=("Inter", 10), bg="#34495e", fg="white")
        self.custom_study_label.pack(side="left", padx=(0, 5))
        self.custom_study_entry = tk.Entry(self.custom_time_frame, font=("Inter", 10), width=5)
        self.custom_study_entry.pack(side="left")

        self.custom_break_label = tk.Label(self.custom_time_frame, text="Pausa (min): ", font=("Inter", 10), bg="#34495e", fg="white")
        self.custom_break_label.pack(side="left", padx=(10, 5))
        self.custom_break_entry = tk.Entry(self.custom_time_frame, width=5, font=("Inter", 10))
        self.custom_break_entry.pack(side="left")

        self.set_custom_time_button = tk.Button(self.custom_time_frame, text="Definir", font=("inter", 10), command=self.set_custom_time)
        self.set_custom_time_button.pack(side="left", padx=10)

        self.timer_label = tk.Label(root, text=self.format_time(self.current_time), font=("Inter", 90, "bold"), fg="#e74c3c", bg="#2c3e50")
        self.timer_label.place(relx=0.5, rely=0.5, anchor="center")

        self.status_label = tk.Label(root, text="Tempo de Estudo", font=("Inter", 20, "italic"), fg="white", bg="#2c3e50")
        self.status_label.place(relx=0.5, rely=0.62, anchor="center")

        button_frame = tk.Frame(root, bg="#34495e")
        button_frame.place(relx=0.5, rely=0.85, anchor="center")

        self.start_pause_button = tk.Button(button_frame, text="Iniciar", font=("Inter", 14), command=self.start_pause_timer)
        self.start_pause_button.pack(side="left", padx=10)
        
        self.stop_button = tk.Button(button_frame, text="Encerrar", font=("Inter", 14), command=self.stop_timer)
        self.stop_button.pack(side="left", padx=10)


    def update_time_selection(self, event):
            selection = self.time_select.get()
            if selection == "Personalizado":
                self.custom_time_frame.pack(pady=10)
            else:
                self.custom_time_frame.pack_forget()
                study_minutes, break_minutes = self.time_options[selection]
                self.initial_study_time = study_minutes * 60
                self.initial_break_time = break_minutes * 60
                self.reset_timer()

    def set_custom_time(self):
            try:
                study_minutes = int(self.custom_study_entry.get())
                break_minutes = int(self.custom_break_entry.get())
                if study_minutes > 0 and break_minutes > 0:
                    self.initial_study_time = study_minutes * 60
                    self.initial_break_time = break_minutes * 60
                    self.reset_timer()
                else:
                    messagebox.showerror("Erro de entrada", "Os tempos de estudo e pausa devem ser maiores que zero.")
                
            except ValueError:
                messagebox.showerror("Erro de entrada", "Por favor, insira números inteiros válidos para os tempos.")

    def format_time(self, seconds):
            minutes = seconds // 60
            seconds = seconds % 60
            return f"{minutes:02d}:{seconds:02d}"

    def start_pause_timer(self):
            if self.is_running:
                self.is_running = False
                self.start_pause_button.config(text="Continuar")
                if self.timer_id:
                    self.root.after_cancel(self.timer_id)
            else:
                self.is_running = True
                self.start_pause_button.config(text="Pausar")
                self.countdown()

    def stop_timer(self):
            self.reset_timer()
        
    def reset_timer(self):
            if self.timer_id:
                self.root.after_cancel(self.timer_id)
                self.timer_id = None
            self.is_running = False
            self.is_study_time = True
            self.current_time = self.initial_study_time

            self.start_pause_button.config(text="Iniciar")
            self.timer_label.config(text=self.format_time(self.current_time), fg="#e74c3c")
            self.status_label.config(text="Tempo de Estudo")

    def countdown(self):
            if self.is_running:
                if self.current_time >= 0:
                    self.timer_label.config(text=self.format_time(self.current_time))
                    self.current_time -= 1
                    self.timer_id = self.root.after(1000, self.countdown)
                else:
                    self.switch_mode()
        
    def switch_mode(self):
            self.is_study_time = not self.is_study_time

            if self.is_study_time:
                self.current_time = self.initial_study_time
                self.timer_label.config(fg="#e74c3c")
                self.status_label.config(text="Tempo de Estudo")
            else:
                self.current_time = self.initial_break_time
                self.timer_label.config(fg="#2ecc71")
                self.status_label.config(text="Tempo de Pausa")

            self.countdown()

if __name__ == "__main__":
    root = tk.Tk()
    app = Pomodoro(root)
    root.mainloop()












