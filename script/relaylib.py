import socket
import string

def comando(host,port,command):
    reply=[]
    if len(command) > 0:
       try:
          client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
          client_socket.connect((host, port))
          client_socket.send(command)
          replychunk = client_socket.recv(16)
          while len(replychunk):
             reply.append(replychunk)
             replychunk = client_socket.recv(16)
          client_socket.close()
       except socket.error:
          reply.append("%12% *Server NON risponde*")
    else:
       reply.append("%11% *Comando assente*")       
    return ''.join(reply)

def accendi(host,port,gpioch):
    return comando(host,port,"accendi %s" %(gpioch))

def spegni(host,port,gpioch):
    return comando(host,port,"spegni %s" %(gpioch))

def stato_gpio(host,port,gpioch):
    return comando(host,port,"stato %s" %(gpioch))

def abilita_bit(host,port,gpioch,bit):
    return comando(host,port,"abilita %s %d" % (gpioch,bit))

def disabilita_bit(host,port,gpioch,bit):
    return comando(host,port,"disabilita %s %d" % (gpioch,bit))

def configura_bit(host,port,gpioch,bitmask):
    return comando(host,port,"configura %s %d" % (gpioch,bitmask)) 

def stato(host,port):
    statusstring = comando(host,port,"stato")
    statuslist = statusstring.split("\n")
    gpioch=[]
    name=[]
    nbits=[]
    bitstatus=[]
    oncond=[]
    locked=[]
    status=[]
    statusdict={'gpioch':gpioch,'name':name,'nbits':nbits,'bitstatus':bitstatus,'oncond':oncond,'locked':locked,'status':status}
    for gpiostatusstring in statuslist[1:]:
        gpiostatus = gpiostatusstring.split(" ")
        if len(gpiostatus)==7:
            gpioch.append(int(gpiostatus[0])) 	
            name.append(gpiostatus[1])	
            nbits.append(int(gpiostatus[2])) 	
            oncond.append(int(gpiostatus[3])) 	
            bitstatus.append(int(gpiostatus[4])) 	
            locked.append(int(gpiostatus[5])) 	
            status.append(int(gpiostatus[6])) 	
    return statuslist[0],statusdict
       
