from flask import Flask, request, redirect, send_from_directory
import smtplib
from email.mime.text import MIMEText
import os

app = Flask(__name__)

# Serve your existing index.html
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# Serve static files
@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

# Handle form submission
@app.route('/send_email', methods=['POST'])
def send_email():
    name = request.form.get('name')
    email = request.form.get('email')
    subject = request.form.get('subject')
    message_body = request.form.get('message')
    
    # Format the email
    message_content = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message_body}"
    
    success = False
    
    try:
        # Email server settings
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        
        # Replace with your credentials (use environment variables in production)
        sender_email = "davidguticodes@gmail.com"
        password = "torito"
        
        server.login(sender_email, password)
        
        # Create message
        msg = MIMEText(message_content)
        msg['Subject'] = f"Contact Form: {subject}"
        msg['From'] = sender_email
        msg['To'] = "davidguticodes@gmail.com"
        
        # Send email
        server.send_message(msg)
        server.quit()
        
        success = True
    except Exception:
        pass
    
    # Create a simple thank you/error page
    if success:
        # Create and serve a success HTML page
        success_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Message Sent</title>
            <meta http-equiv="refresh" content="3;url=/#contact">
            <style>
                body { font-family: Arial, sans-serif; text-align: center; margin-top: 100px; }
                .message { padding: 20px; background-color: #d4edda; color: #155724; border-radius: 5px; display: inline-block; }
            </style>
        </head>
        <body>
            <div class="message">
                <h2>Thank You!</h2>
                <p>Your message has been sent successfully.</p>
                <p>Redirecting back to the site in 3 seconds...</p>
                <p><a href="/#contact">Click here if not redirected automatically</a></p>
            </div>
        </body>
        </html>
        """
        return success_html
    else:
        # Create and serve an error HTML page
        error_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Message Error</title>
            <meta http-equiv="refresh" content="3;url=/#contact">
            <style>
                body { font-family: Arial, sans-serif; text-align: center; margin-top: 100px; }
                .message { padding: 20px; background-color: #f8d7da; color: #721c24; border-radius: 5px; display: inline-block; }
            </style>
        </head>
        <body>
            <div class="message">
                <h2>Error</h2>
                <p>There was a problem sending your message.</p>
                <p>Redirecting back to the site in 3 seconds...</p>
                <p><a href="/#contact">Click here if not redirected automatically</a></p>
            </div>
        </body>
        </html>
        """
        return error_html

# Run the app
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5003))
    app.run(host='0.0.0.0', port=port, debug=True)