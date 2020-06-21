import os
import sys
import time
import errno
import threading
import pickle

WritePath='pipe\\pipe'
ReadPath='pipe\\pipe'

class ReceiveThread (threading.Thread):

    def default_receive_callback (recv):
        print('received - ' + str(recv))
        return

    recv_callback = default_receive_callback

    def __init__(self):
        threading.Thread.__init__(self)

    def run (self):
        while (True):
            try:
                #Read pipe file
                pipe = open(ReadPath, 'rb')
                while True:
                    data = pickle.load(pipe)
                    self.recv_callback(data)
                return
                #buffer = pipe.readlines()
                #pipe.truncate(0)
                #pipe.close()

                #Iterate and call callback function
                bCount = len(buffer)
                idx=0
                while (idx < bCount):
                    received = pickle.load(buffer[idx])
                    self.recv_callback(received)
                    idx+=1

            except OSError as e:
                if e.errno==11:
                    continue
                else:
                    print('OSError is occurred in ipc thread. You`re fucked up')
                    break

            except EOFError as e:
                time.sleep(0.1)
                continue

            #except:
            #    print('Unknown is occurred in ipc thread. You`re totally fucked up')
            #    break

            time.sleep(0.1)

        print('Receive thread is stopped')

def StartReceiving (callback=None):
    t = ReceiveThread()
    t.recv_callback = callback
    t.start()

def Send(data):
    with open(WritePath, 'wb') as pipe:
        p = pickle.dump(data, pipe)
        #p += bytes(os.linesep.encode('utf-8'))
        #pipe.write(p)


#[아키네이터] [2:35] Send는 전송
#[아키네이터] [2:35] StartReceiving은 수신
#[아키네이터] [2:35] StartReceiving은 콜백함수 하나 등록해두면 수신받았을때 호출될거야
#[아키네이터] [2:35] 콜백함수는 파라미터 하나니까 유의하고
