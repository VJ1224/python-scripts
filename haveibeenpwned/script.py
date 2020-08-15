import hashlib
import sys
import requests


def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <password>")
        return

    password = sys.argv[1]
    url = "https://api.pwnedpasswords.com/range/"

    hash_pass = hashlib.sha1(password.encode('utf-8'))
    hex_pass = hash_pass.hexdigest()

    url = url + hex_pass[0:5]
    hex_pass = hex_pass.upper()
    hex_pass = hex_pass[5:]
    
    result = requests.get(url)
    password_set = result.text.split("\n")

    for entry in password_set:
        password = entry.split(":")
        
        if password[0] == hex_pass:
            count = password[1][:-1]
            print("Your password was found {n} times".format(n=count))
            return
    
    print("Your password was not found")


if __name__ == "__main__":
    main()
