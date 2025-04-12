import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class EmailSender:
    def __init__(self):
        # Load email configuration from environment variables
        self.email_host = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
        self.email_port = int(os.getenv('EMAIL_PORT', 587))
        self.email_username = os.getenv('EMAIL_USERNAME', '')
        self.email_password = os.getenv('EMAIL_PASSWORD', '')
        self.email_from = os.getenv('EMAIL_FROM', self.email_username)
        self.admin_email = os.getenv('ADMIN_EMAIL', 'admin@example.com')
    
    def send_email(self, to_email, subject, message, is_html=False):
        """
        Send an email to the specified recipient
        
        Args:
            to_email (str): Recipient email address
            subject (str): Email subject
            message (str): Email content
            is_html (bool): Whether the message is HTML or plain text
        
        Returns:
            bool: True if sent successfully, False otherwise
        """
        if not self.email_username or not self.email_password:
            print("Email credentials not configured")
            return False
            
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.email_from
            msg['To'] = to_email
            
            # Attach message
            content_type = 'html' if is_html else 'plain'
            msg.attach(MIMEText(message, content_type))
            
            # Connect to SMTP server
            server = smtplib.SMTP(self.email_host, self.email_port)
            server.starttls()
            server.login(self.email_username, self.email_password)
            
            # Send email
            server.send_message(msg)
            server.quit()
            
            return True
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            return False
    
    def send_ticket_confirmation(self, ticket_data):
        """
        Send confirmation email to the user when a ticket is created
        
        Args:
            ticket_data (dict): Ticket information
        
        Returns:
            bool: True if sent successfully, False otherwise
        """
        # Skip if no email provided
        if not ticket_data.get('contact_email'):
            return False
        
        subject = f"Ticket #{ticket_data['id']} Received - {ticket_data['category']}"
        
        message = f"""
        <h2>Ticket Received</h2>
        <p>Dear user,</p>
        
        <p>Your ticket has been received and is being processed. Here are the details:</p>
        
        <p><strong>Ticket ID:</strong> #{ticket_data['id']}</p>
        <p><strong>Category:</strong> {ticket_data['category']}</p>
        <p><strong>Priority:</strong> {ticket_data['priority']}</p>
        <p><strong>Date Submitted:</strong> {ticket_data['date']}</p>
        
        <p>We will notify you when your issue is resolved.</p>
        
        <p>Thank you,<br>
        Support Team</p>
        """
        
        return self.send_email(ticket_data['contact_email'], subject, message, is_html=True)
    
    def notify_admin_new_ticket(self, ticket_data):
        """
        Notify administrators about a new ticket
        
        Args:
            ticket_data (dict): Ticket information
        
        Returns:
            bool: True if sent successfully, False otherwise
        """
        subject = f"New Ticket #{ticket_data['id']} - {ticket_data['category']}"
        
        message = f"""
        <h2>New Support Ticket</h2>
        
        <p><strong>Ticket ID:</strong> #{ticket_data['id']}</p>
        <p><strong>Category:</strong> {ticket_data['category']}</p>
        <p><strong>Priority:</strong> {ticket_data['priority']}</p>
        <p><strong>Date Submitted:</strong> {ticket_data['date']}</p>
        <p><strong>Contact Email:</strong> {ticket_data.get('contact_email', 'Not provided')}</p>
        
        <h3>Description:</h3>
        <p>{ticket_data['description']}</p>
        """
        
        return self.send_email(self.admin_email, subject, message, is_html=True)
    
    def send_resolution_notification(self, ticket_data, resolution_notes=""):
        """
        Send notification to the user when their ticket is resolved
        
        Args:
            ticket_data (dict): Ticket information
            resolution_notes (str): Notes on how the issue was resolved
        
        Returns:
            bool: True if sent successfully, False otherwise
        """
        # Skip if no email provided
        if not ticket_data.get('contact_email'):
            return False
        
        subject = f"Ticket #{ticket_data['id']} Resolved"
        
        message = f"""
        <h2>Ticket Resolved</h2>
        <p>Dear user,</p>
        
        <p>Your ticket has been resolved. Here are the details:</p>
        
        <p><strong>Ticket ID:</strong> #{ticket_data['id']}</p>
        <p><strong>Category:</strong> {ticket_data['category']}</p>
        <p><strong>Resolution Date:</strong> {ticket_data.get('resolved_date', 'N/A')}</p>
        
        <p><strong>Resolution Notes:</strong><br>
        {resolution_notes}</p>
        
        <p>Thank you for your patience.</p>
        
        <p>Regards,<br>
        Support Team</p>
        """
        
        return self.send_email(ticket_data['contact_email'], subject, message, is_html=True) 