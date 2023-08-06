#=============================================================
#=================     Library Import    =====================
#=============================================================

import imaplib
import os
import smtplib

import email

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import  MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

#=============================================================
#=================        class          =====================
#=============================================================

# Classe Email Responsável pela automatização do processo usando o Email

class EmailAutomator:
    
    connection = None
    error = None

    def __init__(self):
        nothing = None

    def connect(self, mail_server, username, password):
        self.connection = imaplib.IMAP4_SSL(mail_server)
        # self.connection = imaplib.IMAP4(mail_server)
        self.connection.login(username, password)
        self.connection.select(readonly=False)  # so we can mark mails as read

    def connectNOSSL(self, mail_server, username, password):
        #self.connection = imaplib.IMAP4_SSL(mail_server)
        self.connection = imaplib.IMAP4(mail_server)
        self.connection.login(username, password)
        self.connection.select(readonly=False)  # so we can mark mails as read

    def close_connection(self):
        """
        Close the connection to the IMAP server
        """
        self.connection.close()

    def save_attachment(self, msg, download_folder="/tmp"):
        """
        Given a message, save its attachments to the specified
        download folder (default is /tmp)

        return: file path to attachment
        """
        att_path = "No attachment found."
        for part in msg.walk():
            try:
                if part.get_content_maintype() == 'multipart':
                    continue
                if part.get('Content-Disposition') is None:
                    continue

                filename = part.get_filename()
                att_path = os.path.join(download_folder, filename)

                if not os.path.isfile(att_path):
                    fp = open(att_path, 'wb')
                    fp.write(part.get_payload(decode=True))
                fp.close()
            except:
                nothing = None
        return att_path

    def fetch_unread_messages(self):
        """
        Retrieve unread messages
        """
        emails = []
        (result, messages) = self.connection.search(None, 'UnSeen')
        if result == "OK":
            print(str(messages[0]))
            for message in messages[0].decode().split(' '):
                try: 
                    ret, data = self.connection.fetch(message,'(RFC822)')
                except:
                    print ("No new emails to read.")
                    return []
                msg = email.message_from_bytes(data[0][1])
                if isinstance(msg, str) == False:
                    emails.append(msg)
                response, data = self.connection.store(message, '+FLAGS','\\Seen')

            return emails

        self.error = "Failed to retreive emails."
        return emails


    def fetch_unread_messages_with_given_subject(self,subject):
        """
        Retrieve unread messages
        """
        emails = []
        (result, messages) = self.connection.search(None, 'UnSeen')
        if result == "OK":
            for message in messages[0].decode().split(' '):
                try:
                    ret, data = self.connection.fetch(message,'(RFC822)')
                    retSubject, dataSubject = self.connection.fetch(message, '(RFC822.SIZE BODY[HEADER.FIELDS (SUBJECT)])')
                    if subject in str(dataSubject[0][1]):
                        msg = email.message_from_bytes(data[0][1])
                        if isinstance(msg, str) == False:
                            emails.append(msg)
                    response, data = self.connection.store(message, '+FLAGS', '\\Seen')
                except:
                    print ("No new emails to read.")
                    return []

            return emails

        self.error = "Failed to retreive emails."
        return emails

    def parse_email_address(self, email_address):
        """
        Helper function to parse out the email address from the message

        return: tuple (name, address). Eg. ('John Doe', 'jdoe@example.com')
        """
        return email.utils.parseaddr(email_address)


    def sendEmail(self, mail_server, port, mailFrom, password, mailTo , mailSubject, mailMessage, attachmentpath=""):

        message = MIMEMultipart()
        message["From"] = mailFrom
        message["To"] = mailTo
        message["Subject"] = Header(mailSubject,"utf-8")

        message.attach(MIMEText(mailMessage.encode('utf-8'), "plain", _charset="UTF-8" ))

        if attachmentpath != "":
            with open(attachmentpath, "rb") as attachment:
                part = MIMEBase("application" , "octet-stream")
                part.set_payload(attachment.read())
            encoders.encode_base64(part)

            filename = os.path.split(attachmentpath)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {filename[1]}",
            )

            message.attach(part)

        text = message.as_string()

        conn = smtplib.SMTP(mail_server , port)
        conn.starttls()
        conn.login(mailFrom , password)
        conn.sendmail(mailFrom , mailTo, text)
        conn.close()
