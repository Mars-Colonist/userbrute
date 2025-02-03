from impacket import smbconnection, ntlm
import sys
from socket import error as SocketError
from time import sleep

def main():
    if len(sys.argv) < 3:
        print("Usage: python %s <target_ip> <username_file>" % sys.argv[0])
        return

    target_ip = sys.argv[1]
    username_file = sys.argv[2]

    try:
        with open(username_file, 'r') as f:
            usernames = [line.strip() for line in f if line.strip()]
    except IOError:
        print("Error: Could not read username file")
        return

    port = 445
    timeout = 10
    detected_users = []

    try:
        conn = smbconnection.SMBConnection(target_ip, target_ip, timeout=timeout)
        conn.connect()

        for username in usernames:
            # Attempting to connect with the current username and anonymous password
            try:
                conn.login(username, '')
                print("Success: Username '%s' exists" % username)
                detected_users.append(username)
                conn.logout()
            except Exception as e:
                if "LOGON_FAIL" in str(e):
                    print("Failure: Username '%s' not found or incorrect password" % username)
                else:
                    print("Error during login attempt for '%s': %s" % (username, str(e)))

            # Optional: Implement a delay to avoid rate limiting
            sleep(1)

        conn.disconnect()

    except SocketError as e:
        print("Connection error: %s" % str(e))
        return

    finally:
        if detected_users:
            print("\nDetected Users:")
            for user in detected_users:
                print(user)
        else:
            print("\nNo valid users found.")

if __name__ == "__main__":
    main()