from time import sleep
import smtplib
import subprocess

#sends me an email about the current state of the bot
#copied right from my email_notif.py module
def send(info, to = 'wakydawgster@gmail.com'):
    mail = smtplib.SMTP('smtp.gmail.com',587)
    mail.ehlo()
    mail.starttls()
    mail.login('WakBot6969696969@gmail.com','lelelelele') #made a new email for this just so it doesn't matter if the password and stuff are leaked
    mail.sendmail('WakBot', to, info)
    mail.close()

#a subprocess that I can check for errors after it finishes executing
#copied right from my easy_subprocess.py module
class process:
    def __init__(self, cmd_args):
        self._popen = subprocess.Popen(cmd_args,
                                     stdout = subprocess.PIPE,
                                     stderr = subprocess.PIPE)
        data = self._popen.communicate()
        self._popen.terminate()
        self.output = data[0]
        self.errors = data[1]


#runs the main program every day
while 1:
    print 'Launching!'
    p = process(['python', 'autocancer.py'])
    report_start = "Just another successful day.\n"
    if p.errors != '':
        print "There was an error!"
        report_start = "ERROR IN AUTO YOUTUBE CANCER!!!\n"
    print "sending report..."
    send(report_start + "Here's your last 90000 bytes of output:\n\n\n\n\n" + p.output[-90000:] + '\n\n' + p.errors)
    print "report sent."
    print 'sleeping for like a day...'
    sleep(23 * 60 * 60) #only 23 hours because videos usually take at least an hour to generate and upload
