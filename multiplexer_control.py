from Keithley_controls import *
from requirements import *

mux_commands = [
    "AA0100000000BB", "AA0100000100BB",  # Pixel 1
    "AA0101000000BB", "AA0101000100BB",  # Pixel 2
    "AA0102000000BB", "AA0102000100BB",  # Pixel 3
    "AA0103000000BB", "AA0103000100BB",  # Pixel 4
    "AA0104000000BB", "AA0104000100BB",  # Pixel 5
    "AA0105000000BB", "AA0105000100BB"  # Pixel 6
]


def serialopen(port):
    global ser
    try:
        ser = serial.Serial(port=port, baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE)
    except:
        pass


def muxoperation(ser, value):
    f = bytes.fromhex(value)
    ser.write(f)
    time.sleep(2)


def select_pixel(ser, pixel_number, turn_off=False):
    '''
    Selects or turns off a specific pixel using the multiplexer.

    Parameters:
    - ser (serial.Serial): The serial port for multiplexer control.
    - pixel_number (int): The number of the pixel to be selected or turned off.
    - turn_off (bool): If True, the pixel will be turned off; otherwise, it will be selected.

    Returns:
    None
    '''

    if turn_off == False:
        print(f"Turning off Pixel {pixel_number}")
        # Here, you should send the "turn off" command specific to the pixel
        turn_off_command = f"AA010{pixel_number}000100BB"
        muxoperation(ser, turn_off_command)
    else:
        print(f"Selecting Pixel {pixel_number}")
        # Here, you should send the "turn on" command specific to the pixel
        turn_on_command = f"AA010{pixel_number}000000BB"
        print(turn_on_command)
        muxoperation(ser, turn_on_command)