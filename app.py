import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
import subprocess
import random

app = Flask(__name__)


UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


users = {
    'admin1': '123',
    'admin': '456'
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    if username in users and users[username] == password:
        # Redirect to select page after successful login
        return redirect(url_for('select'))
    else:
        # Redirect back to login page with error message
        return redirect(url_for('index'))

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['new-username']
    password = request.form['new-password']
    
    # Add new user to the database (in reality, you'd hash the password)
    users[username] = password
    
    # Redirect to login page after successful signup
    return redirect(url_for('index'))

@app.route('/select')
def select():
    # Render select page after successful login
    return render_template('select.html')

@app.route('/upload', methods=['POST'])
def upload():
    # Get the number of ways and uploaded files from the request
    num_ways = int(request.form['num_ways'])
    files = request.files.getlist('files')

    # Handle file storage here
    file_paths = []
    for file in files:
        filename = file.filename
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        file_paths.append(file_path)

    # Call the script to process uploaded files
    results = subprocess.check_output(['python', 'counted_vehicles.py'] + file_paths, text=True)
    
    # After processing all videos, run the main program
    os.system('python program.py')

    # Read the content of out.txt and timing.txt
    with open('out.txt', 'r') as file:
        vehicle_count = file.readline().strip()  # Read the vehicle count
    
    with open('timing.txt', 'r') as file:
        timing = file.readline().strip()  # Read the timing

    # Redirect to a page showing the uploaded files or perform further processing
    return redirect(url_for('uploaded_files', vehicle_count=vehicle_count, timing=timing))

@app.route('/spinner')
def spinner():
    return render_template('spinner.html')

@app.route('/uploaded_files')
def uploaded_files():
    # Read the content of out.txt to get the vehicle counts
    with open('out.txt', 'r') as file:
        vehicle_counts = [int(line.strip()) for line in file]

    # Read the timing from timing.txt
    with open('timing.txt', 'r') as file:
        timing = file.readline().strip()

    # Render the template and pass the vehicle counts and timing to it
    return render_template('counted_vehicles.html', vehicle_counts=vehicle_counts, timing=timing)

@app.route('/get_data')
def get_data():
    # Read the content of out.txt to get the vehicle counts
    with open('out.txt', 'r') as file:
        vehicle_counts = [int(line.strip()) for line in file]

    # Read the timing from timing.txt
    with open('timing.txt', 'r') as file:
        timing = file.readline().strip()

    # Return JSON response with vehicle counts and timing
    return jsonify(vehicle_counts=vehicle_counts, timing=timing)

if __name__ == '__main__':
    app.run(debug=True)
