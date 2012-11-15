import socket, json
import time, os
def print_dic(dic):
    os.system("clear")
    for i in range(8):
        l = dic[str(i)]
        p = [" " for k in range(8)]
        for j in l:
            p[j] = "O"
        print '|'.join(p)

if __name__ == '__main__':
    while(1):
        s = socket.socket()
        s.connect(('',50000))
        a = {"level":100, "threshold":0.5, "invert": True}
        b = json.dumps(a)
        s.send(b)
        c = s.recv(1024)
        s.close()
        d = json.loads(c)
        #print '\n'.join([str(i) + " : " + str(d[i]) for i in d])
        print_dic(d)
        time.sleep(0.5)


