import pexpect

def telnet_session(ip, port, username, password, command):
    import pexpect
    # Construct the telnet command
    telnet_command = f"telnet {ip} {port}"

    # Spawn a new telnet process
    telnet_session = pexpect.spawn(telnet_command)

    try:
        # Expect the initial login prompt
        telnet_session.expect("login:")

        # Send the username
        telnet_session.sendline(username)

        # Expect the command prompt
        telnet_session.expect("puwell login:")

        # Send the command
        telnet_session.sendline(command)

        # Wait for the command to finish and print the output
        telnet_session.expect(pexpect.EOF)
        print(telnet_session.before.decode())
    except pexpect.exceptions.ExceptionPexpect as e:
        print(f"Error: {e}")
    finally:
        # Close the telnet session
        telnet_session.close()

# Specify the telnet details and command
telnet_ip = "192.168.1.10" # Victure Camera IP Address
telnet_port = 23
telnet_username = "root"
telnet_password = ""
telnet_command = "ntpd -q -n -p 192.168.1.250" #Local NTP Server IP Address

# Call the telnet_session function
telnet_session(telnet_ip, telnet_port, telnet_username, telnet_password, telnet_command)