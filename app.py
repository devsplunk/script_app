from flask import Flask, render_template, jsonify
import os
import subprocess

app = Flask(__name__)

# Directory where the bash scripts are stored
SCRIPTS_DIR = '/home/bryan/bash_scripts/'

# IP and port to bind the app
HOST = '192.168.254.132'
PORT = 3000

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute', methods=['GET'])
def execute_scripts():
    scripts = []
    for script_name in os.listdir(SCRIPTS_DIR):
        if script_name.endswith('.sh'):  # Only consider bash scripts
            script_path = os.path.join(SCRIPTS_DIR, script_name)
            try:
                # Execute the script
                result = subprocess.run(['bash', script_path], capture_output=True, text=True)
                scripts.append({
                    'script': script_name,
                    'status': 'Executed',
                    'output': result.stdout,
                    'error': result.stderr
                })
            except Exception as e:
                scripts.append({
                    'script': script_name,
                    'status': 'Failed',
                    'error': str(e)
                })

    return jsonify(scripts)

if __name__ == '__main__':
    app.run(host=HOST, port=PORT)

