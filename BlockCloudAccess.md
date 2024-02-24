# Block cloud access to Victure Camera
This is the procedure I followed to block camera's access to IPC360 cloud. Please note this does not block overall internet access, but the IPC360 server will not be anymore reachable after these steps, so you won't be able to command the camera using the IPC360 app.
1. Enable ONVIF from the IPC360 app, so you'll still be able to watch the camera video streaming using the local network URL (see the [main readme](README.md)).
2. Connect via telnet to the camera ip address. The credential login is 'root', no password is required.
3. Run command  `cd puwell/mtd/Config` to move to the configuration directory.
4. Run command  `echo '' > resolv.conf` to empty the DNS configuration file. Doing this, the camera will not be able to resolve the cloud servers host names.
5. Run command `echo '' > IP_DNSBackups.conf` to empty the IP Address backup configuration file. This file is used when DNS Resolution fails, and contains the IP Addresses of the IPC360 cloud servers.

# Block Cloud Access to Victure Camera

This procedure outlines the steps to block the camera's access to the IPC360 cloud. Please note that this doesn't block overall internet access, but the IPC360 servers become unreachable after these steps, preventing commands to the camera using the IPC360 app.

1.  **Enable ONVIF from the IPC360 App:**
    
    -   This allows you to continue watching the camera video stream using the local network URL (refer to the [main readme](https://chat.openai.com/c/README.md)).
2.  **Connect via Telnet to the Camera IP Address:**
    
    -   Use the credentials 'root' with no password.
3.  **Navigate to the Configuration Directory:**
    
    -   Run command `cd puwell/mtd/Config` to move to the configuration directory.
4.  **Empty the DNS Configuration File:**
    
    -   Run command `echo '' > resolv.conf` to clear the DNS configuration file. This action prevents the camera from resolving cloud server hostnames (actually, any hostname)
5.  **Empty the IP Address Backup Configuration File:**
    
    -   Run command `echo '' > IP_DNSBackups.conf` to clear the IP Address backup configuration file. This file is utilized when DNS resolution fails and contains the IP Addresses of the IPC360 cloud servers.