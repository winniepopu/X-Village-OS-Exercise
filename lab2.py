import threading
import queue
import os
import time

buffer_size = 5

lock = threading.Lock()
queue = queue.Queue(buffer_size)
file_count = 0

def producer(top_dir, queue_buffer):
    queue_buffer.put(top_dir, block=True, timeout=None)     #將路徑存進queue
    dir=os.listdir(top_dir)                                 #列出path下所有檔名

    for file_name in dir:
        path=os.path.join(top_dir, file_name)   #將path路徑下的所有檔案併成完整路徑

        if(os.path.isdir(path)):
            producer(path,queue_buffer)         #若不是檔案，繼續往子層資料夾搜尋
               

def consumer(queue_buffer):
    global file_count
    
    try: 
        path=queue_buffer.get(block=True, timeout=0.1)  #取路徑，若timeout超過0.1，表示已無檔案，鎮列為空
        dir=os.listdir(path)             #列出path下所有檔名
        
        for file_name in dir:
            path2=os.path.join(path,file_name)   #將path路徑下的所有檔案併成完整路徑
            if os.path.isfile(path2):    #若是file
                lock.acquire()              
                file_count+=1             
                lock.release()
    except Exception as e :
        pass

def main():
    producer_thread = threading.Thread(target = producer, args = ('./testdata', queue))

    consumer_count = 20
    consumers = []
    for i in range(consumer_count):
        consumers.append(threading.Thread(target = consumer, args = (queue,)))

    producer_thread.start()
    for c in consumers:
        c.start()

    producer_thread.join()
    for c in consumers:
        c.join()

    print(file_count, 'files found.')

if __name__ == "__main__":
    main()

