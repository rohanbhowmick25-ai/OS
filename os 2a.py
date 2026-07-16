from multiprocessing import Process, Queue
import time
import random


# Producer Function
def producer(queue):
    """
    The producer generates data and puts it into the queue.
    queue.put(item) sends data to the consumer.
    """
    for i in range(5):
        item = random.randint(1, 100)
        print(f"Producer produced: {item}")

        queue.put(item)      # Put item into queue
        time.sleep(random.uniform(0.5, 1.5))


# Consumer Function
def consumer(queue):
    """
    The consumer receives data from the queue.
    queue.get() waits until an item is available.
    """
    for i in range(5):
        item = queue.get()   # Get item from queue
        print(f"Consumer consumed: {item}")

        time.sleep(random.uniform(0.5, 1.5))


# Main Program
if __name__ == "__main__":
    # Create a Queue for communication
    q = Queue()

    # Create Producer and Consumer Processes
    p1 = Process(target=producer, args=(q,))
    p2 = Process(target=consumer, args=(q,))

    # Start Processes
    p1.start()
    p2.start()

    # Wait for both processes to complete
    p1.join()
    p2.join()

    print("\nProducer and Consumer have finished.")
