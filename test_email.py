from imap_tools import MailBox, AND
from config import settings
import logging

def test_email_connection():
    try:
        print("Attempting to connect to email server...")
        with MailBox(settings.EMAIL_SERVER).login(
            settings.EMAIL_USERNAME,
            settings.EMAIL_PASSWORD
        ) as mailbox:
            print("Successfully connected to email server!")
            print(f"Total emails in inbox: {len(list(mailbox.fetch()))}")
            print("Unread emails:")
            for msg in mailbox.fetch(AND(seen=False)):
                print(f"- Subject: {msg.subject}")
                print(f"  From: {msg.from_}")
                print(f"  Date: {msg.date}")
    except Exception as e:
        print(f"Error connecting to email server: {e}")

if __name__ == "__main__":
    test_email_connection() 