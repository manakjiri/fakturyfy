import subprocess
import sys
import os
import signal
import tkinter
import tkinter.messagebox
import webbrowser
from pathlib import Path

SERVER_ADDRESS = '127.0.0.1:8000'
SERVER_URL = 'http://' + SERVER_ADDRESS
SERVER_PATH = (Path(__file__).parent / 'backend').resolve()
EXECUTABLE = 'python' if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS') else sys.executable

try:
    sys.path.append(str(SERVER_PATH / 'fakturyfy'))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
    import django
    django.setup()
    django.core.management.execute_from_command_line(['manage.py', 'migrate'])
    server = subprocess.Popen([EXECUTABLE, 'manage.py', 'runserver', SERVER_ADDRESS], cwd='../backend')

except subprocess.CalledProcessError as e:
    print('Failed to start server:', e)
    tkinter.messagebox.showerror('Chyba', 'Nepodařilo se spustit server.\n' + str(e))
    sys.exit(1)

try:
    root = tkinter.Tk()
    root.title('Fakturyfy Server')
    root.geometry('400x300')

    frame = tkinter.Frame(root)
    tkinter.Label(frame, text='Server spuštěn na adrese ' + SERVER_ADDRESS).pack(padx=2, pady=2)
    tkinter.Button(frame, text='Otevřít v prohlížeči', command=lambda: webbrowser.open(SERVER_URL)).pack(padx=2, pady=2)
    tkinter.Button(frame, text='Ukončit', command=root.quit).pack(padx=2, pady=2)
    frame.pack(expand=True, anchor='center')

    root.after(3000, lambda: webbrowser.open(SERVER_URL))
    root.mainloop()

finally:
    print('Killing server...')
    server.send_signal(signal.SIGINT)
    server.wait()
