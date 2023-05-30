response = '\'popo\': close'
print(response[0:-1])

idx = response.find(':')
print(idx)
print('last char: ', response[-1])
print(response[idx+2:len(response)])
if response[idx+2:len(response)] == 'close':
    print('AAAAAAAAAAAA')


import time
import threading

def popo(max):
    for i in range(10):
        time.sleep(1)
        print(i)
        if i == max:
            return


thread1 = threading.Thread(target=popo, args=[2])
thread2 = threading.Thread(target=popo,args=[5])
thread3 = threading.Thread(target=popo, args=[8])

thread_mass = [thread1, thread2, thread3]

for i in thread_mass:
    i.start()

for i in thread_mass:
    i.join()