# Issue Management System with Email Notifications

A comprehensive issue tracking and analytics platform that enables users to submit, track, and analyze issues with automated email notifications.

## Tech Stack

### Backend
- **Flask** (v2.3.3): Core web framework for the main application interface
- **FastAPI** (v0.104.1): API framework for the email integration service
- **Uvicorn** (v0.24.0): ASGI server for running FastAPI
- **Pydantic** (v2.4.2): Data validation and settings management
- **Pydantic-Settings** (v2.2.1): Environment configuration management
- **Python-dotenv** (v1.0.0): Environment variable management
- **IMAP-Tools** (v1.0.0): Email integration for monitoring inbound tickets

### Frontend
- **Streamlit** (v1.44.1): Analytics dashboard and data visualization
- **Plotly** (v6.0.1): Interactive charts and graphs
- **Jinja2** (v3.1.2): Templating engine for Flask interface
- **HTML/CSS**: Custom styling and interface components

### Data Handling
- **Pandas** (v2.0.3): Data manipulation and analysis
- **JSON**: Issue data storage and interchange format

### Email Integration
- **SMTP**: Outbound email notification delivery
- **IMAP**: Inbound email monitoring for ticket creation

## Features

### Issue Management
- Submit new issues with priority levels and contact information
- Automatic issue classification using keyword-based categorization
- Ticket tracking through web interface
- Issue resolution workflow with status updates

### Email Notifications
- Automated email notifications for new issues
- Customized notifications based on issue category and priority
- Resolution notifications to ticket submitters
- Email-to-ticket conversion for incoming support emails

### Analytics Dashboard
- Real-time issue analytics with Streamlit
- Visual representations of issue priority distribution
- Category distribution analysis
- Time-based issue tracking
- Status overview and key metrics

### Multi-Channel Support
- Web interface for direct ticket submission
- Email integration for ticket creation
- API endpoints for programmatic access

## Getting Started

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Configure your environment variables in `.env` file:
   ```
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USERNAME=your_email@gmail.com
   EMAIL_PASSWORD=your_app_password
   EMAIL_FROM=support@yourcompany.com
   ADMIN_EMAIL=admin@yourcompany.com
   FLASK_SECRET_KEY=your-secret-key-here
   ```
4. Configure Streamlit secrets in `.streamlit/secrets.toml`:
   ```
   [email]
   username = "your_email@gmail.com"
   password = "your_app_password"
   ```
5. Start the Flask application:
   ```
   python app.py
   ```
6. Start the Streamlit dashboard in a separate terminal:
   ```
   streamlit run streamlit_app.py
   ```
7. Access the main interface at http://localhost:5000
8. Access the analytics dashboard at http://localhost:8501

## System Architecture

The system consists of two main components:
1. **Flask Application**: Core issue management interface with full CRUD capabilities
2. **Streamlit Dashboard**: Real-time analytics and data visualization interface

These components communicate through a RESTful API, with the Flask app serving as the data source for the Streamlit dashboard.

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Configure email settings:
   - Rename `.env.example` to `.env` or create a new `.env` file
   - Update the email configuration settings:
     ```
     EMAIL_HOST=smtp.gmail.com
     EMAIL_PORT=587
     EMAIL_USERNAME=your_email@gmail.com
     EMAIL_PASSWORD=your_app_password
     EMAIL_FROM=support@yourcompany.com
     ADMIN_EMAIL=admin@yourcompany.com
     FLASK_SECRET_KEY=your-secret-key-here
     ```

   **Note for Gmail users:** You'll need to use an App Password instead of your regular account password. See [Google's documentation](https://support.google.com/accounts/answer/185833) for instructions.

4. Run the application:
   ```
   python app.py
   ```

5. Access the application at http://localhost:5000

## How Email Notifications Work

1. **Ticket Creation:**
   - When a user submits a ticket with their email address, they'll receive a confirmation email
   - An administrator will also receive a notification about the new ticket

2. **Ticket Resolution:**
   - When support staff resolves a ticket, they can add resolution notes
   - The user who submitted the ticket will receive an email notification with these notes

## Project Structure

- `app.py` - Main application file
- `mailer.py` - Email functionality
- `classifier.py` - Issue categorization 
- `templates/` - HTML templates
  - `base.html` - Base template
  - `index.html` - Home page
  - `submit.html` - Ticket submission form
  - `requests.html` - List of all tickets
  - `request.html` - Individual ticket view with resolution form

## Security Considerations

- Store sensitive email credentials in environment variables, not in code
- Use HTTPS in production
- Consider implementing user authentication for admin functions

## License

[MIT License](LICENSE) 