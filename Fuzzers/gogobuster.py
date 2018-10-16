# System modules
from Queue import Queue
from threading import Thread
import time

# Local modules
import feedparser

# Set up some global variables
thread_count = 2
command_queue = Queue()

file = "test"
targets = open(file).read().splitlines()


def runCommand(item, queue):
    while True:
        print '%s: Looking for the next enclosure' % item
        command = queue.get()
        print '%s: Downloading:' % item, url
        # instead of really downloading the URL,
        # we just pretend and sleep
        time.sleep(item + 2)
        queue.task_done()


# Set up some threads to fetch the enclosures
for item in range(thread_count):
    worker = Thread(target=runCommand, args=(iitem, command,))
    worker.setDaemon(True)
    worker.start()

# Download the feed(s) and put the enclosure URLs into
# the queue.
for url in targets:
    


    
    response = feedparser.parse(url, agent='fetch_podcasts.py')
    for entry in response['entries']:
        for enclosure in entry.get('enclosures', []):
            print 'Queuing:', enclosure['url']
            enclosure_queue.put(enclosure['url'])
        
# Now wait for the queue to be empty, indicating that we have
# processed all of the downloads.
print '*** Main thread waiting'
enclosure_queue.join()
print '*** Done'