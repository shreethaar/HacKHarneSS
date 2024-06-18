#! /usr/bin/python3

def rotate(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            is_upper = char.isupper()
            char = chr(((ord(char.lower()) - 97 + shift) % 26) + 97)
            if is_upper:
                char = char.upper()
        result += char
    return result

def search_for_flag(text, flag_header):
    for shift in range(26):
        rotated_text = rotate(text, shift)
        if flag_header in rotated_text:
            return rotated_text
    return None

if __name__ == "__main__":
    text_to_search = input("Enter the encrypted text: ")
    flag_header = input("Enter the flag header (e.g., '***CTF'): ")

    found_flag = search_for_flag(text_to_search, flag_header)
    if found_flag:
        print("Flag found:", found_flag)
    else:
        print("Flag not found.")
