# -*- coding: utf-8 -*-

import fire
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

from_addr ='2312570224gui@sina.com' 
password = ''
to_addr = '2312570224@qq.com'
smtp_server = 'smtp.sina.com'


def send_email(context,subject):
    def _format_addr(s):
        name, addr = parseaddr(s)
        return formataddr(( \
            Header(name, 'utf-8').encode(), \
            addr.encode('utf-8') if isinstance(addr, unicode) else addr))

    msg = MIMEText(context, 'plain', 'utf-8')
    msg['From'] = _format_addr('guicunbin <%s>' % from_addr)
    msg['To'] = _format_addr('guicunbin <%s>' % to_addr)
    msg['Subject'] = Header(subject, 'utf-8').encode()
    
    server = smtplib.SMTP(smtp_server, 25)
    #server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()


if __name__=='__main__':
    fire.Fire(send_email)
