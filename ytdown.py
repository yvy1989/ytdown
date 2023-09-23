import tkinter as tk
import tkinter.filedialog as filedialog
import threading
import yt_dlp as youtube_dl

def selecionar_diretorio():
    diretorio_destino = filedialog.askdirectory()
    if diretorio_destino:
        diretorio_entry.delete(0, tk.END)
        diretorio_entry.insert(0, diretorio_destino)

def baixar_video():
    url = url_entry.get()
    diretorio_destino = diretorio_entry.get()
    baixar_apenas_audio = baixar_apenas_audio_var.get()

    if not url:
        status_label.config(text="Please insert an URL.")
        return

    if not diretorio_destino:
        status_label.config(text="Please select a destination directory.")
        return

    ydl_opts = {
        'outtmpl': f'{diretorio_destino}/%(title)s.%(ext)s',
        'progress_hooks': [download_progress_hook],
        'format': 'bestaudio' if baixar_apenas_audio else 'best',
    }

    ydl = youtube_dl.YoutubeDL(ydl_opts)

    def download():
        try:
            with ydl:
                ydl.download([url])
                status_label.config(text="Download finished!")
                progress_bar.stop()
                abrir_pasta(diretorio_destino)
        except Exception as e:
            status_label.config(text=f"Erro: {str(e)}")
            progress_bar.stop()

    progress_bar.start()
    download_thread = threading.Thread(target=download)
    download_thread.start()

def download_progress_hook(d):
    if d['status'] == 'downloading':
        progress = d['_percent_str']
        status_label.config(text=f"Downloading: {progress}")
        try:
            progress_value = int(d['_percent_str'].strip('%').split('.')[0])
            progress_bar['value'] = progress_value
        except ValueError:
            pass

def abrir_pasta(diretorio):
    try:
        import os
        os.startfile(diretorio)  # Abre o diretório no sistema padrão do sistema operacional
    except AttributeError:
        import subprocess
        subprocess.Popen(['xdg-open', diretorio])  # Tente abrir a pasta no Linux
    except Exception as e:
        print(f"Error on open folder: {str(e)}")

root = tk.Tk()
root.title("YouTube Downloader")

# Defina as dimensões da janela em pixels
window_width = 400
window_height = 400
root.geometry(f"{window_width}x{window_height}")

url_label = tk.Label(root, text="Video URL:")
url_label.pack()

url_entry = tk.Entry(root, width=40)
url_entry.pack()

diretorio_label = tk.Label(root, text="Destination directory:")
diretorio_label.pack()

diretorio_entry = tk.Entry(root, width=40)
diretorio_entry.pack()

selecionar_diretorio_button = tk.Button(root, text="Select Directory", command=selecionar_diretorio)
selecionar_diretorio_button.pack()

baixar_apenas_audio_var = tk.BooleanVar()
baixar_apenas_audio_checkbutton = tk.Checkbutton(root, text="audio only", variable=baixar_apenas_audio_var)
baixar_apenas_audio_checkbutton.pack()

download_button = tk.Button(root, text="Download", command=baixar_video)
download_button.pack()

status_label = tk.Label(root, text="")
status_label.pack()

# Usando ttk.Progressbar com "ttk."
import tkinter.ttk as ttk
progress_bar = ttk.Progressbar(root, orient="horizontal", mode="determinate")
progress_bar.pack()

root.mainloop()
