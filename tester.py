# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 12:29:52 2023

@author: WAVELABS-R90VZ50M
"""

import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from PyPDF2 import PdfWriter, PdfReader
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
import numpy as np
from io import BytesIO
from datetime import datetime
from tabulate import tabulate

mux_commands = [
    "AA0100000000BB", "AA0100000100BB",  # Pixel 1
    "AA0101000000BB", "AA0101000100BB",  # Pixel 2
    "AA0102000000BB", "AA0102000100BB",  # Pixel 3
    "AA0103000000BB", "AA0103000100BB",  # Pixel 4
    "AA0104000000BB", "AA0104000100BB",  # Pixel 5
    "AA0105000000BB", "AA0105000100BB"  # Pixel 6
]


def mux(pixel_count, num_sweeps, start, stop, step):
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
    pdf_file_path = 'plots_test.pdf'
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
            row_index = pixel_number // num_cols
            col_index = pixel_number % num_cols
            # Continue with voltage sweeps and data collection for the current pixel
            voltage_values, current_values = generate_c_and_v(pixel_number)
            print('start saving')
            # Save data for the current pixel in a text file
            save_data_to_file(pixel_number, voltage_values, current_values)
            print('change mux')
            # Turn off the current pixel after completing its measurements
            plot_new(voltage_values, current_values, pixel_number, ax[row_index, col_index])
        fig.set_size_inches(a4_width_inches, a4_height_inches)
        pdf.savefig()
        plt.close()
    return pdf_file_path


def save_data_to_file(pixel_number, voltage_values, current_values):
    # Define the file name based on the pixel number
    file_name = f'pixel_{pixel_number}_data.txt'

    # Combine voltage and current values into a table
    data_table = list(zip(voltage_values, current_values))

    # Open the file in write mode and save the data as a table
    with open(file_name, 'w') as file:
        # Write headings
        file.write("Voltage\t \t Current\n")
        # Write the table with customized formatting
        file.write(tabulate(data_table, tablefmt='plain', floatfmt=('.6f', '.6e')))


def plot_new(vvalues, cvalues, pixel_number, ax):
    for i in range(len(cvalues)):
        cvalues[i] = cvalues[i] * -1
    # # Plot the data
    ax.plot(vvalues, cvalues)
    # # Set title and labels
    ax.set_title(f' Pixel {pixel_number}')
    ax.set_xlabel("VOLTAGE(V)")
    ax.set_ylabel("CURRENT(A)")


def generate_c_and_v(pixel_count):
    cvalues=[]
    vvalues=[]
    if (pixel_count==0):
        cvalues = [2.68119e-08, -1.632134e-08, -1.198021e-08, -1.869012e-09, -6.030973e-09, -5.018592e-09, -1.126784e-08]
        vvalues= [1.2,0.96665,0.73335,0.5,0.26665,0.033335,-0.2]
    elif (pixel_count==1):
        cvalues = [-3.442744e-08, 1.665182e-08, -2.341949e-11, -1.869012e-09, 8.56619e-09, -5.018592e-09, 9.645078e-09]
        vvalues = [1.2, 0.96665, 0.73335, 0.5, 0.26665, 0.033335, -0.2]
    elif (pixel_count==2):
        cvalues = [2.68119e-08, -1.632134e-08, -1.198021e-08, -1.869012e-09, -6.030973e-09, -5.018592e-09, -1.126784e-08]
        vvalues = [1.2, 0.96665, 0.73335, 0.5, 0.26665, 0.033335, -0.2]
    elif (pixel_count==3):
        cvalues = [2.68119e-08, -1.632134e-08, -1.198021e-08, -1.869012e-09, -6.030973e-09, -5.018592e-09, -1.126784e-08]
        vvalues = [1.2, 0.96665, 0.73335, 0.5, 0.26665, 0.033335, -0.2]
    elif (pixel_count==4):
        cvalues = [1.421995e-09, -9.816858e-10, -1.201772e-08, -6.205937e-09, 1.902208e-08, -5.018592e-09, -6.82121e-12]
        vvalues = [1.2, 0.96665, 0.73335, 0.5, 0.26665, 0.033335, -0.2]
    elif (pixel_count==5):
        cvalues = [2.68119e-08, -1.632134e-08, -1.198021e-08, -1.869012e-09, -6.030973e-09, -5.018592e-09, -1.126784e-08]
        vvalues = [1.2, 0.96665, 0.73335, 0.5, 0.26665, 0.033335, -0.2]

    return vvalues,cvalues
def add_page_heading(pdf_path, title, author, other_details, current_date):
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
    with open("final_plots_test.pdf", "wb") as final_pdf:
        output_pdf.write(final_pdf)



start_voltage = -0.2
stop_voltage = 1.2
voltage_step = 0.2
num_sweeps = 29
pixel_count = 6
# Get the current date and time
current_datetime = datetime.now()
current_date = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
# read(keithley, start_voltage, stop_voltage, voltage_step, num_sweeps)
output_file_path = mux(pixel_count, num_sweeps, start_voltage, stop_voltage, voltage_step)
add_page_heading(output_file_path, "My Plots", "Abhishek O", "Plots of pixels", current_date)