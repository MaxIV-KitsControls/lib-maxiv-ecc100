# lib-maxiv-ecc100

Communication library for the Attocube ECC100 three axes piezo motion controller.
Based on the C protocol provided by Attocube adapted to python.

## Usage

The main file is `libECC100.py`, if you run it directly some test code is launched which will retrieve and change positions of the axis. See the file and change the `host_list` based on your local settings.

Example output:

```
$ python libECC100.py
Starting test program...
Controller host:  172.16.118.51
connected axis names:  ECS3030 ECS3030 ECS3030
AXIS 0 >>> Position:  498.0 | Connected:  1
AXIS 1 >>> Position:  1005.0 | Connected:  1
AXIS 2 >>> Position:  1499.0 | Connected:  1
Connection closed
#################

$$$$$$$$$$$

Moving to new positions...
Controller host:  172.16.118.51
AXIS 0 >>> Position:  599.0
AXIS 1 >>> Position:  1203.0
AXIS 2 >>> Position:  1800.0
Connection closed
#################
```

If you import the file:
```python
import libECC100
controller = libECC100.ECC100('your_hostname')

controller.get_firmware()  		## '20160427'
controller.axis_connected(0) 	## 1
controller.get_position(0)  	## 599.0
```



## Known issues

* Some call generate a huge response by the server (far larger than the expected response size), that's why some methods repeat the call if there is any exeption. Same can be achieved by closing and reconnecting the socket.

* One should not allow any call on a disconnected axis.
## Credits

TODO: Write credits

## License

TODO: Write license