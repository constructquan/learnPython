#
#利用python的smtp模块完成简单的邮件发送功能，可以发送纯文本，也可以是html，可以添加附件。
#现在将图片嵌入到邮件的内容然后发送出去
#注释部分代码，实现了将图片作为附件发送
#

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

#用来格式化邮件地址
def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

from_addr = input('From_addr:')
password = input('Password:')
to_addr = input('To_addr:')
smtp_server = input('SMTP_server:')

#一个MIMEMultipart类型，因为有附件，图片等需要添加
#如果邮件有音频，视频等都可以用MIMEMultipart类型
msg = MIMEMultipart()

msg['From'] = _format_addr('Pythoner<%s>' % from_addr)
msg['To'] = _format_addr('mumu<%s>' % to_addr)
#邮件的主题可以是中文
msg['Subject'] = Header('From my best wish', 'utf-8').encode()

#发送纯文本 ‘plain’的方式：
#msg.attach(MIMEText('send with file...', 'plain', 'utf-8'))

#添加html文本
msg.attach(htl)
#添加图片，已经在html路径中的cid:image1了
msg.attach(msgImage)

#把图片作为附件添加：
#with open('/home/hell/different.png', 'rb') as f:
# 设置附件的MIME和文件名，这里是png类型:
#    mime = MIMEBase('image', 'png', filename = 'different.png')
#添加必要的文件头信息：
#    mime.add_header('Content-Disposition', 'attachment', filename =
#                    'different.png')
#    mime.add_header('Content-ID', '<1>')
#    mime.add_header('X-Attachment-Id', '1')
#    mime.set_payload(f.read())
#需要转码：
#    encoders.encode_base64(mime)
#添加到MIMEMultipart
#    msg.attach(mime)

#SMTP对象,smtp服务器的端口默认是25
server = smtplib.SMTP(smtp_server, 25)

#已debug的模式，可以打印一些发送过程的信息：
#server.set_debuglevel(1)
server.login(from_addr, password)

#to_addr是一个list,如果有多个收件人，则[to_addr1, to_addr2,...]
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()

