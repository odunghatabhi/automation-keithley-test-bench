# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 12:29:52 2023

@author: WAVELABS-R90VZ50M
"""

from requirements import *
from Keithley_controls import *
from multiplexer_control import *
from data_analysis import *
def get_mpp(power_values):
    mpp_index = np.argmax(power_values)
    return mpp_index

def mux(keithley, ser, pixel_count, start, stop, step,username):
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
            voltage_values, current_values, time_values = sweep(keithley, start, stop, step,0)
            voltage_values_d, current_values_d, time_values_d = sweep(keithley, start, stop, step,1)
            print('start saving')
            
            
            combined_voltage_values = voltage_values + voltage_values_d
            combined_current_values = current_values + current_values_d
            power_values=np.multiply(combined_voltage_values,combined_current_values)
            # mpp_index= get_mpp(power_values)
            # mpp_voltage = combined_voltage_values[mpp_index]
            # mpp_current = combined_current_values[mpp_index]
            
            # Save data for the current pixel in a text file
            save_data_to_file(pixel_number, combined_voltage_values, combined_current_values,username)
            print('change mux')
            # Turn off the current pixel after completing its measurements
            select_pixel(ser, pixel_number, turn_off=False)   
            plot_new(combined_voltage_values, combined_current_values, pixel_number, ax[row_index, col_index])
        fig.set_size_inches(a4_width_inches, a4_height_inches)
        pdf.savefig()
        plt.close()       
    return pdf_file_path

class DesignNewApp:
    def __init__(self, master=None):
        # build ui
        self.top_main = tk.Tk() if master is None else tk.Toplevel(master)
        self.top_main.configure(background="#9dceff", height=600, width=600)
        self.text_heading = tk.Text(self.top_main, name="text_heading")
        self.top_main.title("Solar Cell test")
        self.text_heading.configure(
            background="#9dceff",
            blockcursor=True,
            font="{Calibri} 24 {bold}",
            height=0,
            state="disabled",
            width=15,
            wrap="word")
        _text_ = 'SOLAR CELL TEST'
        self.text_heading.configure(state="normal")
        self.text_heading.insert("0.0", _text_)
        self.text_heading.configure(state="disabled")
        self.text_heading.place(anchor="nw", relx=0.26, rely=0.04, x=0, y=0)
        self.username = ttk.Label(self.top_main, name="username")
        self.username.configure(
            background="#9dceff",
            font="{Arial} 10 {bold}",
            text='USER NAME')
        self.username.place(anchor="nw", relx=0.04, rely=0.19, x=0, y=0)
        self.username_entry = ttk.Entry(self.top_main, name="username_entry")
        self.user_name = tk.StringVar()
        self.username_entry.configure(
            font="{Arial} 12 {}",
            justify="left",
            state="normal",
            textvariable=self.user_name)
        self.username_entry.place(anchor="nw", relx=0.19, rely=0.19, x=0, y=0)
        self.s_voltage = ttk.Label(self.top_main, name="s_voltage")
        self.s_voltage.configure(
            background="#9dceff",
            font="{Arial} 10 {}",
            text='START VOLTAGE')
        self.s_voltage.place(anchor="nw", relx=0.04, rely=0.45, x=0, y=0)
        self.start_v = ttk.Entry(self.top_main, name="start_v")
        self.start_voltage = tk.DoubleVar(value=-0.2)
        self.start_v.configure(
            font="{Arial} 10 {}",
            justify="center",
            textvariable=self.start_voltage)
        _text_ = '-0.2'
        self.start_v.delete("0", "end")
        self.start_v.insert("0", _text_)
        self.start_v.place(
            anchor="nw",
            relheight=0.04,
            relwidth=0.09,
            relx=0.23,
            rely=0.45,
            x=0,
            y=0)
        self.st_voltage = ttk.Label(self.top_main, name="st_voltage")
        self.st_voltage.configure(
            background="#9dceff",
            font="{Arial} 10 {}",
            text='STOP VOLTAGE')
        self.st_voltage.place(anchor="nw", relx=0.04, rely=0.55, x=0, y=0)
        self.stop_v = ttk.Entry(self.top_main, name="stop_v")
        self.stop_voltage = tk.DoubleVar(value=1.2)
        self.stop_v.configure(
            font="{Arial} 10 {}",
            justify="center",
            textvariable=self.stop_voltage)
        _text_ = '1.2'
        self.stop_v.delete("0", "end")
        self.stop_v.insert("0", _text_)
        self.stop_v.place(
            anchor="nw",
            relheight=0.04,
            relwidth=0.09,
            relx=0.23,
            rely=0.55,
            x=0,
            y=0)
        self.sw_value = ttk.Label(self.top_main, name="sw_value")
        self.sw_value.configure(
            background="#9dceff",
            font="{Arial} 10 {}",
            text='SWEEP STEP')
        self.sw_value.place(anchor="nw", relx=0.39, rely=0.45, x=0, y=0)
        self.sweep_value = ttk.Entry(self.top_main, name="sweep_value")
        self.sweep_voltage = tk.DoubleVar(value=0.2)
        self.sweep_value.configure(
            font="{Arial} 10 {}",
            justify="center",
            textvariable=self.sweep_voltage)
        _text_ = '0.2'
        self.sweep_value.delete("0", "end")
        self.sweep_value.insert("0", _text_)
        self.sweep_value.place(
            anchor="nw",
            relheight=0.04,
            relwidth=0.09,
            relx=0.57,
            rely=0.45,
            x=0,
            y=0)
        self.sweep_value.bind("<1>", self.ack, add="")
        self.Sweep_butt = ttk.Button(self.top_main, name="sweep_butt")
        self.Start_sweep = tk.StringVar(value='START SWEEP')
        self.Sweep_butt.configure(
            cursor="arrow",
            state="disabled",
            text='START SWEEP',
            textvariable=self.Start_sweep)
        self.Sweep_butt.place(anchor="nw", relx=0.39, rely=0.55, x=0, y=0)
        self.Sweep_butt.configure(command=self.start_sweeping)
        self.connect_main = ttk.Button(self.top_main, name="connect_main")
        self.connect_device = tk.StringVar(value='CONNECT KEITHLEY')
        self.connect_main.configure(
            default="normal",
            text='CONNECT KEITHLEY',
            textvariable=self.connect_device)
        self.connect_main.place(anchor="nw", relx=0.58, rely=0.19, x=0, y=0)
        self.connect_main.configure(command=self.connect_keithley)
        self.disconnect_main = ttk.Button(self.top_main, name="disconnect_main")
        self.disconnect_device = tk.StringVar(value='DISCONNECT ALL')
        self.disconnect_main.configure(
            state="disabled",
            text='DISCONNECT ALL',
            textvariable=self.disconnect_device)
        self.disconnect_main.place(anchor="nw", relx=0.58, rely=0.25, x=0, y=0)
        self.disconnect_main.configure(command=self.disconnect_keithley)  
        self.conn_mux = ttk.Button(self.top_main, name="conn_mux")
        self.connect_mux = tk.StringVar(value='CONNECT MUX')
        self.conn_mux.configure(
            default="normal",
            text='CONNECT MUX',
            textvariable=self.connect_mux)
        self.conn_mux.place(anchor="nw", relx=0.19, rely=0.26, x=0, y=0)
        self.conn_mux.configure(command=self.connect_multiplexer)
        self.separator1 = ttk.Separator(self.top_main, name="separator1")
        self.separator1.configure(orient="horizontal")
        self.separator1.place(
            bordermode="inside",
            height=5,
            relheight=0.0,
            relwidth=0.0,
            relx=0.0,
            rely=0.38,
            width=600,
            x=0,
            y=0)
        self.separator2 = ttk.Separator(self.top_main, name="separator2")
        self.separator2.configure(orient="horizontal")
        self.separator2.place(
            bordermode="inside",
            height=5,
            relheight=0.0,
            relwidth=0.0,
            relx=0.0,
            rely=0.65,
            width=600,
            x=0,
            y=0)
        text3 = tk.Text(self.top_main)
        text3.configure(
            background="#9dceff",
            blockcursor=True,
            borderwidth=0,
            font="{Arial} 10 {}",
            height=1,
            relief="flat",
            setgrid=False,
            state="normal",
            undo=False,
            width=15)
        _text_ = 'PIXEL Number'
        text3.insert("0.0", _text_)
        text3.place(anchor="nw", relx=0.1, rely=0.68, x=0, y=0)
        self.muxnum = tk.IntVar(value=0)
        __values = ['1', '2', '3', '4', '5', '6']
        optionmenu3 = tk.OptionMenu(
            self.top_main,
            self.muxnum,
            *__values,
            command=self.selectmux)
        optionmenu3.place(anchor="nw", relx=0.27, rely=0.68, x=0, y=0)
        self.button = tk.Button(self.top_main, name="button")
        self.on = tk.StringVar(value='ON')
        self.button.configure(
            activebackground="#ffffff",
            activeforeground="#ffffff",
            background="#008000",
            font="{Arial} 9 {bold}",
            text='ON',
            textvariable=self.on)
        self.button.place(anchor="nw", relx=0.22, rely=0.74, x=0, y=0)
        self.button.configure(command=self.muxon)
        self.buttoff1 = tk.Button(self.top_main, name="buttoff1")
        self.off = tk.StringVar(value='OFF')
        self.buttoff1.configure(
            activebackground="#ffffff",
            activeforeground="#ffffff",
            background="#ff0000",
            font="{Arial} 9 {bold}",
            text='OFF',
            textvariable=self.off)
        self.buttoff1.place(anchor="nw", relx=0.35, rely=0.74, x=0, y=0)
        self.buttoff1.configure(command=self.muxoff)
        self.maincontrol = ttk.Label(self.top_main, name="maincontrol")
        self.maincontrol.configure(
            background="#9dceff",
            font="{Arial} 14 {italic}",
            text='MAIN\n    CONTROL\n')
        self.maincontrol.place(anchor="nw", relx=0.74, rely=0.47, x=0, y=0)
        self.manualcontrol = ttk.Label(self.top_main, name="manualcontrol")
        self.manualcontrol.configure(
            background="#9dceff",
            font="{Arial} 14 {italic}",
            text='MANUAL\n     CONTROL\n')
        self.manualcontrol.place(anchor="nw", relx=0.74, rely=0.71, x=0, y=0)
        self.manual_sweep = ttk.Button(self.top_main, name="manual_sweep")
        self.manual_sweep.configure(
            cursor="arrow",
            state="disabled",
            text='START MANUAL SWEEP',
            textvariable=self.Start_sweep)
        self.manual_sweep.place(anchor="nw", relx=0.20, rely=0.83, x=0, y=0)
        self.manual_sweep.configure(command=self.start_manual_sweeping)
        self.port = tk.StringVar(value='COM')
        __values = ['COM5', 'COM3', 'COM4', 'COM31', 'COM7']
        self.comport = tk.OptionMenu(
            self.top_main,
            self.port,
            *__values,
            command=self.comval)
        self.comport.place(anchor="nw", relx=0.05, rely=0.26, x=0, y=0)

        # Main widget
        self.mainwindow = self.top_main

    def run(self):
        self.mainwindow.mainloop()

    def ack(self, event=None):
        pass
    
    
    def unlock_all(self):
        if connected:
            self.Sweep_butt.configure(state="normal")
            self.manual_sweep.configure(state="normal")

    def start_sweeping(self):
        current_datetime = datetime.now()
        current_date = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        output_file_path = mux(keithley, ser, 6, self.start_voltage.get(),self.stop_voltage.get(), self.sweep_voltage.get(),self.user_name.get())
        add_page_heading(output_file_path, "My Plots", self.user_name.get(), "Plots of pixels", current_date)

    def connect_keithley(self):
        connect_keithley()
        if connected:
            self.connect_main.configure(state="disabled")
            self.disconnect_main.configure(state="normal")
        run_start_up_commands(keithley)

    def connect_multiplexer(self):
        k=self.port.get()
        serialopen(k)
        if ser.isOpen():
            self.unlock_all()
    
    def disconnect_keithley(self):
        try:
         keithley.close()
         connected=False
        except Exception as e:
          connected=True
        if not connected:
            self.connect_main.configure(state="normal")
            self.disconnect_main.configure(state="disabled")
            self.Sweep_butt.configure(state="disabled")
            self.manual_sweep.configure(state="disabled")
            ser.close()
        
    def selectmux(self, option):
        pass

    def muxon(self):
        pass

    def muxoff(self):
        pass

    def start_manual_sweeping(self):
        pass

    def comval(self, option):
        pass


if __name__ == "__main__":
    app = DesignNewApp()
    app.run()
    ser.close()
    keithley.close()









