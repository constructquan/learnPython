import smtplib
from email.mime.image import MIMEImage
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email.mime.base import MIMEBase
from email import encoders

htl = MIMEText('<html><body><hl>Hi.</hl>'+\
               '<p>Send by <a href="http://www.python.org">Python</a>\
               and an image...<br><img src="cid:image1"></br></p>'\
               +'</body></html>','html','utf-8')
fp = open('/home/hell/think.jpeg', 'rb')
msgImage = MIMEImage(fp.read())
fp.close()
msgImage.add_header('Content-ID','<image1>')

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

from_addr = input('From_addr:')
password = input('Password:')
to_addr = input('To_addr:')
smtp_server = input('SMTP_server:')

msg = MIMEMultipart()
msg['From'] = _format_addr('Pythoner<%s>' % from_addr)
msg['To'] = _format_addr('mumu<%s>' % to_addr)
msg['Subject'] = Header('From my best wish', 'utf-8').encode()

#msg.attach(MIMEText('send with file...', 'plain', 'utf-8'))
msg.attach(htl)
msg.attach(msgImage)
#with open('/home/hell/different.png', 'rb') as f:
#    mime = MIMEBase('image', 'png', filename = 'different.png')
#    mime.add_header('Content-Disposition', 'attachment', filename =
#                    'different.png')
#    mime.add_header('Content-ID', '<1>')
#    mime.add_header('X-Attachment-Id', '1')
#    mime.set_payload(f.read())
#    encoders.encode_base64(mime)
#    msg.attach(mime)

server = smtplib.SMTP(smtp_server, 25)
#server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()

