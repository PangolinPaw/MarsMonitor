from flask import Flask, render_template, redirect, request
import os
import socket
import threading

dirname, _ = os.path.split(os.path.abspath(__file__))
THIS_DIRECTORY = f'{dirname}{os.sep}'

app = Flask(__name__)

@app.route('/', methods=['GET'])
def root():
    captures = [c.split(os.sep)[-1] for c in list_files(f'{THIS_DIRECTORY}static{os.sep}captures', ['png'])]
    for c in captures:
        print(c)
    hero = captures[-1]
    if 'capture' in request.args:
        if request.args['capture'] in captures:
            hero = request.args['capture']
    captures.reverse()
    return render_template(
        'index.html',
        captures = captures,
        hero = hero
    )

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect(('10.254.254.254', 1)) # doesn't have to be reachable
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def launch():
    web_thread = threading.Thread(target=app.run, kwargs={'host':'0.0.0.0', 'port':5000})
    web_thread.start()
    return f'http://{get_ip()}:5000'

def list_files(folder, extensions=None):
    file_list = []
    all_files = os.listdir(folder)
    for name in all_files:
        if extensions is not None:
            for ext in extensions:
                if name.endswith(ext):
                    file_list.append(f'{folder}{os.sep}{name}')
        else:
            file_list.append(f'{folder}{os.sep}{name}')
    return file_list


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)