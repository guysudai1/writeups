#actf{w0000sh_1s_th3_s0und_0f_th3_r3qu3st_fly1ng_p4st_th3_fr0nt3nd}
import requests
from pprint import pprint
import socketio
from datetime import datetime
from time import sleep

sio = socketio.Client()
BASE_URL = "https://woooosh.2020.chall.actf.co/"


@sio.event
def connect():
    print("Connection established!")
    sio.emit("start")    
    print("Sent: start")

@sio.on('disp')
def disp(msg):
    print("Tried sending disp... ", msg)

@sio.on('shapes')
def shapes(arr):
    ball_x = arr[0]['x']
    ball_y = arr[1]['y']
    sio.emit("click", (int(ball_x), int(ball_y)))
    print(f"Sent: ({int(ball_x)}, {int(ball_y)})")

@sio.on('score')
def score(score):
    print("[*] Current score: " + str(score))

@sio.event
def message(data):
    print(f"I received data: {data}")

sio.connect(BASE_URL + "socket.io")
sio.wait()
