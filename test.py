from writeCSV import WriteCSV
import threading

# A thread class from https://www.tutorialspoint.com/python/python_multithreading.htm
class myThread (threading.Thread):
   def __init__(self, threadID, name, counter, writer):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.writer = writer
   def run(self):
        generator = gen()
        for i in generator:
            self.writer.writeData(i)

def gen():
    l = [1,2,3,5,6,7]
    for i in l:
        yield [i+1,i+2]

print("Opening output.csv")
writer = WriteCSV('output.csv')
writer.openFile()
writer.writeHeader()
print('Starting thread')
# Create a new daemon thread just for taking in sensory-motor values
thread1 = myThread(1, "Thread-1", 1, writer)
thread1.daemon = True
thread1.start()
writer.closeFile()