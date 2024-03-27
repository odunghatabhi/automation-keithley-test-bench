from requirements import *

def save_data_to_file(pixel_number, voltage_values, current_values, username):
    # Define the file name based on the pixel number
    file_name = f'{username}_{pixel_number}_data.txt'
    data_table = list(zip(voltage_values, current_values))
    # Open the file in write mode and save the data
    with open(file_name, 'w') as file:
        file.write("Voltage\t \t Current\n")
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


# ax.scatter(mpp_voltage, mpp_current, color='red', label='MPP')


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
    with open("final_plots.pdf", "wb") as final_pdf:
        output_pdf.write(final_pdf)