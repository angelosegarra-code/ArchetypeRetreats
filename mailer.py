import os, smtplib, mimetypes
from email.message import EmailMessage
MAIL_SERVER=os.environ.get('MAIL_SERVER','smtp.office365.com')
MAIL_PORT=int(os.environ.get('MAIL_PORT','587'))
MAIL_USE_TLS=os.environ.get('MAIL_USE_TLS','True').lower()=='true'
MAIL_USERNAME=os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD')
MAIL_FROM_NAME=os.environ.get('MAIL_FROM_NAME','Archetype Retreats')
MAIL_FROM_ADDR=os.environ.get('MAIL_FROM_ADDR', MAIL_USERNAME or 'no-reply@example.com')
def send_email(to_addr, subject, html, attachments=None):
    msg=EmailMessage(); msg['Subject']=subject; msg['From']=f"{MAIL_FROM_NAME} <{MAIL_FROM_ADDR}>"; msg['To']=to_addr
    msg.set_content('This message requires an HTML-compatible email client.'); msg.add_alternative(html, subtype='html')
    for path in attachments or []:
        import os, mimetypes
        ctype,_=mimetypes.guess_type(path); maintype,subtype=(ctype.split('/',1) if ctype else ('application','octet-stream'))
        with open(path,'rb') as f: data=f.read()
        msg.add_attachment(data, maintype=maintype, subtype=subtype, filename=os.path.basename(path))
    with smtplib.SMTP(MAIL_SERVER, MAIL_PORT) as server:
        if MAIL_USE_TLS: server.starttls()
        if MAIL_USERNAME and MAIL_PASSWORD: server.login(MAIL_USERNAME, MAIL_PASSWORD)
        server.send_message(msg)
