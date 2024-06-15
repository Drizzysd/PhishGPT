from flask import Flask
from flask_mail import Mail, Message
from email_generator import EmailGenerator
import csv

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'email'
app.config['MAIL_PASSWORD'] = 'password'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

class EmailSender:
    
    def send_email(self, recipient_email, recipient_name):
        ai_generated_mail = EmailGenerator().generate_phishing_email(recipient_name, "https://phish-gpt.onrender.com/?id=" + recipient_email)
        
        subject, body = extract_email_content(ai_generated_mail)
        
        try:
            with app.app_context():
                msg = Message(subject, sender='ikennambelu.im@gmail.comcd', recipients=[recipient_email])
                msg.body = body
                mail.send(msg)
                print(f"Email sent successfully to {recipient_email}")
        except Exception as e:
            print(f"Error sending email to {recipient_email}: {str(e)}")
            
            
def extract_email_content(ai_response):
    # Extract subject and body from AI response
    subject = ai_response.split('\n')[0]
    body = '\n'.join(ai_response.split('\n')[2:])
    return subject, body

def main():
    # Initialize EmailSender instance
    email_sender = EmailSender()

    # Read email addresses from CSV file
    with open('./data/email_addresses.csv', 'r') as file:
        reader = list(csv.reader(file))
        del reader[0]
        print(reader)
        for row in reader:
            # Send the email
            email_sender.send_email(row[0], row[1])

if __name__ == "__main__":
    main()
