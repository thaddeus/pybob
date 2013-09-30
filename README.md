pybob
=====

Python 3 interface for boblightd (LED controller)

Documentation
-------------
It's as simple as typing 
```python
import pybob
b = pybob.Boblights()
b.open()
b.set_light(b.get_lights()[0], "FF0000")
b.sync()
time.sleep(10)
b.close();
```

Useful functions
```python
b.open() #Open a connection to the server
b.set_light(light_name, hex_color, brightness_multiplier) #Set an individual light to a specified color
b.set_lights(hex_color, brightness_multiplier) #Set all lights reporting by the server to a specified color
b.set_use(light_name, true_false) #Enable/disable use of a light by this particular client, useful when running two or more clients
b.set_speed(light_name, refresh_percent) #Set the speed at which a light changes color
b.sync() #After sending bulk data to the server, manually push changes to the lights
b.close() #Properly exit the client connection
```
