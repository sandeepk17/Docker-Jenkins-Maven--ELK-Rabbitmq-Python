import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='Maven')

def callback(ch, method, properties, body):
    import smtplib

    gmail_user = "mkrtichmatevosyan9@gmail.com"
    gmail_pwd = "Mko555653"
    FROM = "mkrtichmatevosyan9@gmail.com"
    TO = ["mukuch90@gmail.com"]
    SUBJECT = "test"
    TEXT = body
	
    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print ("successfully sent the mail")
    except:
        print ("failed to send mail")

channel.basic_consume(callback,
                      queue='Maven',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()