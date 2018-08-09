import numpy as np
import threading
import time


def thread_func(mat_peice,matB,matC,a,b,col):
    
    row_value= np.matmul(mat_peice, matB)
    #print("++",matD)
    #print(row_value)
    matC[a:b,:col]=row_value
    

def main(n):
    # How many thread you want to use
    thread_num = 10
    threads = []

    matA = np.random.randint(10, size = (n, n))
    matB = np.random.randint(10, size = (n, n))
    matC = np.zeros((matA.shape[0], matB.shape[1]))
  
    # Assign job to threads
    a=0
    b=matA.shape[0]//thread_num
    for i in range(thread_num):    
        # Pass argument to function with tuple

        mat_peice=matA[a:b,:matB.shape[1]]   #a為起始列 b為結束點(不會到b) ex:row是0:10 col是100 
        thread = threading.Thread(target = thread_func, args = (mat_peice,matB,matC,a,b,matB.shape[1]))
        threads.append(thread)
        
        a+=matA.shape[0]//thread_num         # "0"-10 "10"-20 "20"-30 ..... (ex:100*100)
        b+=matA.shape[0]//thread_num         # 0-"10" 10-"20" 20-"30" ..... (ex:100*100)

    # run all threads
    start_time = time.time()
    for thread in threads:
        thread.start()

    # Wait for threads finish
    
    for thread in threads:
        thread.join()

    end_time = time.time()
    print('Time elapsed:\t', end_time - start_time)
    print('Answer is correct:', np.all(np.matmul(matA, matB) == matC))
    
if __name__ == "__main__":
    main(10)
    main(100)
    main(1000)

