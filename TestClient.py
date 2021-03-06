#This file is a proof of concept for the TenderClient class. It tests and shows the functionality of TenderClient.

from TenderClient import TenderClient

client = TenderClient()

toSend = input('To Send: ')
toSend.lower()
while toSend != 'quit':
    #client.WriteRead(toSend)
    client.WriteToSock(toSend)
    recv = client.ReadFromSock()
    print(recv)
    if recv != 'quit':
        toSend = input('To Send: ')
        toSend.lower()
    else:
        toSend = recv

client.CloseConn()