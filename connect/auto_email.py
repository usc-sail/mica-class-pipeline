import smtplib, ssl

def send_email(subject, message, receiver_email, sender_email="micaclasssail@gmail.com", sender_email_passwd="mica-classSAIL"):
    port = 465  
    smtp_server = "smtp.gmail.com"

    msg = "Subject: " + subject + "\n\n" + message

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, sender_email_passwd)
        server.sendmail(sender_email, receiver_email, msg)

def workflow_1():
    send_email("test subject", "sample message sent from python", "sbaruah@usc.edu")

def main():
    workflow_1()

if __name__ == "__main__":
    main()