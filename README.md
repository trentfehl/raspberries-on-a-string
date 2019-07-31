# office-communicator
This project is kind of the modern day cup-on-a-string communication device. Originally conceived to connect two different desks in an office with a fun, hard-wired communication pipe, the office-communicator is a fun way to send messages via a 16x16 LED matrix on one end and 5 buttons on the other. This project utilizes a Raspberry Pi and the Unicorn Hat HD and Button Shim from Pimeroni. Check out the media below and the setup guide if you want to run it yourself.

### In Operation
<p align="center">
<img src="/media/communicator_demo.gif" width="496" height="289">
</p>
<br />

<p align="center">
<img src="/media/default.JPG" width="420px"/> <img src="/media/glasses.JPG" width ="420px"/>
</p>

### Setup
There are a few network and system settings that you'll need to configure
before you can connect your two Raspberry Pis together and have them talking.
Below is most of what you'll need. I made this list from my memory so if you
come across an issue please let me know and I may be able to help you out.

1. Assemble the Pimeroni [Unicorn Hat HD](https://shop.pimoroni.com/products/unicorn-hat-hd) and [Button Shim](https://shop.pimoroni.com/products/button-shim).
2. Get an SD card with the latest verion of [Raspbian](https://www.raspberrypi.org/downloads/raspbian/)
3. Configure static IP addressing in /etc/dhcpcd.conf and connect the Pi to your router via an Ethernet cable.
4. Recommended: I really like interacting with Pis in headless mode. I use most of the steps from the exellent guide [here](https://slippytrumpet.io/posts/raspberry-pi-zero-w-setup/). Keep in mind that if you use that guide you'll need to whitelist the ports used by office-communicator.
5. On the Pi, configure Unicorn Hat HD and Button Shim via the utilities on their GitHub pages ([Hat](https://github.com/pimoroni/unicorn-hat-hd), [Shim](https://github.com/pimoroni/button-shim))
6. Optional: Try out some of the example programs to make sure you've assembled everything correctly.
7. Clone the office-communicator repository.
8. Configure a systemd service to run buttons.py and display.py on boot.
9. Reboot your Pi and make sure the default display starts up. You can also test out the software if you run buttons.py with the argument --loopback.
10. Set this up on a second Pi once you have it running on one. You might want to just make an image of this first one and apply it to a fresh SD card. The guide for setting your Pi up in headless mode had commands for how to create and write images.
11. On the second Pi, you'll still need to configure a DIFFERENT static IP address and make sure that in buttons.py on each device that you have the address of the other device.
12. You should be able to get them talking to each other even with both connected to the router. You can then connect them directly together and that should work too. 

### Acknowledgements
* As usual when working with Pis this guide has been helpful: https://slippytrumpet.io/posts/raspberry-pi-zero-w-setup/
* Sockets were throwing me for a loop. This server/client example was just what I needed: [py3_asyncore_server.py](https://gist.github.com/justinfx/72581492b92444b1fb1116c0fc919cb5#file-py3_asyncore_server-py)
