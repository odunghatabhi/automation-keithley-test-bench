from requirements import *


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


def connect_keithley():
    rm = pyvisa.ResourceManager()
    print(rm.list_resources())
    global keithley
    global connected
    connected = False
    try:
        keithley = rm.open_resource('ASRL31::INSTR')
        keithley.set_visa_attribute(pyvisa.constants.VI_ATTR_ASRL_BAUD, 9600)
        keithley.timeout = None
        print(keithley.query('*IDN?'))
        connected = True
    except Exception as e:
        connected = False


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
        send_command(keithley, ':SENS:FUNC "CURR"')

    elif sensor_type == 'voltage' or sensor_type == 'volt' or sensor_type == 'v':
        send_command(keithley, ':SENS:FUNC "VOLT"')

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
        send_command(keithley, ':SOUR:FUNC CURRENT')
    elif source_type == 'voltage' or source_type == 'volt' or source_type == 'v':
        send_command(keithley, ':SOUR:FUNC VOLT')
    else:
        print("Unknown source setting!")


# Function to send commands to Keithley device
def send_command(keithley, command):
    keithley.write(command)





def sweep(keithley, start, stop, step, direction):
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
    all_time_values = []

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
    if (direction == 0):
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
    time_data = []
    keithley.write(':INIT')
    time.sleep(1)
    print('sweep done')
    response = keithley.query(':READ?')
    data = [float(val) for val in response.split(',')]

    vvalues = data[0::3]
    cvalues = data[1::3]
    tvalues = data[2::3]
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
        send_command(keithley, com)
        time.sleep(.01)


def constantvoltagemeasureself(keithley, k):
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
    send_command(keithley, ':SOUR:FUNC VOLT')
    send_command(keithley, ':SENS:FUNC "CURR"')
    send_command(keithley, ':SENSE:CURR:PROT 0.2')
    send_command(keithley, ':SOUR:VOLT:MODE FIX')
    send_command(keithley, ':SOUR:VOLT:LEV %f' % k)
    send_command(keithley, ':FORM:ELEM CURR,TIME')
    send_command(keithley, ':OUTP ON')
    send_command(keithley, ':INIT')
    send_command(keithley, ':TRIG:COUN 5')
    send_command(keithley, ':SOUR:DEL 0.1')
    response = keithley.query(':READ?')
    time.sleep(1)
    send_command(keithley, ':OUTP OFF')
    print(response)
    data = [float(val) for val in response.split(',')]
    cvalues = data[0::2]
    tvalues = data[1::2]
    plt.plot(tvalues, cvalues)
    plt.xlabel("TIME(s)")
    plt.ylabel("CURRENT(A)")
    plt.pyplot.show()


def constantcurrentmeasureself(keithley, k):
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
    send_command(keithley, ':SOUR:FUNC CURR')
    send_command(keithley, ':SENS:FUNC "VOLT"')
    send_command(keithley, ':SENSE:VOLT:PROT 10')
    send_command(keithley, ':SOUR:CURR:MODE FIX')
    send_command(keithley, ':SOUR:CURR:%f' % k)
    send_command(keithley, ':FORM:ELEM VOLT,TIME')

    send_command(keithley, ':SYST:RSEN ON')
    send_command(keithley, ':OUTP ON')
    send_command(keithley, ':INIT')
    send_command(keithley, ':TRIG:COUN 10')
    send_command(keithley, ':SOUR:DEL 1')
    response = keithley.query(':READ?')
    time.sleep(1)

    send_command(keithley, ':SYST:RSEN OFF')
    send_command(keithley, ':OUTP OFF')
    print(response)
    data = [float(val) for val in response.split(',')]
    vvalues = data[0::2]
    tvalues = data[1::2]
    plt.plot(tvalues, vvalues)
    plt.xlabel("TIME(s)")
    plt.ylabel("VOLT(v)")
    plt.pyplot.show()