from email.mime.text import MIMEText
from flask import Flask, jsonify, request
import datetime
import time  # Simulate some work
from threading import Thread
import smtplib

app = Flask(__name__)
tasks = [
    {'id': 1, 'title': 'Grocery Shopping', 'completed': False,
     'due_date': '2024-03-15'},
    {'id': 2, 'title': 'Pay Bills', 'completed': False,
     'due_date': '2024-03-20'},
]

next_task_id = 3  # For assigning new task IDs


@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)


@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    global next_task_id # In the given code, this line is below the new_task line,
    # it throws error as the 'next_task_id' is used first and then global keyword used 
    # so it throws error as it becomes as a local variable without using global keyword first.
    new_task = {
        'id': next_task_id,
        'title': data['title'],
        'completed': False,
        'due_date': data.get('due_date') or
        datetime.date.today().strftime("%Y-%m-%d")
    }
    
    next_task_id += 1
    tasks.append(new_task)
    return jsonify(new_task), 201


def sendnotification(data):
    # Email Notification task
    # Create an APP password for the sender Email temporarily as newer accounts doesn't have Allow Less Secure Apps now
    sender_email = "" # Enter the sender Email
    receiver_email = "" # Enter the receiver Email
    password = "" # Enter sender Email Password

    msg = MIMEText(f"This is a notification - {data['title']}")
    msg["Subject"] = "Notification"
    msg["From"] = sender_email
    msg["To"] = receiver_email
    
    # Using smtplib Library, sending the Email
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
    
    time.sleep(15) # This is just to simulate the thread to run for more time 


@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):

    data = request.get_json()
    for task in tasks:
        if task['id'] == task_id:
            task.update(data)
            
            # Using Thread to send notification to Email
            # Creating of Thread Object that sets the target method with arguments
            th = Thread(target=sendnotification,args=(data,))  
            
            # Starting the thread to create a new thread and runs the threads separately 
            th.start()
            
            
            return jsonify(task), 200
    return jsonify({'error': 'Task not found'}), 404


@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    for i, task in enumerate(tasks):
        if task['id'] == task_id:
            del tasks[i]
            return jsonify({'message': 'Task deleted'}), 204
    return jsonify({'error': 'Task not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)
