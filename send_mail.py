# Import smtplib for the actual sending function
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

def send_mail(errormsg):
    port = 587
    smtp_server = 'smtp.gmail.com'
    sender_email = 'durantibot@gmail.com'
    receiver_email = ['matteo.duranti@cern.ch', 'yaozu.jiang@cern.ch', 'dexing.miao@cern.ch', 'pingcheng.liu@cern.ch', 'zijun.xu@cern.ch', 'zhiyu.xiang@cern.ch']
    password = "aqwp vhts flak cuuy"
    
    message = MIMEText(errormsg)
    message['Subject'] = 'Automatic mail from pcgsc03'
    message['From'] = sender_email
    message['To'] = ", ".join(receiver_email)
    
    server = smtplib.SMTP(smtp_server, port)
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message.as_string())
    server.quit()
