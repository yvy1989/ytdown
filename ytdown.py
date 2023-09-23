#downloader program
import tkinter as tk
import tkinter.filedialog as filedialog
import threading
import yt_dlp as youtube_dl
import os

def selecionar_diretorio():
    diretorio_destino = filedialog.askdirectory()
    if diretorio_destino:
        diretorio_entry.delete(0, tk.END)
        diretorio_entry.insert(0, diretorio_destino)

def baixar_video():
    url = url_entry.get()
    diretorio_destino = diretorio_entry.get()

    if not url:
        status_label.config(text="Por favor, insira uma URL.")
        return

    if not diretorio_destino:
        status_label.config(text="Por favor, selecione um diretório de destino.")
        return

    ydl_opts = {
        'outtmpl': f'{diretorio_destino}/%(title)s.%(ext)s',
        'progress_hooks': [download_progress_hook],
    }

    ydl = youtube_dl.YoutubeDL(ydl_opts)

    def download():
        try:
            with ydl:
                ydl.download([url])
                status_label.config(text="Download concluído!")
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
        status_label.config(text=f"Baixando: {progress}")
        try:
            progress_value = int(d['_percent_str'].strip('%').split('.')[0])
            progress_bar['value'] = progress_value
        except ValueError:
            pass

def abrir_pasta(diretorio):
    try:
        os.startfile(diretorio)  # Abre o diretório no sistema padrão do sistema operacional
    except AttributeError:
        import subprocess
        subprocess.Popen(['xdg-open', diretorio])  # Tente abrir a pasta no Linux
    except Exception as e:
        print(f"Erro ao abrir a pasta: {str(e)}")

root = tk.Tk()
root.title("YouTube Downloader")

# Defina as dimensões da janela em pixels
window_width = 400
window_height = 350
root.geometry(f"{window_width}x{window_height}")

url_label = tk.Label(root, text="URL do Vídeo:")
url_label.pack()

url_entry = tk.Entry(root, width=40)
url_entry.pack()

diretorio_label = tk.Label(root, text="Diretório de Destino:")
diretorio_label.pack()

diretorio_entry = tk.Entry(root, width=40)
diretorio_entry.pack()

selecionar_diretorio_button = tk.Button(root, text="Selecionar Diretório", command=selecionar_diretorio)
selecionar_diretorio_button.pack()

download_button = tk.Button(root, text="Baixar Vídeo", command=baixar_video)
download_button.pack()

status_label = tk.Label(root, text="")
status_label.pack()

# Usando ttk.Progressbar com "ttk."
import tkinter.ttk as ttk
progress_bar = ttk.Progressbar(root, orient="horizontal", mode="determinate")
progress_bar.pack()

root.mainloop()
