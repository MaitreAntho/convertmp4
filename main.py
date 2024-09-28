import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from moviepy.editor import VideoFileClip
import threading
import time

window = tk.Tk()
window.title("Convertisseur Vidéo en MP4")
window.geometry("600x300")
window.config(bg="#0a0f25")

progress_var = tk.DoubleVar()
selected_file = None

def convertir_video():
    global selected_file
    if selected_file:
        try:
            convert_button.config(state=tk.DISABLED, text="Conversion en cours...")
            progress_bar.start()
            file_label.config(text="Conversion en cours...")
            select_button.pack_forget()

            clip = VideoFileClip(selected_file)
            duration = clip.duration 
            
            output_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
            if not output_path:
                reset_interface()
                return
            
            start_time = time.time()

            clip.write_videofile(output_path, codec='libx264', audio_codec='aac')

            elapsed_time = time.time() - start_time
            estimated_time_label.config(text=f"Temps de conversion : {int(elapsed_time)} secondes")

            messagebox.showinfo("Succès", "La vidéo a été convertie avec succès !")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la conversion : {e}")
        finally:
            reset_interface()
    else:
        messagebox.showwarning("Avertissement", "Veuillez d'abord sélectionner une vidéo.")

def reset_interface():
    progress_bar.stop()
    progress_var.set(0)
    convert_button.config(state=tk.NORMAL, text="Convertir")
    file_label.config(text="Aucune vidéo sélectionnée")
    select_button.pack(pady=10)

def select_file():
    global selected_file
    selected_file = filedialog.askopenfilename(filetypes=[("Tous fichiers vidéo", "*.mp4 *.avi *.mov *.mkv")])
    if selected_file:
        file_label.config(text=f"Vidéo sélectionnée : {selected_file.split('/')[-1]}")
        convert_button.pack(pady=10)
        estimated_time_label.config(text="")

progress_bar = ttk.Progressbar(window, variable=progress_var, maximum=100, mode='indeterminate')
progress_bar.pack(pady=10, padx=20, fill="x")

file_label = tk.Label(window, text="Aucune vidéo sélectionnée", bg="#0a0f25", fg="white", font=("Helvetica", 12))
file_label.pack(pady=10)

estimated_time_label = tk.Label(window, text="", bg="#0a0f25", fg="#00ff6a", font=("Helvetica", 12, "bold"))
estimated_time_label.pack(pady=5)

select_button = tk.Button(window, text="Sélectionner une vidéo", command=select_file, bg="#00ff6a", fg="black", font=("Helvetica", 12, "bold"), relief="raised", borderwidth=2, padx=20, pady=5)
select_button.pack(pady=10)

convert_button = tk.Button(window, text="Convertir", command=lambda: threading.Thread(target=convertir_video).start(), bg="#0052cc", fg="white", font=("Helvetica", 12, "bold"), relief="raised", borderwidth=2, padx=20, pady=5)
convert_button.pack_forget()

window.mainloop()
