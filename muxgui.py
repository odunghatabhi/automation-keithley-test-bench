# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 10:13:57 2023

@author: WAVELABS-R90VZ50M
"""

import tkinter as tk
import tkinter.ttk as ttk
import serial
import time

#The various values that should be sent  to the multiplexer to turn it ON or OFF. 1 ,2 ,3...6 represents each switch in the MUX
m1_ON= "AA0100000000BB"
m1_OFF="AA0100000100BB"
m2_ON= "AA0101000000BB"
m2_OFF="AA0101000100BB"
m3_ON= "AA0102000000BB"
m3_OFF="AA0102000100BB"
m4_ON= "AA0103000000BB"
m4_OFF="AA0103000100BB"
m5_ON= "AA0104000000BB"
m5_OFF="AA0104000100BB"
m6_ON= "AA0105000000BB"
m6_OFF="AA0105000100BB"

def serialopen(port):
    global ser1
    try:
        ser1=serial.Serial(port=port,baudrate=115200,bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE)
    except:
        pass
def muxoperation(value):
    '''
    

    Parameters
    ----------
    value : Passes the M1_on, M1_off etc.. to decide which one to ON/OFF

    Returns
    -------
    None.

    '''
    f = bytes.fromhex(value)
    ser1.write(f)

def switcher_on(k):
    if(k==1):
        muxoperation(m1_ON)
    if(k==2):
        muxoperation(m2_ON)
    if(k==3):
        muxoperation(m3_ON)
    if(k==4):
        muxoperation(m4_ON)
    if(k==5):
        muxoperation(m5_ON)
    if(k==6):
        muxoperation(m6_ON)
        
def switcher_off(k):
    if(k==1):
        muxoperation(m1_OFF)
    if(k==2):
        muxoperation(m2_OFF)
    if(k==3):
        muxoperation(m3_OFF)
    if(k==4):
        muxoperation(m4_OFF)
    if(k==5):
        muxoperation(m5_OFF)
    if(k==6):
        muxoperation(m6_OFF)

class multiplexer:
    '''
      THIS CLASS IS GENERATED FROM THE pygubu SOFTWARE TO DESIGN THE GUI OF THE MULTIPLEXER INTERFACE
     '''
    def __init__(self, master=None):
        # build ui
        toplevel1 = tk.Tk() if master is None else tk.Toplevel(master)
        toplevel1.configure(background="#9dceff", height=200, width=200)
        toplevel1.geometry("480x320")
        toplevel1.resizable(True, True)
        toplevel1.title("Multiplexer Control")
        text3 = tk.Text(toplevel1)
        text3.configure(
            background="#9dceff",
            borderwidth=0,
            font="{Arial} 10 {bold}",
            height=1,
            relief="flat",
            setgrid="false",
            state="normal",
            undo="false",
            width=17)
        _text_ = 'MULTIPLEXER No:'
        text3.insert("0.0", _text_)
        text3.place(anchor="nw", relx=0.32, rely=0.62, x=0, y=0)
        self.port = tk.StringVar(value='COM5')
        __values = ['COM5', 'COM3', 'COM4', 'COM31', 'COM7', 'Other']
        self.comport = tk.OptionMenu(
            toplevel1, self.port, *__values, command=self.comval)
        self.comport.place(anchor="nw", relx=0.05, rely=0.16, x=0, y=0)
        self.comentry = tk.Entry(toplevel1)
        self.com = tk.StringVar()
        self.comentry.configure(
            state="normal",
            textvariable=self.com,
            width=13)
        self.comentry.place(anchor="nw", relx=0.22, rely=0.18, x=0, y=0)
        self.comentry.configure(validatecommand=self.comenter)
        self.comopen = tk.Button(toplevel1)
        self.open = tk.StringVar(value='OPEN COM')
        self.comopen.configure(state="normal",text='OPEN COM', textvariable=self.open)
        self.comopen.place(anchor="nw", relx=0.05, rely=0.29, x=0, y=0)
        self.comopen.configure(command=self.openport)
        self.status = tk.Message(toplevel1)
        self.comstatus = tk.StringVar(value='COM CLOSED')
        self.status.configure(
            background="#ff0000",
            borderwidth=0,
            font="{Arial} 10 {}",
            justify="center",
            pady=50,
            text='COM STATUS',
            textvariable=self.comstatus)
        self.status.place(
            anchor="nw",
            height=30,
            relheight=0.0,
            relwidth=0.0,
            relx=0.11,
            rely=0.44,
            width=100,
            x=0,
            y=0)
        self.close = tk.Button(toplevel1)
        self.closecom = tk.StringVar(value='CLOSE COM')
        self.close.configure(text='CLOSE COM', textvariable=self.closecom)
        self.close.place(anchor="nw", relx=0.23, rely=0.29, x=0, y=0)
        self.close.configure(command=self.serialclose)
        self.muxnum = tk.IntVar(value='1')
        __values = ['1', '2', '3', '4', '5', '6']
        optionmenu3 = tk.OptionMenu(
            toplevel1,
            self.muxnum,
            *__values,
            command=self.selectmux)
        optionmenu3.place(anchor="nw", relx=0.58, rely=0.6, x=0, y=0)
        self.button = tk.Button(toplevel1)
        self.on = tk.StringVar(value='ON')
        self.button.configure(
            state='disabled',
            activebackground="#ffffff",
            activeforeground="#ffffff",
            background="#008000",
            font="{Arial} 9 {bold}",
            text='ON',
            textvariable=self.on)
        self.button.place(anchor="nw", relx=0.53, rely=0.71, x=0, y=0)
        self.button.configure(command=self.muxon)
        self.buttoff1 = tk.Button(toplevel1)
        self.off = tk.StringVar(value='OFF')
        self.buttoff1.configure(
            state='disabled',
            activebackground="#ffffff",
            activeforeground="#ffffff",
            background="#ff0000",
            font="{Arial} 9 {bold}",
            text='OFF',
            textvariable=self.off)
        self.buttoff1.place(anchor="nw", relx=0.65, rely=0.71, x=0, y=0)
        self.buttoff1.configure(command=self.muxoff)
        self.header = tk.Label(toplevel1)
        self.header.configure(
            background="#9dceff",
            font="{Arial} 14 {bold}",
            text='MULTIPLEXER SWITCH CONTROL')
        self.header.place(anchor="center", relx=0.47, rely=0.07, x=0, y=0)
        self.instruction1 = tk.Text(toplevel1)
        self.instruction1.configure(
            background="#9dceff",
            borderwidth=0,
            font="{Arial} 10 {}",
            height=4,
            width=20)
        _text_ = 'Select other and enter COM port value manually when it  is not available in list.         Example: "com3"'
        self.instruction1.insert("0.0", _text_)
        self.instruction1.place(
            anchor="nw",
            relheight=0.21,
            relwidth=0.35,
            relx=0.42,
            rely=0.17,
            x=0,
            y=0)

        # Main widget
        self.mainwindow = toplevel1

         
    def run(self):
        self.mainwindow.mainloop()

    def selectmux(self, option):
        pass
            
    def muxon(self):
        k=self.muxnum.get()
        switcher_on(k)
        
    def muxoff(self):
        k=self.muxnum.get()
        switcher_off(k)   
        
    def comval(self, option):
       pass
   
    def comenter(self):  
         pass
     
    def openport(self):
        k=self.port.get()
        if(k=='Other'):
              portval=self.com.get()
              serialopen(portval)
              if ser1.isOpen():
               self.comopen.configure(state="disabled")
               self.comstatusprint('%s OPEN' %portval)
               self.button.configure(state='normal')
               self.buttoff1.configure(state='normal')
              else:
               self.comstatusprint('COM CLOSED')
        else:
          serialopen(k)
          if ser1.isOpen():
            self.comopen.configure(state="disabled")
            self.comstatusprint('%s OPEN' %k)
            self.button.configure(state='normal')
            self.buttoff1.configure(state='normal')
            
          else:
             self.comstatusprint('COM CLOSED')
            
    def serialclose(self):
        ser1.close()
        self.button.configure(state='disabled')
        self.buttoff1.configure(state='disabled')
        self.comopen.configure(state="normal",text='OPEN COM', textvariable=self.open)
        if not ser1.isOpen():
            self.comstatusprint('COM CLOSED')
        
    def comstatusprint(self,status):
             self.comstatus = tk.StringVar(value=status)
             self.status.place(
                 anchor="nw",
                 height=30,
                 relheight=0.0,
                 relwidth=0.0,
                 relx=0.11,
                 rely=0.44,
                 width=100,
                 x=0,
                 y=0)
             if(status=='COM CLOSED'):
                 self.status.configure(
                     background="#ff0000",
                     borderwidth=0,
                     font="{Arial} 10 {}",
                     justify="center",
                     pady=50,
                     text=status,
                     textvariable=self.comstatus)
             if('OPEN' in status):
                  self.status.configure(
                      background="#008000",
                      borderwidth=0,
                      font="{Arial} 10 {}",
                      justify="center",
                      pady=50,
                      text=status,
                      textvariable=self.comstatus)
    
if __name__ == "__main__":
    app = multiplexer()
    app.run()
    ser1.close()
