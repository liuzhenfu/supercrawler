# Author: Yunqiao Zhang
# Email: zhangyunqiao@gmail.com

'''
A crawler process which is used to crawling a url. 
'''

# Config.

# Maximum HTTP request waiting time.
MAX_REQUEST_TIME = 3 

# Maximum response page size 512K.
MAX_PAGE_SIZE = 2**19

import Queue as Q
from multiprocessing import Process, Queue
import urllib2

class Crawler(Process):
  def __init__(self):
    Process.__init__(self)
    # Making a queue only contains 1 element.
    self.__queue = Queue(1)
    self.__isbusy = False

  def add_request(self, request):
    '''
    Add a request to crawler to crawl. This method is a non-blocking method.
    When the crawler is busy it will return False immediately, otherwise try 
    insert into the Queue.
    '''
    if not self.__isbusy:
      try:
        self.__queue.put_nowait(request)
      except Q.Full:
        return False
      else:
        return True
    else:
      return False

  def run(self):
    while True:
      request = self.__queue.get()

      self.__isbusy = True

      # Urlopen.
      try:
        print 'opening:', request
        response = urllib2.urlopen(request, timeout=MAX_REQUEST_TIME)
	print 'reading...'
        result = response.read(MAX_PAGE_SIZE)
        if len(result) == MAX_PAGE_SIZE:
          print 'Page size exceeds maximum'
      except Exception as e:
        # Catch all exceptions and continue next loop.
        print e

      self.__isbusy = False


# Unit test & sample usage.
if __name__ == '__main__':
  c = Crawler()
  c.start()
  c.add_request('http://www.microsoft.com')
  # The second request will fail.
  if not c.add_request('http://www.microsoft.com'):
    print 'add failed'
  c.join()
