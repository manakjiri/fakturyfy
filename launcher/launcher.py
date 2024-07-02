import ctypes.wintypes
import multiprocessing
import sys
import os
import json
import ctypes
import platform
import tkinter
import tkinter.messagebox
import webbrowser
from pathlib import Path

SERVER_ADDRESS = '127.0.0.1:8000'
SERVER_URL = 'http://' + SERVER_ADDRESS
SERVER_PATH = Path(__file__).parent.resolve()


def run_server():
    print('Starting server...', os.getpid())
    sys.path.append(str(SERVER_PATH))
    sys.path.append(str(SERVER_PATH / 'external'))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'fakturyfy.settings'
    import django
    django.setup()
    django.core.management.execute_from_command_line(['manage.py', 'migrate'])
    django.core.management.execute_from_command_line(['manage.py', 'runserver', SERVER_ADDRESS, '--noreload'])
    return None

        
try:
    if platform.system() == 'Windows':
        dll = ctypes.windll.shell32
        buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH + 1)
        if dll.SHGetSpecialFolderPathW(None, buf, 0x0005, False):
            data_directory = Path(buf.value) / 'Fakturyfy'
        else:
            data_directory = Path.home() / 'Fakturyfy'
    elif platform.system() == 'Linux':
        data_directory = Path.home() / '.fakturyfy'
    
    config = {'data_directory': str(data_directory)}
    Path(SERVER_PATH / 'config.json').write_text(json.dumps(config))

    multiprocessing.freeze_support()
    server = multiprocessing.Process(target=run_server)
    server.start()

    root = tkinter.Tk()
    root.title('Fakturyfy Server')
    root.geometry('600x300')

    frame = tkinter.Frame(root)
    tkinter.Label(frame, text='Server spuštěn na adrese ' + SERVER_ADDRESS).pack(padx=2, pady=2)
    tkinter.Button(frame, text='Otevřít v prohlížeči', command=lambda: webbrowser.open(SERVER_URL)).pack(padx=2, pady=2)
    tkinter.Label(frame, text='Data jsou uložena ve složce ' + str(data_directory)).pack(padx=2, pady=2)
    if platform.system() == 'Windows':
        tkinter.Button(frame, text='Otevřít složku', command=lambda: os.startfile(data_directory)).pack(padx=2, pady=2)
    tkinter.Button(frame, text='Ukončit', command=root.quit).pack(padx=2, pady=2)
    frame.pack(expand=True, anchor='center')

    root.after(3000, lambda: webbrowser.open(SERVER_URL))
    root.mainloop()

finally:
    print('Killing server...')
    server.terminate()
    server.join()
