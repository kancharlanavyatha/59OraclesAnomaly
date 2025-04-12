import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email Configuration
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USERNAME = st.secrets["email"]["username"]
EMAIL_PASSWORD = st.secrets["email"]["password"]

# Issue Handler Configuration
ISSUE_HANDLERS = {
    "bug": "bug-team@company.com",
    "feature": "feature-team@company.com",
    "documentation": "docs-team@company.com",
    "security": "security-team@company.com",
    "performance": "performance-team@company.com"
}

def send_email_notification(issue_data):
    """Send email notification to appropriate handler based on issue category."""
    try:
        handler_email = ISSUE_HANDLERS.get(issue_data['category'].lower())
        if not handler_email:
            st.warning(f"No handler configured for category: {issue_data['category']}")
            return

        # Create message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USERNAME
        msg['To'] = handler_email
        msg['Subject'] = f"New {issue_data['priority'].upper()} Priority Issue: #{issue_data['id']}"

        # Email body
        body = f"""
        New Issue Assigned:
        
        ID: {issue_data['id']}
        Description: {issue_data['description']}
        Priority: {issue_data['priority']}
        Category: {issue_data['category']}
        Status: {issue_data['status']}
        Date: {issue_data['date']}
        
        Please review and take appropriate action.
        """
        
        msg.attach(MIMEText(body, 'plain'))

        # Send email
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            server.send_message(msg)
            
        st.success(f"Email notification sent to {handler_email}")
    except Exception as e:
        st.error(f"Failed to send email notification: {str(e)}")

# Flask API endpoint
FLASK_API_URL = "http://localhost:5000"

# Configure Streamlit page
st.set_page_config(
    page_title="Issue Analytics",
    layout="wide",
    page_icon="📊"
)

# Add a link back to Flask interface
st.markdown("[← Back to Main Interface](http://localhost:5000)")
st.title("Issue Analytics Dashboard")

# Manual Refresh Button
if "issues_data" not in st.session_state:
    st.session_state.issues_data = None

if "previous_issues" not in st.session_state:
    st.session_state.previous_issues = set()

if st.button("🔄 Refresh Data"):
    st.session_state.issues_data = None

# Fetching and caching the data (only when session_state is None)
if st.session_state.issues_data is None:
    try:
        with st.spinner("Fetching data from server..."):
            response = requests.get(f"{FLASK_API_URL}/api/recent-requests")
            if response.status_code == 200:
                new_issues = response.json()
                
                # Check for new issues and send notifications
                current_issue_ids = {issue['id'] for issue in new_issues}
                new_issue_ids = current_issue_ids - st.session_state.previous_issues
                
                # Send notifications for new issues only
                for issue in new_issues:
                    if issue['id'] in new_issue_ids:
                        send_email_notification(issue)
                
                # Update previous issues set with current issues
                st.session_state.previous_issues = current_issue_ids
                st.session_state.issues_data = new_issues
            else:
                st.error("Failed to fetch data from the server.")
    except Exception as e:
        st.error(f"Error connecting to server: {str(e)}")
        st.info("Please make sure the Flask server is running on port 5000")

# Proceed if we have data
issues = st.session_state.issues_data

if issues is None:
    st.info("No issues found. Submit some issues to see analytics.")
elif not issues:
    st.warning("No issues available at the moment.")
else:
    df = pd.DataFrame(issues)

    # Create two columns for layout
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Priority Distribution")
        priority_counts = df['priority'].value_counts()
        fig_priority = px.pie(
            values=priority_counts.values,
            names=priority_counts.index,
            color=priority_counts.index,
            color_discrete_map={
                'high': '#ef4444',
                'medium': '#f59e0b',
                'low': '#10b981'
            }
        )
        st.plotly_chart(fig_priority, use_container_width=True)

        st.subheader("Category Distribution")
        category_counts = df['category'].value_counts()
        fig_category = px.bar(
            x=category_counts.index,
            y=category_counts.values,
            labels={'x': 'Category', 'y': 'Count'}
        )
        st.plotly_chart(fig_category, use_container_width=True)

    with col2:
        st.subheader("Issues Over Time")
        df['date'] = pd.to_datetime(df['date'])
        daily_counts = df.groupby(df['date'].dt.date).size().reset_index(name='count')
        fig_timeline = px.line(
            daily_counts,
            x='date',
            y='count',
            labels={'date': 'Date', 'count': 'Number of Issues'}
        )
        st.plotly_chart(fig_timeline, use_container_width=True)

        st.subheader("Status Overview")
        status_counts = df['status'].value_counts()
        fig_status = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            color=status_counts.index
        )
        st.plotly_chart(fig_status, use_container_width=True)

    st.subheader("Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Issues", len(df))
    with col2:
        st.metric("High Priority", len(df[df['priority'] == 'high']))
    with col3:
        st.metric("Open Issues", len(df[df['status'] == 'open']))
    with col4:
        st.metric("Avg Response Time", "24h")

    st.subheader("Recent Issues")
    st.dataframe(
        df[['id', 'description', 'priority', 'category', 'status', 'date']].sort_values('date', ascending=False),
        use_container_width=True
    )
