import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
import numpy as np
from io import BytesIO
from PyPDF2 import PdfReader, PdfWriter
from datetime import datetime

def generate_plots():
    # Generate some random data
    x = np.linspace(0, 10, 100)
    y1 = np.sin(x)
    y2 = np.cos(x)
    y3 = np.sin(2 * x)
    y4 = np.cos(2 * x)

    # Create plots
    plt.figure(figsize=(8, 6))

    plt.subplot(2, 2, 1)
    plt.plot(x, y1)
    plt.title('Plot 1')

    plt.subplot(2, 2, 2)
    plt.plot(x, y2)
    plt.title('Plot 2')

    plt.subplot(2, 2, 3)
    plt.plot(x, y3)
    plt.title('Plot 3')

    plt.subplot(2, 2, 4)
    plt.plot(x, y4)
    plt.title('Plot 4')

    # Save the plots to a PDF file
    pdf_file_path = "plots.pdf"
    with PdfPages(pdf_file_path) as pdf:
     for i in range(1, plt.gcf().number + 1):
            plt.figure(i)
            pdf.savefig()  # Save the current figure to the PDF
            plt.close()

    return pdf_file_path


def add_page_heading(pdf_path, title, author, other_details,current_date):
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)

    # Set font and size for the heading
    can.setFont("Helvetica", 14)

    # Add heading details
    can.drawString(100, 750, f"Title: {title}")
    can.drawString(100, 730, f"Author: {author}")
    can.drawString(100, 710, f"Other Details: {other_details}")
    can.drawString(100, 690, f"Date: {current_date}")

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


if __name__ == "__main__":
    output_file_path = generate_plots()
    current_datetime = datetime.now()
    current_date = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    add_page_heading(output_file_path, "My Plots", "Abhishek O", "Plots of pixels", current_date)
    add_page_heading(output_file_path, "My Plots", "John Doe", "Generated on January 30, 2024",current_date)
    print("PDF with plots and heading generated successfully at final_plots.pdf")
