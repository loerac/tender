#This file is a proof of concept for the TenderServer class. It tests and shows the functionality of TenderServer.

from TenderServer import TenderServer

serv = TenderServer()
work = 0
conns = [0]*5
numConns = 0
msg = ''

while msg != 'bye':
    work,key,msg = serv.CheckEvent()

    if work == 1:
        #Add conn to list
        conns[numConns] = key
        numConns += 1
    if work == 2:
        #Search conns for match
        i = 0
        while key != conns[i]:
            i += 1
            
        #Just do an echo to the client
        print(msg)
        if msg != 'bye':
            serv.FormatResponse(conns[i],msg) #We could instead do FormatResponse(key,msg), but for POC we do the extra stuff
    if work == 3:
        #Search conns for match
        i = 0
        while key != conns[i]:
            i += 1
        
        #remove the conn
        numConns -= 1
        while i <= numConns:
            cons[i] = cons[i+1]

print('Closing Conn')
serv.CloseConn(conns,numConns)