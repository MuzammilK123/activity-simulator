from flask import Flask, render_template, request, jsonify
import logging
import pyautogui
import time
import random
import threading
from io import StringIO

app = Flask(__name__)

# Custom handler to capture logs in memory
class MemoryHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.buffer = StringIO()

    def emit(self, record):
        self.buffer.write(self.format(record) + '\n')

    def get_logs(self):
        logs = self.buffer.getvalue()
        self.buffer.truncate(0)
        self.buffer.seek(0)
        return logs.strip()

# Attach the custom handler to the root logger
memory_handler = MemoryHandler()
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s')
logging.getLogger().addHandler(memory_handler)

def get_user_choices(choices):
    actions = []
    if 'move' in choices:
        actions.append('move')
    if 'click' in choices:
        actions.append('click')
    if 'scroll' in choices:
        actions.append('scroll')
    if 'type' in choices:
        actions.append('type')
    if 'shift' in choices:
        actions.append('shift')
    if 'arrow_down' in choices:
        actions.append('arrow_down')
    if 'random' in choices:
        actions = ['move', 'click', 'scroll', 'type', 'shift', 'arrow_down']

    return actions

def keep_awake(actions, interval, time_cap):
    start_time = time.time()
    try:
        while True:
            action = random.choice(actions)
            if action == 'move':
                x = random.randint(-100, 100)
                y = random.randint(-100, 100)
                logging.debug(f"Moving mouse by ({x}, {y})")
                pyautogui.moveRel(x, y, duration=0.25)
            elif action == 'click':
                logging.debug("Clicking")
                pyautogui.click()
            elif action == 'scroll':
                clicks = random.randint(-10, 10)
                logging.debug(f"Scrolling by {clicks} clicks")
                pyautogui.scroll(clicks)
            elif action == 'type':
                text = random.choice(['Hello', 'Awake', 'Keep awake'])
                logging.debug(f"Typing text: {text}")
                pyautogui.typewrite(text, interval=0.1)
            elif action == 'shift':
                logging.debug("Pressing 'shift' key")
                pyautogui.press('shift')
            elif action == 'arrow_down':
                logging.debug("Pressing arrow down key")
                pyautogui.press('down')

            time.sleep(interval)
            
            elapsed_time = time.time() - start_time
            if elapsed_time > (time_cap * 60):
                logging.info(f"Ending loop after {time_cap} minutes")
                break
    except Exception as e:
        logging.error(f"An error occurred: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    data = request.get_json()
    actions = get_user_choices(data['actions'])
    interval = int(data['interval'])
    time_cap = int(data['timeCap'])

    # Run the keep_awake function in a separate thread to avoid blocking
    threading.Thread(target=keep_awake, args=(actions, interval, time_cap)).start()
    
    return jsonify({'message': 'Activity started!'})

if __name__ == '__main__':
    app.run(debug=True)
