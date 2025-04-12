from flask import Flask, render_template, request, jsonify, Response, flash, redirect, url_for
import json
from datetime import datetime
import os
from classifier import IssueClassifier
from mailer import EmailSender
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your-secret-key-here')
classifier = IssueClassifier()
email_sender = EmailSender()

# File to store requests
REQUESTS_FILE = 'requests_db.json'

# Initialize requests database from file or create empty if not exists
def load_requests_db():
    if os.path.exists(REQUESTS_FILE):
        with open(REQUESTS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_requests_db(requests_db):
    with open(REQUESTS_FILE, 'w') as f:
        json.dump(requests_db, f, indent=2)

# Load initial requests
requests_db = load_requests_db()

@app.route('/')
def index():
    # Pass the requests_db to the template, showing only the last 5 requests
    recent_requests = requests_db[-5:][::-1]  # Get last 5 requests, newest first
    return render_template('index.html', requests_db=recent_requests)

# Add API endpoint for Streamlit app
@app.route('/api/recent-requests', methods=['GET'])
def api_recent_requests():
    return jsonify(requests_db)

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        try:
            description = request.form.get('description')
            priority = request.form.get('priority')
            contact_email = request.form.get('contact_email')

            if not description or not priority:
                flash('Please fill in all required fields', 'error')
                return redirect(url_for('submit'))

            new_request = {
                'id': len(requests_db) + 1,
                'description': description,
                'priority': priority,
                'category': classifier.classify_issue(description),
                'contact_email': contact_email,
                'status': 'open',
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            requests_db.append(new_request)
            save_requests_db(requests_db)  # Save to file after adding new request
            
            # Send email notifications
            if contact_email:
                email_sender.send_ticket_confirmation(new_request)
            
            # Notify admin about new ticket
            email_sender.notify_admin_new_ticket(new_request)
            
            flash('Issue submitted successfully!', 'success')
            return redirect(url_for('index'))  # Redirect to home page after submission
        except Exception as e:
            flash(f'Error submitting issue: {str(e)}', 'error')
            return redirect(url_for('submit'))
    return render_template('submit.html')

@app.route('/requests')
def list_requests():
    return render_template('requests.html', requests=requests_db[::-1])

@app.route('/requests/<int:request_id>')
def view_request(request_id):
    request_data = next((req for req in requests_db if req['id'] == request_id), None)
    if request_data:
        return render_template('request.html', request=request_data)
    return "Request not found", 404

@app.route('/resolve/<int:request_id>', methods=['POST'])
def resolve_request(request_id):
    try:
        request_data = next((req for req in requests_db if req['id'] == request_id), None)
        if not request_data:
            flash('Request not found', 'error')
            return redirect(url_for('list_requests'))
        
        resolution_notes = request.form.get('resolution_notes', '')
        
        # Update request status
        request_data['status'] = 'resolved'
        request_data['resolved_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        request_data['resolution_notes'] = resolution_notes
        
        # Save the updated request
        save_requests_db(requests_db)
        
        # Send resolution notification email
        if request_data.get('contact_email'):
            email_sender.send_resolution_notification(request_data, resolution_notes)
        
        flash('Request resolved successfully', 'success')
        return redirect(url_for('view_request', request_id=request_id))
    except Exception as e:
        flash(f'Error resolving request: {str(e)}', 'error')
        return redirect(url_for('view_request', request_id=request_id))

if __name__ == '__main__':
    app.run(debug=True, port=5000) 