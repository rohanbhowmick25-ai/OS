from multiprocessing import Process, Queue
import time


def producer(q):
    for i in range(1, 6):
        print("Producer produced:", i)
        q.put(i)        
        time.sleep(1)



def consumer(q):
    for i in range(1, 6):
        item = q.get()    
        print("Consumer consumed:", item)
        time.sleep(2)



if __name__ == "__main__":
    q = Queue(maxsize=3)   

    p1 = Process(target=producer, args=(q,))
    p2 = Process(target=consumer, args=(q,))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    print("Program Finished")
