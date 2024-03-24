# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 12:29:52 2023

@author: WAVELABS-R90VZ50M
"""

import time
from tabulate import tabulate
import numpy as np
import keithley_serial as ks
import pyvisa
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from PyPDF2 import PdfWriter, PdfReader
import serial
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
import numpy as np
from io import BytesIO
from datetime import datetime
rm = pyvisa.ResourceManager()
print(rm.list_resources())
keithley=rm.open_resource('ASRL31::INSTR') #established connection with the ketithley device
keithley.set_visa_attribute(pyvisa.constants.VI_ATTR_ASRL_BAUD, 9600) 
keithley.timeout=None
print(keithley.query('*IDN?'))     
ser=serial.Serial(port='COM5',baudrate=115200,bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE)     #a command to ensure connection is established properly. Ideally returns the system names      
mux_commands = [
    "AA0100000000BB", "AA0100000100BB",  # Pixel 1
    "AA0101000000BB", "AA0101000100BB",  # Pixel 2
    "AA0102000000BB", "AA0102000100BB",  # Pixel 3
    "AA0103000000BB", "AA0103000100BB",  # Pixel 4
    "AA0104000000BB", "AA0104000100BB",  # Pixel 5
    "AA0105000000BB", "AA0105000100BB"   # Pixel 6
]
def send_command(keithley, command):
        '''

    Parameters 
    ----------
    command : The command that needs to be written to the keithley device to perform the specific function

    Returns
    -------
    None.

    '''
        response = ks.write(keithley, command)      
        
def set_sensor_type(keithley, sensor_type):
    '''
    

    Parameters
    ----------
    sensor_type : Pass as CURR , VOLT sets the keithleys sensing mode to current sensor or voltage sensor
    Returns
    -------
    None.

    '''
    sensor_type = sensor_type.lower()
    if sensor_type == 'current' or sensor_type == 'curr' or sensor_type == 'c':
        send_command(keithley,':SENS:FUNC "CURR"')
        
    elif sensor_type == 'voltage' or sensor_type == 'volt' or sensor_type == 'v':
          send_command(keithley,':SENS:FUNC "VOLT"')
        
    else:
        print("Unknown sensor setting!")
        return None


def set_source_type(keithley, source_type):
    '''
    

    Parameters
    ----------
    sensor_type : Pass as CURR , VOLT sets the keithleys source mode to current or voltage sources
    Returns
    -------
    None.
    '''
    source_type = source_type.lower()
    if source_type == 'current' or source_type == 'curr' or source_type == 'c':
        send_command(keithley,':SOUR:FUNC CURRENT')
    elif source_type == 'voltage' or source_type == 'volt' or source_type == 'v':
        send_command(keithley,':SOUR:FUNC VOLT')
    else:
        print("Unknown source setting!")
        
# Function to send commands to Keithley device
def send_command(keithley, command):
    keithley.write(command)

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
    
    if turn_off==False:
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
        


def mux(keithley, ser, pixel_count, num_sweeps, start, stop, step):
    '''
    Coordinates measurements for multiple pixels by switching between them, performing sweeps, and saving data to text files.

    Parameters:
    - keithley (pyvisa.Resource): The Keithley device resource.
    - ser (serial.Serial): The serial port for multiplexer control.
    - pixel_count (int): The total number of pixels to be measured.
    - num_sweeps (int): The number of voltage sweeps to perform.
    - start (float): The starting voltage for the sweeps.
    - stop (float): The ending voltage for the sweeps.
    - step (float): The voltage step size.

    Saves data for each pixel in separate text files.
    '''
    pdf_file_path='plots.pdf'
    # Calculate the number of subplots needed for the given pixel_count
    num_rows = 3
    num_cols = 2
    a4_width_inches = 8.27
    a4_height_inches = 11.69
    # Initialize the figure with dynamically determined layout
    fig, ax = plt.subplots(nrows=num_rows, ncols=num_cols, figsize=(8, 6))
    plt.subplots_adjust(wspace=0.3, hspace=0.5)
    with PdfPages(pdf_file_path) as pdf:
        for pixel_number in range(0, pixel_count):
            # Turn on the current pixel
            select_pixel(ser, pixel_number, turn_off=True)
            row_index = pixel_number // num_cols
            col_index = pixel_number % num_cols
            # Continue with voltage sweeps and data collection for the current pixel
            voltage_values, current_values, time_values = sweep(keithley, start, stop, step, num_sweeps,0)
            voltage_values_d, current_values_d, time_values_d = sweep(keithley, start, stop, step, num_sweeps,1)
            print('start saving')
            
            
            combined_voltage_values = voltage_values + voltage_values_d
            combined_current_values = current_values + current_values_d
            
            
            
            # Save data for the current pixel in a text file
            save_data_to_file(pixel_number, combined_voltage_values, combined_current_values)
            print('change mux')
            # Turn off the current pixel after completing its measurements
            select_pixel(ser, pixel_number, turn_off=False)   
            plot_new(combined_voltage_values, combined_current_values, pixel_number, ax[row_index, col_index])
        fig.set_size_inches(a4_width_inches, a4_height_inches)
        pdf.savefig()
        plt.close()       
    return pdf_file_path

def save_data_to_file(pixel_number, voltage_values, current_values):
    # Define the file name based on the pixel number
    file_name = f'pixel_{pixel_number}_data.txt'
    data_table = list(zip(voltage_values, current_values))
    # Open the file in write mode and save the data
    with open(file_name, 'w') as file:
        file.write("Voltage\t \t Current\n")
        file.write(tabulate(data_table, tablefmt='plain', floatfmt=('.6f', '.6e')))
            

def plot_new(vvalues,cvalues,pixel_number,ax):
    for i in range(len(cvalues)):
        cvalues[i]=cvalues[i]*-1
    # # Plot the data
    ax.plot(vvalues, cvalues)
    # # Set title and labels
    ax.set_title(f' Pixel {pixel_number}')
    ax.set_xlabel("VOLTAGE(V)")
    ax.set_ylabel("CURRENT(A)")



def sweep(keithley, start, stop, step, num_sweeps,direction):
    '''
    This function performs a voltage sweep on the Keithley device.

    Parameters:
    - keithley (pyvisa.Resource): The Keithley device resource.
    - start (float): The starting voltage for the sweeps.
    - stop (float): The ending voltage for the sweeps.
    - step (float): The voltage step size.
    - num_sweeps (int): The number of voltage sweeps to perform.

    Returns:
    Lists of voltage and current values for each sweep.
    '''
    
    sweep_points = int((stop - start) / step) + 1
    num_trigs = sweep_points

    all_voltage_values = []
    all_current_values = []
    all_time_values=[]

   # for i in range(num_sweeps):
    send_command(keithley, ':FORM:ELEM VOLT,CURR,TIME')
    send_command(keithley, ':SOUR:FUNC VOLT')
    time.sleep(0.1)
    send_command(keithley, ':SENS:FUNC "CURR"')
    time.sleep(0.1)
    send_command(keithley, ':SENSE:CURR:PROT 0.3')
    time.sleep(0.1)
    send_command(keithley, ':SOUR:VOLT:MODE SWE')
    time.sleep(0.1)
    send_command(keithley, ':SOUR:SWE:RANG FIX')
    time.sleep(0.1)
    send_command(keithley, ':SOUR:SWE:SPAC LIN')
    time.sleep(0.1)
    if (direction==0):
        send_command(keithley, ':SOUR:SWE:DIR UP')
    else:
        send_command(keithley, ':SOUR:SWE:DIR DOWN')
    send_command(keithley, f':SOUR:VOLT:START {start}')
    time.sleep(0.1)
    send_command(keithley, f':SOUR:VOLT:STEP {step}')
    time.sleep(0.1)
    send_command(keithley, f':SOUR:VOLT:STOP {stop}')
    time.sleep(0.1)
    send_command(keithley, f':SOUR:SWE:POIN {sweep_points}')
    time.sleep(0.1)
    send_command(keithley, f':TRIG:COUN {num_trigs}')
    time.sleep(0.1)
    send_command(keithley, ':SOUR:DEL 0.5')
    send_command(keithley, ':OUTP ON')

    voltage_data = []
    current_data = []
    time_data=[]
    keithley.write(':INIT')
    time.sleep(1)
    print('sweep done')
    response = keithley.query(':READ?')
    data = [float(val) for val in response.split(',')]
    
    
    vvalues=data[0::3]
    cvalues=data[1::3]
    tvalues=data[2::3]
    print(tvalues)
    print('----------------------------')
    print(vvalues)
    print('----------------------------')
    print(cvalues)
    
    
    
    # voltage_data.append(data[0])
    # current_data.append(data[1])
    # time_data.append(data[2])
    print('store done')
    # all_voltage_values.append(voltage_data)
    # all_current_values.append(current_data)
    # all_time_values.append(time_data)
    send_command(keithley, ':OUTP OFF')

    return vvalues, cvalues, tvalues




def run_start_up_commands(keithley):
    '''
    
     Function to run when the device is startup. It sets all device paramters to its default value

    Returns
    -------
    None.

    '''
    for com in start_up_commands:
        send_command(keithley,com)
        time.sleep(.01)

def constantvoltagemeasureself(keithley,k):
    '''
    
    Function to measure current at a fixed voltage value accross time.
    Parameters
    ----------
    k : TYPE
        DESCRIPTION. The voltage to be fixed

    Returns
    -------
    None.

    '''
    send_command(keithley,':SOUR:FUNC VOLT')
    send_command(keithley,':SENS:FUNC "CURR"')
    send_command(keithley,':SENSE:CURR:PROT 0.2')
    send_command(keithley,':SOUR:VOLT:MODE FIX')
    send_command(keithley,':SOUR:VOLT:LEV %f' %k)
    send_command(keithley,':FORM:ELEM CURR,TIME')
    send_command(keithley,':OUTP ON')
    send_command(keithley,':INIT')
    send_command(keithley,':TRIG:COUN 5')
    send_command(keithley,':SOUR:DEL 0.1')
    response=keithley.query(':READ?')
    time.sleep(1)
    send_command(keithley,':OUTP OFF')
    print(response)
    data=[float(val) for val in response.split(',')]
    cvalues=data[0::2]
    tvalues=data[1::2]
    plt.plot(tvalues, cvalues) 
    plt.xlabel("TIME(s)")
    plt.ylabel("CURRENT(A)")            
    plt.pyplot.show()
    
    
def constantcurrentmeasureself(keithley,k):
    '''
    
    Function to measure voltage at a fixed current value accross time.
    Parameters
    ----------
    k : TYPE
        DESCRIPTION. The voltage to be fixed

    Returns
    -------
    None.

    '''
    send_command(keithley,':SOUR:FUNC CURR')
    send_command(keithley,':SENS:FUNC "VOLT"')
    send_command(keithley,':SENSE:VOLT:PROT 10')
    send_command(keithley,':SOUR:CURR:MODE FIX')
    send_command(keithley,':SOUR:CURR:%f' %k)
    send_command(keithley,':FORM:ELEM VOLT,TIME')

    send_command(keithley, ':SYST:RSEN ON')
    send_command(keithley,':OUTP ON')
    send_command(keithley,':INIT')
    send_command(keithley,':TRIG:COUN 10')
    send_command(keithley,':SOUR:DEL 1')
    response=keithley.query(':READ?')
    time.sleep(1)

    send_command(keithley, ':SYST:RSEN OFF')
    send_command(keithley,':OUTP OFF')
    print(response)
    data=[float(val) for val in response.split(',')]
    vvalues=data[0::2]
    tvalues=data[1::2]
    plt.plot(tvalues, vvalues) 
    plt.xlabel("TIME(s)")
    plt.ylabel("VOLT(v)")           
    plt.pyplot.show()



def add_page_heading(pdf_path, title, author, other_details,current_date):
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)

    # Set font and size for the heading
    can.setFont("Helvetica", 16)

    # Add heading details
    can.drawString(160, 550, f"Title: {title}")
    can.drawString(160, 530, f"Author: {author}")
    can.drawString(160, 510, f"Other Details: {other_details}")
    can.drawString(160, 490, f"Date: {current_date}")
    # Save the canvas
    can.save()

    # Move the packet cursor to the beginning
    packet.seek(0)

    # Create a new PDF with the heading
    new_pdf = PdfReader(packet)
    existing_pdf = PdfReader(open(pdf_path, "rb"))
    output_pdf = PdfWriter()

    # Add the heading page
    heading_page = new_pdf.pages[0]
    output_pdf.add_page(heading_page)

    # Add the existing pages
    for i in range(len(existing_pdf.pages)):
        page = existing_pdf.pages[i]
        output_pdf.add_page(page)

    # Write the combined PDF to a new file
    with open("final_plots.pdf", "wb") as final_pdf:
        output_pdf.write(final_pdf)



#the various startup commands that need to be excecuted at the start of the system. 
start_up_commands = ["*RST",
                     ":SYST:TIME:RES:AUTO 1",
                     ":SYST:BEEP:STAT 1",
                     ":SOUR:FUNC CURR",
                     ":SENS:FUNC:CONC OFF",
                     ":SENS:AVER:STAT OFF",
                     ":SENS:CURR:NPLC 0.01",
                     ":SENS:VOLT:NPLC 0.01",
                     ":SENS:RES:NPLC 0.01",
                     ":SENS:FUNC 'VOLT'",
                     ":SENS:VOLT:RANG 1e1",
                     ":TRIG:DEL 0.0",
                     ":SYST:AZER:STAT OFF",
                     ":SOUR:DELAY 0.0",
                     ":DISP:ENAB ON"]

run_start_up_commands(keithley)
print('start done')
set_source_type(keithley, 'voltage')
set_sensor_type(keithley, 'current')
# Specify sweep parameters
start_voltage = -0.2
stop_voltage = 1.2
voltage_step = 0.2
num_sweeps = 29
pixel_count=6
# Get the current date and time
current_datetime = datetime.now()
current_date = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
#read(keithley, start_voltage, stop_voltage, voltage_step, num_sweeps)
output_file_path=mux(keithley, ser, pixel_count, num_sweeps, start_voltage, stop_voltage, voltage_step)
add_page_heading(output_file_path, "My Plots", "Abhishek O", "Plots of pixels",current_date)
ser.close()
print('Closed')