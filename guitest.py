#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk



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

    def start_sweeping(self):
        pass

    def connect_keithley(self):
        pass

    def connect_multiplexer(self):
        pass

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

