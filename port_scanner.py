import socket
import threading
from queue import Queue

# Port scanning function
def scan_port(target_ip, port, q):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # 1 second timeout
        result = sock.connect_ex((target_ip, port))
        
        # If the connection is successful
        if result == 0:
            q.put(port)  # Add open ports to the queue
            # Banner grabbing (getting information about the port)
            try:
                banner = sock.recv(1024).decode().strip()
                print(f"Port {port} is open! ({banner})")
            except:
                print(f"Port {port} is open!")
        sock.close()
    except Exception as e:
        pass

# Function to scan ports with multiple threads
def port_scan(target_ip, start_port, end_port):
    print(f"\nStarting port scan on: {target_ip}")
    open_ports = []
    q = Queue()
    
    # Start threads for all ports
    threads = []
    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=scan_port, args=(target_ip, port, q))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    # Get all open ports from the queue
    while not q.empty():
        open_ports.append(q.get())
    
    if open_ports:
        print(f"\nOpen Ports: {open_ports}")
    else:
        print("\nNo open ports found.")

# Get user input
target_ip = input("Enter target IP address: ")
start_port = int(input("Enter starting port: "))
end_port = int(input("Enter ending port: "))

# Run the port scanner
port_scan(target_ip, start_port, end_port)
