import socket
import string
import time

class CharacterTester:
    def __init__(self, host="misc.1nf1n1ty.team", port=30010, delay=0.2):
        self.host = host
        self.port = port
        self.delay = delay

    def test_character(self, char):
        """Test a single character against the server"""
        try:
            # Create a new socket for each test
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((self.host, self.port))
                # Receive welcome banner
                sock.recv(1024)

                # Create a simple payload using the character
                # We'll use a basic expression that should be valid Python
                payload = f"({char})"

                # Send the payload
                sock.sendall(payload.encode() + b'\n')

                # Get the response
                response = sock.recv(1024).decode()

                # If we don't see "Blocked Character" in the response, the character is allowed
                if "Blocked Character" in response:
                    return False
                return True

        except Exception as e:
            print(f"Error testing character '{char}': {e}")
            return False

    def test_all_characters(self):
        """Test all printable ASCII characters"""
        allowed_chars = []
        blocked_chars = []

        # Generate all characters to test
        chars_to_test = string.printable.strip()  # Remove any unwanted whitespace

        print("Starting character testing...")
        print("This may take a few minutes...")

        for char in chars_to_test:
            # Log the progress of the current character being tested
            print(f"Testing character: {repr(char)}", end='\r')

            if self.test_character(char):
                allowed_chars.append(char)
                print(f"\nAllowed character found: {repr(char)}")
            else:
                blocked_chars.append(char)

            # Add a small delay to avoid overwhelming the server
            time.sleep(self.delay)

        return allowed_chars, blocked_chars

def save_results(allowed_chars, blocked_chars):
    """Save test results to a file"""
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

    # Save results to a file
    save_results(allowed_chars, blocked_chars)

if __name__ == "__main__":
    main()

