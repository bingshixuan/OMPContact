#!/opt/anaconda3/bin/python
#coding=utf-8

import cgi
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
import multiprocessing

import datetime
import random


def calculateResult(form):
    emailAddr = form['email'].value
    print(emailAddr)
    filename = emailAddr.split('@', 1)[0]
    print(filename)
    filename = filename.split('.', 1)[0] # in case there is . in username
    print(filename) #multi-sutmit will lead error of former job.

    now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    randomNum = random.randint(0, 100)
    filename = filename + str(now) + str(randomNum)

    f = open('ompcontactPython2/fastaInput/'+filename+'.fasta','w')
    f.write(form['sequence'].value)
    f.close()
    
    # The end of web interact. finish write the sequence into a file
    pth1 = os.getcwd() 
    os.chdir(pth1 + '/ompcontactPython2')
    cmd = '/opt/anaconda2/bin/python OMPContact.py -i ' + 'fastaInput/' + filename + '.fasta'
    print(cmd)
    os.system(cmd)
    sendEmail(emailAddr, filename)


def sendEmail(email, filename):
    username = 'bingshixuan@126.com'
    password = 'bingshixuan_0000'
    sender = 'bingshixuan@126.com'
    
    receiver = {email}
    subject = 'OmpContact Result'
    subject = Header(subject, 'utf-8').encode()
    
    msg = MIMEMultipart('mixed')
    msg['Subject'] = subject
    msg['From'] = 'bingshixuan@126.com <bingshixuan@126.com>'
    msg['To'] = ";".join(receiver)
    text = 'Dear Tester:\n Attached file is the Result of your Tested sequence.\n If there is any question.' \
           + 'Please contact us by bingshixuan@126.com. If you like our program. Please cite your paper.'
    text_plain = MIMEText(text, 'plain', 'utf-8')
    msg.attach(text_plain)
    
    sendfile=open(os.getcwd() + '/fastaInput/'+filename+'.pred', 'rb').read()
    text_att = MIMEText(sendfile, 'base64', 'utf-8')
    text_att["Content-Type"] = 'application/octet-stream'
    text_att.add_header('Content-Disposition', 'attachment', filename=filename+'.xls')
    msg.attach(text_att)
    
    smtp = smtplib.SMTP()
    smtp.connect('smtp.126.com')
    smtp.login(username, password)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()
    

def main():
    print('Content-type:text/html\n\n')
    form = cgi.FieldStorage()
    
    if form['sequence'].value =="":
        print("No fasta Sequence input, please input sequence again and retry.")
        return 
    
    if form['email'].value =="":
        print("Confirm you input your email address, or you will not get predict result.")
        
    # should check the input format of fasta file.
    
    # start a process to predict 

    calProcess = multiprocessing.Process(target=calculateResult, args=(form,))
    calProcess.start()

    print("The job you submitted has began. Please check Email later.\n")
    print("The result file will be attached to the respond email.\n")
    print("Be patient. Maybe the calculation process cost some times.\n")
    print("Sometimes the respond email may be blocked as spams. \n")
    print("Don't forget to check trash. Enjoy!")

    
main()
