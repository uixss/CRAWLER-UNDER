import asyncio
import os
import pickle
import customtkinter as ctk
from tkinter import filedialog
import ctypes
from telethon import TelegramClient, functions, types, errors
from PIL import Image, ImageTk
import requests

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
BACKGROUND_COLOR = "#262626"
FOREGROUND_COLOR = "#333333"
TEXT_COLOR = "#E5E5E5"
BUTTON_COLOR = "#d9534f"
HOVER_COLOR = "#c9302c"
CHECKBOX_BORDER_COLOR = "#262626"
CHECKBOX_HOVER_COLOR = "#262626"
LOGO_PATH = "undermain.png"

def validate_token_and_chat_id(token, chat_id):
    return token and chat_id and token.strip() != "" and chat_id.strip() != ""

def test_bot():
    token = input1.get().strip()
    chat_id = input2.get().strip()
    if not validate_token_and_chat_id(token, chat_id):
        write_to_console("Bot token y chat ID deben estar completos.")
        return
    
    message = "Mensaje de prueba desde el bot."
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    params = {"chat_id": chat_id, "text": message}
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            write_to_console("Mensaje de prueba enviado exitosamente.")
        else:
            write_to_console(f"Error al enviar mensaje: {response.json().get('description', 'Error desconocido')}")
    except requests.exceptions.RequestException as e:
        write_to_console(f"Error de conexión: {e}")

def create_main_window():
    root = ctk.CTk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = int(screen_width * 0.3)
    window_height = int(screen_height * 0.45)
    root.geometry(f"{window_width}x{window_height}")
    root.title("𝐒𝐇𝐈𝐓 𝐔𝐍𝐃𝐄𝐑 💀")
    root.configure(bg=BACKGROUND_COLOR)
    root.resizable(False, False)
    root.overrideredirect(True)
    root.wm_attributes('-alpha', 0.92)
    return root

def load_logo(frame):
    if os.path.exists(LOGO_PATH):
        logo_image = Image.open(LOGO_PATH).resize((100, 100), Image.LANCZOS)
        logo_image_tk = ImageTk.PhotoImage(logo_image)
        logo_canvas = ctk.CTkCanvas(frame, width=100, height=100, bg=BACKGROUND_COLOR, highlightthickness=0)
        logo_canvas.create_image(50, 50, image=logo_image_tk)
        logo_canvas.image = logo_image_tk
        logo_canvas.pack(side="right", padx=(0, 35))

def select_path():
    filepath = filedialog.askdirectory()
    if filepath:
        path_entry.delete(0, ctk.END)
        path_entry.insert(0, filepath)

def write_to_console(message):
    console_text.configure(state="normal")
    console_text.insert(ctk.END, f"{message}\n")
    console_text.configure(state="disabled")
    console_text.see(ctk.END)

def run_action():
    token = input1.get().strip()
    chat_id = input2.get().strip()

    checkbox_values = {
        "LOGS": checkbox1_var.get(),
        "LEADS": checkbox2_var.get(),
        "LOGS DE 3": checkbox3_var.get(),
        "SMTP": check_button_var.get(),
        "OFFICE365": dependent_checkboxes[0].cget("state") == "normal" and dependent_checkboxes[0].get(),
        "GMAIL": dependent_checkboxes[1].cget("state") == "normal" and dependent_checkboxes[1].get(),
        "EXTRA": dependent_checkboxes[2].cget("state") == "normal" and dependent_checkboxes[2].get(),

    }
    write_to_console(f"Token: {token}")
    write_to_console(f"Chat ID: {chat_id}")
    for name, selected in checkbox_values.items():
        write_to_console(f"{name}: {'ON' if selected else 'OFF'}")
        
def stop_action():
    write_to_console("Acción detenida.")

def toggle_checkboxes():
    state = "normal" if check_button_var.get() else "disabled"
    for checkbox in dependent_checkboxes:
        checkbox.configure(state=state)

def enable_window_dragging(root):
    def start_move(event):
        root.x, root.y = event.x, event.y
    def stop_move(event):
        root.x, root.y = None, None
    def on_motion(event):
        x = root.winfo_x() + (event.x - root.x)
        y = root.winfo_y() + (event.y - root.y)
        root.geometry(f"+{x}+{y}")
    root.bind("<ButtonPress-1>", start_move)
    root.bind("<ButtonRelease-1>", stop_move)
    root.bind("<B1-Motion>", on_motion)

def toggle_checkboxes_col3():
    state = "normal" if check_button_var_col3.get() else "disabled"
    for checkbox in dependent_checkboxes_col3:
        checkbox.configure(state=state)

root = create_main_window()
top_frame = ctk.CTkFrame(root, fg_color=BACKGROUND_COLOR)
top_frame.pack(fill="x", padx=10, pady=(10, 5))
load_logo(top_frame)

path_entry = ctk.CTkEntry(top_frame, width=300, placeholder_text="Selecciona una ruta", font=("Arial", 12))
path_entry.pack(side="left", padx=(10, 10), fill="x", expand=True)
path_button = ctk.CTkButton(top_frame, text="...", command=select_path, fg_color=BUTTON_COLOR, hover_color=HOVER_COLOR)
path_button.pack(side="right", fill="x", padx=(20, 20))

input1 = ctk.CTkEntry(root, placeholder_text="ENTER TOKEN BOT", font=("Arial", 12))
input1.pack(fill="x", padx=20, pady=(20, 5), before=top_frame)
input2 = ctk.CTkEntry(root, placeholder_text="ENTER CHAT ID", font=("Arial", 12))
input2.pack(fill="x", padx=20, pady=(5, 10), before=top_frame)

