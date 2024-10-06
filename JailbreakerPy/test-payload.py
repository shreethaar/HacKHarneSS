
import builtins
import keyword
import string
import socket

allowed_chars = set("$(),/1:;=EHSUVWYZ]bcdinqz{")
banned_letters = set("abcdefghijklmnopqrstuvwxyz") - allowed_chars
banned_symbols = set(string.punctuation) - allowed_chars
banned_words = ["flag"]  

def is_allowed(word):
    return not any(c in word for c in banned_letters.union(banned_symbols).union(banned_words))

server_address = "misc.1nf1n1ty.team"
server_port = 30010
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(2)  
sock.connect((server_address, server_port))

globals_list = list(globals().keys())

payloads = []
for w in globals_list:
    if is_allowed(w):
        payloads.append(w)
for w in builtins.__dict__:
    if is_allowed(w):
        payloads.append(w)
for w in keyword.kwlist:
    if is_allowed(w):
        payloads.append(w)
for w in string.punctuation:
    if w in allowed_chars:
        payloads.append(w)

for payload in payloads:
    try:
        sock.sendall(payload.encode())
        response = sock.recv(1024).decode()  
        print(f"Payload: {payload}, Response: {response}")
    except socket.timeout:
        print(f"Payload: {payload}, No response within the timeout period.")
    except Exception as e:
        print(f"Payload: {payload}, Error: {e}")

sock.close()
