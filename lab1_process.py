import multiprocessing
import random
import time
import numpy as np

def thread_func(row_no, matA,matB,result_queue,result_queue_no):
    row_value= np.matmul(matA, matB)

    result_queue_no.put(row_no)
    result_queue.put(row_value)


def main(n):
    # Generate queue for communication
    result_queue_no = multiprocessing.Manager().Queue()
    result_queue= multiprocessing.Manager().Queue()


    matA = np.random.randint(10, size = (n, n))
    matB = np.random.randint(10, size = (n, n))
    matC = np.zeros((matA.shape[0], matB.shape[1]))


    processes = 10
    jobs = []
    Q_per_process=matA.shape[0]//processes

    a=0
    b=Q_per_process
    for i in range(processes):
        mat_peice=matA[a:b,:matB.shape[1]]   #a為起始列 b為結束點(不會到b) ex:row是0:10 col是100 


        process = multiprocessing.Process(target = thread_func, args = (i, mat_peice,matB,result_queue,result_queue_no))
        jobs.append(process)

        a+=Q_per_process       # "0"-10 "10"-20 "20"-30 ..... (ex:100*100)
        b+=Q_per_process         # 0-"10" 10-"20" 20-"30" ..... (ex:100*100)        

    start_time=time.time()
    for process in jobs:
        process.start()

    for process in jobs:
        process.join()

    while not result_queue.empty():
        no = result_queue_no.get()
        result = result_queue.get()
        #print(no)
        #print(result)
        matC[no*Q_per_process:(no+1)*Q_per_process, :matB.shape[1]]=result #ex:100*100 --> 0:0-10 1:10-20 2:20-30

  
    end_time = time.time()
    print('Time elapsed:\t', end_time - start_time)

    print('Answer is correct:', np.all(np.matmul(matA, matB) == matC))


if __name__ == "__main__":
    main(10)
    main(100)
    main(1000)