bottom_frame = ctk.CTkFrame(root, fg_color=BACKGROUND_COLOR)
bottom_frame.pack(fill="both", expand=True, padx=10, pady=(10, 0))
bottom_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

col1_frame = ctk.CTkFrame(bottom_frame, fg_color="#262626", corner_radius=10)
col1_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
checkbox1_var = ctk.BooleanVar()
checkbox2_var = ctk.BooleanVar()
checkbox3_var = ctk.BooleanVar()
checkboxes = [
    ctk.CTkCheckBox(col1_frame, text="LOGS", variable=checkbox1_var, text_color=TEXT_COLOR, font=("Arial", 10), border_color=CHECKBOX_BORDER_COLOR, hover_color=CHECKBOX_HOVER_COLOR, fg_color=FOREGROUND_COLOR),
    ctk.CTkCheckBox(col1_frame, text="LOGS DE 3", variable=checkbox3_var, text_color=TEXT_COLOR, font=("Arial", 10), border_color=CHECKBOX_BORDER_COLOR, hover_color=CHECKBOX_HOVER_COLOR, fg_color=FOREGROUND_COLOR)
]
for i, checkbox in enumerate(checkboxes):
    checkbox.grid(row=i, column=0, sticky="nsew", pady=5)
col2_frame = ctk.CTkFrame(bottom_frame, fg_color="#262626", corner_radius=10)
col2_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
check_button_var = ctk.BooleanVar()
check_button = ctk.CTkCheckBox(col2_frame, text="SMTP", variable=check_button_var, command=toggle_checkboxes, text_color=TEXT_COLOR, font=("Arial", 10, "bold"))
check_button.grid(row=0, column=0, sticky="nsew", pady=5)

dependent_checkboxes = [
    ctk.CTkCheckBox(col2_frame, text="OFFICE365", state="disabled", text_color=TEXT_COLOR, font=("Arial", 10), border_color=CHECKBOX_BORDER_COLOR, hover_color=CHECKBOX_HOVER_COLOR, fg_color=FOREGROUND_COLOR),
    ctk.CTkCheckBox(col2_frame, text="GMAIL", state="disabled", text_color=TEXT_COLOR, font=("Arial", 10), border_color=CHECKBOX_BORDER_COLOR, hover_color=CHECKBOX_HOVER_COLOR, fg_color=FOREGROUND_COLOR),
    ctk.CTkCheckBox(col2_frame, text="EXTRA", state="disabled", text_color=TEXT_COLOR, font=("Arial", 10), border_color=CHECKBOX_BORDER_COLOR, hover_color=CHECKBOX_HOVER_COLOR, fg_color=FOREGROUND_COLOR)
]
for i, checkbox in enumerate(dependent_checkboxes, start=1):
    checkbox.grid(row=i, column=0, sticky="nsew", pady=5)

col3_frame = ctk.CTkFrame(bottom_frame, fg_color="#262626", corner_radius=10)
col3_frame.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")
check_button_var_col3 = ctk.BooleanVar()
check_button_col3 = ctk.CTkCheckBox(col3_frame, text="LEADS", variable=check_button_var_col3, command=toggle_checkboxes, text_color=TEXT_COLOR, font=("Arial", 10, "bold"))
check_button_col3.grid(row=0, column=0, sticky="nsew", pady=5)

dependent_checkboxes_col3 = [
    ctk.CTkCheckBox(col3_frame, text="HOTMAIL", state="disabled", text_color=TEXT_COLOR, font=("Arial", 10), border_color=CHECKBOX_BORDER_COLOR, hover_color=CHECKBOX_HOVER_COLOR, fg_color=FOREGROUND_COLOR),
    ctk.CTkCheckBox(col3_frame, text="GMAIL", state="disabled", text_color=TEXT_COLOR, font=("Arial", 10), border_color=CHECKBOX_BORDER_COLOR, hover_color=CHECKBOX_HOVER_COLOR, fg_color=FOREGROUND_COLOR),
    ctk.CTkCheckBox(col3_frame, text="EXTRA", state="disabled", text_color=TEXT_COLOR, font=("Arial", 10), border_color=CHECKBOX_BORDER_COLOR, hover_color=CHECKBOX_HOVER_COLOR, fg_color=FOREGROUND_COLOR)
]
for i, checkbox in enumerate(dependent_checkboxes_col3, start=1):
    checkbox.grid(row=i, column=0, sticky="nsew", pady=5)

check_button_col3.configure(command=toggle_checkboxes_col3)
col4_frame = ctk.CTkFrame(bottom_frame, fg_color="#262626", corner_radius=10)
col4_frame.grid(row=0, column=3, padx=5, pady=5, sticky="nsew")
run_button = ctk.CTkButton(col4_frame, text="RUN", fg_color="#3A3A4D", hover_color="#3A3A4D", font=("Arial", 12, "bold"), command=run_action, width=100)
run_button.pack(pady=(10, 0))
stop_button = ctk.CTkButton(col4_frame, text="STOP", fg_color="#3A3A4D", hover_color="#3A3A4D", font=("Arial", 12, "bold"), command=stop_action, width=100)
stop_button.pack(pady=(5, 5))
testbot = ctk.CTkButton(col4_frame, text="TEST BOT", fg_color="#3A3A4D", hover_color="#3A3A4D", font=("Arial", 12, "bold"), command=test_bot, width=100)
testbot.pack()

console_frame = ctk.CTkFrame(root, fg_color=BACKGROUND_COLOR, corner_radius=5)
console_frame.pack(fill="both", padx=10, pady=(0, 10), expand=True)
console_text = ctk.CTkTextbox(console_frame, wrap="word", font=("Arial", 10), fg_color=FOREGROUND_COLOR)
console_text.pack(expand=True, fill="both", padx=5, pady=5)

enable_window_dragging(root)
root.mainloop()
