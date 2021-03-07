#This file is a proof of concept for the TenderServer class. It tests and shows the functionality of TenderServer.

from TenderServer import TenderServer

serv = TenderServer()
work = [0]*5
conns = [0]*5
keys = [0]*5
numConns = 0
msgs = ['']*5
done = False

while not done:
    input('Holding server...')
    work,keys,msgs = serv.CheckEvent()
    j = 0
    while j < len(work):
        if work[j] == 1:
            #Add conn to list
            conns[numConns] = keys[j]
            numConns += 1
        if work[j] == 2:               
            #Just do an echo to the client
            print(msgs[j])
            if msgs[j] != 'bye':
                serv.FormatResponse(keys[j],msgs[j])
            else:
                done = True
        if work[j] == 3:
            #Search conns for match
            i = 0
            while keys[j] != conns[i] and i < numConns:
                i += 1
            
            #remove the conn
            numConns -= 1
            while i <= numConns:
                conns[i] = conns[i+1]
        j += 1

print('Closing Conn')
serv.CloseConn(conns,numConns)