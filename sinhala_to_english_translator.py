import tkinter as tk
from tkinter import ttk
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# Load the pre-trained translation model
model_name = "facebook/m2m100_418M"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Default translation direction (Sinhala to English)
source_lang = "si"  # Sinhala
target_lang = "en"  # English

# Function to translate text in the current direction
def translate_text(text):
    tokenizer.src_lang = source_lang
    inputs = tokenizer(text, return_tensors="pt", padding=True)
    translated_tokens = model.generate(**inputs, forced_bos_token_id=tokenizer.lang_code_to_id[target_lang])
    translation = tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)
    return translation[0]

# Function to update the translation in the target text box
def update_translation(event=None):
    input_text = input_textbox.get("1.0", tk.END).strip()  # Get input text
    if input_text:
        translated_text = translate_text(input_text)
        output_textbox.delete("1.0", tk.END)  # Clear the output text box
        output_textbox.insert(tk.END, translated_text)  # Insert translation

# Function to toggle translation direction
def toggle_direction():
    global source_lang, target_lang
    if source_lang == "si":  # If currently Sinhala to English, switch to English to Sinhala
        source_lang, target_lang = "en", "si"
        input_label.config(text="English Text:")
        output_label.config(text="Sinhala Translation:")
    else:  # If currently English to Sinhala, switch to Sinhala to English
        source_lang, target_lang = "si", "en"
        input_label.config(text="Sinhala Text:")
        output_label.config(text="English Translation:")
    # Clear both text boxes when toggling direction
    input_textbox.delete("1.0", tk.END)
    output_textbox.delete("1.0", tk.END)

# Updated text actions: copy, paste, and cut functions
def copy_text(textbox):
    selected_text = textbox.get(tk.SEL_FIRST, tk.SEL_LAST)
    root.clipboard_clear()
    root.clipboard_append(selected_text)

def paste_text(textbox):
    try:
        clipboard_text = root.clipboard_get()
        textbox.insert(tk.INSERT, clipboard_text)
    except tk.TclError:
        pass  # If there's nothing in the clipboard, do nothing

def cut_text(textbox):
    copy_text(textbox)
    textbox.delete(tk.SEL_FIRST, tk.SEL_LAST)

# Toggle between Light Mode and Dark Mode
def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode

    if dark_mode:
        # Dark Mode Colors
        root.configure(bg="#2E2E2E")
        title_label.config(bg="#1F1F1F", fg="#FFFFFF")
        input_label.config(bg="#2E2E2E", fg="#FFFFFF")
        output_label.config(bg="#2E2E2E", fg="#FFFFFF")
        toggle_theme_button.config(text="Light Mode", bg="#4A4A4A", fg="black")
        style.configure("Custom.TButton", background="#4A4A4A", foreground="black")
        input_textbox.config(bg="#333333", fg="#FFFFFF", insertbackground="white")
        output_textbox.config(bg="#333333", fg="#FFFFFF", insertbackground="white")
    else:
        # Light Mode Colors
        root.configure(bg="#f3f8fb")
        title_label.config(bg="#007acc", fg="#FFFFFF")
        input_label.config(bg="#f3f8fb", fg="#333333")
        output_label.config(bg="#f3f8fb", fg="#333333")
        toggle_theme_button.config(text="Dark Mode", bg="#D3D3D3", fg="black")
        style.configure("Custom.TButton", background="#D3D3D3", foreground="black")
        input_textbox.config(bg="white", fg="black", insertbackground="black")
        output_textbox.config(bg="white", fg="black", insertbackground="black")

# Create the main GUI window
root = tk.Tk()
root.title("Sinhala-English Translator")
root.geometry("500x500")  # Fixed window size
root.resizable(False, False)  # Prevent resizing to keep layout fixed

# Set initial theme to Light Mode
dark_mode = False

# Styling options
label_font = ("Helvetica", 12, "bold")
textbox_font = ("Helvetica", 10)
button_font = ("Helvetica", 10)
title_font = ("Helvetica", 14, "bold")

