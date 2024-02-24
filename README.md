# Victure Camera tips and tools
This repository contains scripts I've written to manage my [Victure PC530](https://it.govicture.com/products/victure-pc530n-1080p-baby-monitor-con-videocamera) camera within my local network using [Home Assistant](https://www.home-assistant.io/). 

## IPC360 Security issues
This camera is typically controlled through the [IPC360 Platform](https://play.google.com/store/apps/details?id=com.ipc360&hl=it&gl=US), which has significant vulnerabilities, as detailed in this [BitDefender whitepaper](https://www.bitdefender.com/blog/labs/cracking-the-victure-pc420-camera/). 
Due to these security issues, I opted to block internet access to the camera by manually editing certain configuration files, and the procedure is documented here.

## ONVIF functionality for local video streaming
After disabling internet access, the only way to view the camera's video stream via the local network is by using the ONVIF feature, which needs activation from the IP360 app before blocking internet access. To connect to the camera via ONVIF, you can use software like [Onvif Device Manager](https://github.com/aleksandrm8/ONVIF-Device-Manager), with the following  arguments:

 - URL: http://\<camera IP Address\>:8080/onvif/device_service 
 - user: admin
 - password: 123456

You can also watch the camera's video stream using media player software like VideoLAN VLC with the following RTSP URL::
 rtsp://\<camera IP Address\>:554/realmonitor?channel=1&stream=0.sdp
 In Home Assistant, I utilize [Custom WebRTC Camera Component](https://github.com/AlexxIT/WebRTC) to integrate the camera streaming into my HA Dashoard.

## PTZ Commands
Once internet access is disabled, sending Pan-Tilt-Zoom commands to the camera through the IPC360 app is not possible. However, I found [this post](https://ipcamtalk.com/threads/url-for-generic-ipc365-ip-camera-to-be-used-with-ispy.44633/page-4#post-727935) on IPCamTalk forum. 
on the IPCamTalk forum. 
To locally send PTZ commands to the camera, you need to establish a TCP connection on the camera's port 23456. The byte sequences associated with each command are as follows:
- Right  
`cc dd ee ff 77 4f 00 00 e3 12 69 00 48 00 00 00 00 00 00 00 af 93 c6 3b 09 f7 4b 01 01 00 00 00 00 00 00 00 00 00 00 00 05 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00`

 - Left  
`cc dd ee ff 77 4f 00 00 e3 12 69 00 48 00 00 00 00 00 00 00 af 93 c6 3b 09 f7 4b 01 01 00 00 00 00 00 00 00 00 00 00 00 fb ff ff ff 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00`
  
- Down  
`cc dd ee ff 77 4f 00 00 e3 12 69 00 48 00 00 00 00 00 00 00 af 93 c6 3b 09 f7 4b 01 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 fb ff ff ff 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00`
  
- Up  
`cc dd ee ff 77 4f 00 00 e3 12 69 00 48 00 00 00 00 00 00 00 af 93 c6 3b 09 f7 4b 01 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 05 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00`

### PTZ Commands WPF/C# test app
Based on that information, to test the commands I created a quick and dirty (very, very dirty) C#/WPF application to send commands to the camera. Its code is  available here. 

### PTZ Commands Python Proxy Server
The camera requires a persistent TCP connection to execute commands. For unknown reasons, the commands don't work if the client connects, sends the command, and immediately disconnects. To address this, I wrote a Python script that acts as a proxy server for the camera. It maintains a TCP connection with the camera and listens for incoming connections, forwarding commands when a client connects and sends one. The proxy server script code is available here. 
### Home Assistant configuration 

To send PTZ commands through Home Assistant, I did the following:

- Created an automation to start the Python proxy server at startup
- Set up shell commands associated with PTZ Commands
- Integrated shell commands into an HA script used by the custom WebRTC Camera component.

All YAML configuration files are available [here]().

### Camera time synchronization script
Another small issue arising when you block the camera's internet connection is that it does not synchronize its time anymore. To address this, I wrote a Python script that runs on my HA server every night. It connects via Telnet to the camera and synchronizes it with my local NTP Server. The code is available [here]().
