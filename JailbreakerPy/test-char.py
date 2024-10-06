import socket
import string
import time

class CharacterTester:
    def __init__(self, host="misc.1nf1n1ty.team", port=30010):
        self.host = host
        self.port = port
        
    def test_character(self, char):
        """Test a single character against the server"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((self.host, self.port))
                sock.recv(1024)
                
                payload = f"({char})"
                sock.send(payload.encode() + b'\n')
                response = sock.recv(1024).decode()
                return "Blocked Character" not in response
                
        except Exception as e:
            print(f"Error testing character '{char}': {e}")
            return False
            
    def test_all_characters(self):
        """Test all printable ASCII characters"""
        allowed_chars = []
        blocked_chars = []
        
        chars_to_test = string.printable
        
        print("Starting character testing...")
        print("This may take a few minutes...")
        
        for char in chars_to_test:
            if char in string.whitespace:
                continue
                
            print(f"Testing character: {char}", end='\r')
            
            if self.test_character(char):
                allowed_chars.append(char)
                print(f"\nAllowed character found: {char}")
            else:
                blocked_chars.append(char)
            time.sleep(0.5)
        
        return allowed_chars, blocked_chars

def main():
    tester = CharacterTester()
    
    print("Character Testing Tool for PyJail Challenge")
    print("==========================================")
    print(f"Target: {tester.host}:{tester.port}")
    print("Starting tests...\n")
    
    allowed_chars, blocked_chars = tester.test_all_characters()
    
    print("\n\nResults:")
    print("========")
    print("\nAllowed characters:")
    print(''.join(sorted(allowed_chars)))
    print(f"Total allowed: {len(allowed_chars)}")
    
    print("\nBlocked characters:")
    print(''.join(sorted(blocked_chars)))
    print(f"Total blocked: {len(blocked_chars)}")
    with open("char_test_results.txt", "w") as f:
        f.write("PyJail Character Test Results\n")
        f.write("============================\n\n")
        f.write("Allowed characters:\n")
        f.write(''.join(sorted(allowed_chars)))
        f.write(f"\nTotal allowed: {len(allowed_chars)}\n\n")
        f.write("Blocked characters:\n")
        f.write(''.join(sorted(blocked_chars)))
        f.write(f"\nTotal blocked: {len(blocked_chars)}\n")
    
    print("\nResults have been saved to 'char_test_results.txt'")

if __name__ == "__main__":
    main()