# Title label for the app
title_label = tk.Label(
    root,
    text="Sinhala-English Translator",
    font=title_font,
    bg="#007acc",
    fg="white",
    padx=10,
    pady=10,
)
title_label.pack(fill="x")

# Theme toggle button in top-right corner
toggle_theme_button = tk.Button(root, text="Dark Mode", command=toggle_theme, font=("Helvetica", 10), bg="#D3D3D3", fg="black")
toggle_theme_button.place(relx=0.9, rely=0.02, anchor="ne")

# Create and style the input text box with a scrollbar
input_label = tk.Label(root, text="Sinhala Text:", font=label_font, bg="#f3f8fb", fg="#333333")
input_label.pack(pady=(10, 0), anchor="w", padx=10)

input_frame = tk.Frame(root, bg="#f3f8fb")
input_frame.pack(padx=10, pady=5, fill="x")

input_scrollbar = tk.Scrollbar(input_frame, orient="vertical")
input_textbox = tk.Text(input_frame, height=6, font=textbox_font, wrap="word", yscrollcommand=input_scrollbar.set, relief="solid", bd=1)
input_textbox.pack(side="left", fill="both", expand=True)
input_scrollbar.config(command=input_textbox.yview)
input_scrollbar.pack(side="right", fill="y")

# Add copy, paste, cut buttons for input text box
button_frame = tk.Frame(root, bg="#f3f8fb")
button_frame.pack(pady=5)
ttk.Button(button_frame, text="Copy", command=lambda: copy_text(input_textbox), style="Custom.TButton").grid(row=0, column=0, padx=5)
ttk.Button(button_frame, text="Paste", command=lambda: paste_text(input_textbox), style="Custom.TButton").grid(row=0, column=1, padx=5)
ttk.Button(button_frame, text="Cut", command=lambda: cut_text(input_textbox), style="Custom.TButton").grid(row=0, column=2, padx=5)

# Add a rotation button to switch translation direction
rotate_button = ttk.Button(root, text="Swap Languages", command=toggle_direction, style="Custom.TButton")
rotate_button.pack(pady=10)

# Create and style the output translation text box with a scrollbar
output_label = tk.Label(root, text="English Translation:", font=label_font, bg="#f3f8fb", fg="#333333")
output_label.pack(pady=(10, 0), anchor="w", padx=10)

output_frame = tk.Frame(root, bg="#f3f8fb")
output_frame.pack(padx=10, pady=5, fill="x")

output_scrollbar = tk.Scrollbar(output_frame, orient="vertical")
output_textbox = tk.Text(output_frame, height=6, font=textbox_font, wrap="word", yscrollcommand=output_scrollbar.set, relief="solid", bd=1)
output_textbox.pack(side="left", fill="both", expand=True)
output_scrollbar.config(command=output_textbox.yview)
output_scrollbar.pack(side="right", fill="y")

# Add copy, paste, cut buttons for output text box
output_button_frame = tk.Frame(root, bg="#f3f8fb")
output_button_frame.pack(pady=5)
ttk.Button(output_button_frame, text="Copy", command=lambda: copy_text(output_textbox), style="Custom.TButton").grid(row=0, column=0, padx=5)
ttk.Button(output_button_frame, text="Paste", command=lambda: paste_text(output_textbox), style="Custom.TButton").grid(row=0, column=1, padx=5)
ttk.Button(output_button_frame, text="Cut", command=lambda: cut_text(output_textbox), style="Custom.TButton").grid(row=0, column=2, padx=5)

# Add a translate button at the bottom
translate_button = ttk.Button(root, text="Translate", command=update_translation, style="Custom.TButton")
translate_button.pack(pady=10)

# Bind the input text box to update translation on any key press
input_textbox.bind("<KeyRelease>", update_translation)

# Style for custom button
style = ttk.Style(root)
style.configure("Custom.TButton", font=button_font, padding=6, background="#D3D3D3", foreground="black")
style.map("Custom.TButton", background=[("active", "#A9A9A9")], foreground=[("active", "black")])

# Initial theme setup (Light Mode by default)
toggle_theme()

# Run the application
root.mainloop()
