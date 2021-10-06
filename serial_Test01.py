import serial
import struct
import time
import re
import paho.mqtt.client as mqtt
import json

arduino = None

def on_connect(client, userdata, flags, rc):
    print('connected')
    client.subscribe('smartfarm/control')

# client.publish('smartfarm/control', b'{"type":"led","cmd":"on"}')
def on_message(client, userdata, msg):
    print(msg.topic, msg.payload)
    if msg.topic == 'smartfarm/control':
        try:
            j = json.loads(msg.payload)
            if j['type'] == 'led':
                if j['cmd'] == 'on':
                    arduino.write(b'A')
                else:
                    arduino.write(b'a')
            elif j['type'] == 'fan':
                if j['cmd'] == 'on':
                    arduino.write(b'B')
                else:
                    arduino.write(b'b')
        except Exception as e:
            print(e)
            pass

address = '13.209.41.37'

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(address, 1883)
client.loop_start()

regex = b'^H(.{2})T(.{2})S(.{2})C(.{4})\n$'
def read_arduino(ser):
    m = re.match(regex, ser.readline())
    if m is not None:
        humidity = int.from_bytes(m[1], byteorder='little')
        temperature = int.from_bytes(m[2], byteorder='little')
        soil_humidity = int.from_bytes(m[3], byteorder='little')
        air = struct.unpack('<f', m[4])[0]
        
        return {
            'temperature': temperature,
            'humidity': humidity,
            'air': air,
            'soil_humidity': soil_humidity
        }
    else:
        return None

def run():
    global arduino
    arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    
    arduino.flushInput()
    while True:
        data = read_arduino(arduino)
        if data is not None:
            print('{temperature}°C / {humidity}% / Soil: {soil_humidity}% / Air: {air:.2f}ppm'.format(**data))

            client.publish('smartfarm/sensor', json.dumps(data))
        
        client.loop_read()
        time.sleep(1)
    
    arduino.close()

run()

# ser.flushInput()
# ser.flushOutput()