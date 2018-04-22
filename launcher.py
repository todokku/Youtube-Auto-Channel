from time import sleep
from os import system

#runs the main program every day
while 1:
    print 'Launching!'
    system('python27 autocancer.py')
    print 'sleeping for like a day...'
    sleep(23 * 60 * 60) #only 23 hours because videos usually take at least an hour to generate and upload
