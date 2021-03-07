import selectors
import socket
import types

class TenderServer:  
    #Constructor
    #Set up the socket on localhost:12345 and selector.
    def __init__(self):
        self.sel = selectors.DefaultSelector()
        self.lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostname()
        port = 12345
  
        self.lsock.bind((host, port))        # Bind to the port
        self.lsock.listen()
        print('listening on', (host, port))
        
        self.lsock.setblocking(False)
        self.sel.register(self.lsock, selectors.EVENT_READ, data=None)

    #CheckEvent
    #This needs to be called once per work loop in Server application.
    #Checks for new conn, read, or write events and dispatches calls
    #to the appropriate method.
    #Returns 0,0'0' if accepting wrapper or write event
    #Returns 1,key,'0' if handling signon msg
    #Returns 2,key,msg if handling a transaction msg
    #Returns 3,key,'0' if handling signoff msg
    def CheckEvent(self):
        #while True:
        events = self.sel.select(timeout=None) #Possible hang up here. Need to do some testing. - HEF
        works = [0]*5
        keys = [0]*5
        msgs = [0]*5
        i = 0
        for key, mask in events:
            if key.data is None:
                self.AcceptWrapper(key.fileobj)
                works[i] = 0
                keys[i] = key
                msgs[i] = '0'
            else: 
                works[i],keys[i],msgs[i] = self.ServiceConnection(key, mask)
            i += 1
        return works,keys,msgs
                    
    #AcceptWrapper
    #Handle a new connection
    def AcceptWrapper(self,sock):
        conn, addr = sock.accept()  # Should be ready to read
        print('accepted connection from', addr)
        conn.setblocking(False)
        data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.sel.register(conn, events, data=data)
        
    #ServiceConnection
    #Reads or Echoes on a Socket.
    #Expects a new connection to be followed up with signon message
    #We need to enhance this. If this is a read, let the Server know there is something
    def ServiceConnection(self,key, mask):
        sock = key.fileobj
        data = key.data
        #If we're ready to read, receive the data. If it is a connection close notification,
        #close the related socket
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024)  # Should be ready to read
            if recv_data: #Do we have data
                decoded = recv_data.decode()
                if decoded == 'signon':
                    return 1,key,'0'
                else:
                    return 2,key,decoded
            else:
                print('closing connection to', data.addr)
                self.sel.unregister(sock)
                sock.close()
                return 3,key,'0'
        #If we're ready to write, echo
        if mask & selectors.EVENT_WRITE:
            if data.outb:
                print('echoing', repr(data.outb), 'to', data.addr)
                sent = sock.send(data.outb)  # Should be ready to write
                data.outb = data.outb[sent:]
        return 0,key,'0'
        
    #FormatResponse
    #Takes the key returned by AcceptWrapper mapped to the client and the string message to send.
    #Format the message and put it in the data.outb of the client.
    def FormatResponse(self,key,msg):
        data = key.data
        data.outb = str.encode(msg)
        
    #CloseConn
    #Clean up selectors and close the socket. This should only happen when the server is taken down for maintenance.
    def CloseConn(self,conns,numConns):
        i = 0
        while i < numConns:
            conns[i].fileobj.close()
            i += 1
        print('socks closed')
        self.sel.close()
        self.lsock.close()
        print('done closing conn')
    