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
import tkinter as tk
import tkinter.ttk as ttk