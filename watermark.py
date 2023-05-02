#!/usr/bin/env python3
# File name          : watermark.py
# Author             : IllmaticJV
# Date created       : 02 May 2023

import sys
import os
import PyPDF2
import math
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.colors import red

def draw_string(ca, watermark_string):
    # Helper function to draw the watermark text on a canvas
    width = ca._pagesize[0]
    height = ca._pagesize[1]
    ca.setFont('Helvetica-Bold', 72)
    ca.setFillColorRGB(0.2, 0.2, 0.2, alpha=0.35)
    text_width = ca.stringWidth(watermark_string, 'Helvetica-Bold', 72)
    text_height = 72
    center_x = width/2
    center_y = height/2
    ca.translate(center_x, center_y)
    ca.rotate(45)
    ca.translate(-text_width/2, -text_height/2)
    ca.drawString(0, 0, watermark_string)
    return ca

def create_watermark_files(watermark_string):
    # Function to create portrait and landscape watermarks with the specified text
    ca_portrait = Canvas('tmp-portrait.pdf', pagesize=A4)
    ca_landscape = Canvas('tmp-landscape.pdf', pagesize=landscape(A4))
    draw_string(ca_portrait, watermark_string).save()
    draw_string(ca_landscape, watermark_string).save()

def watermark_file(watermark_string, input_file):
    # Function to add watermarks to the specified input PDF file
    source_pdf = PyPDF2.PdfReader(open(input_file, 'rb'))
    landscape_file = open('tmp-landscape.pdf', 'rb')
    watermark_landscape = PyPDF2.PdfReader(landscape_file)
    portrait_file = open('tmp-portrait.pdf', 'rb')
    watermark_portrait = PyPDF2.PdfReader(portrait_file)
    output = PyPDF2.PdfWriter()

    for page in source_pdf.pages:
        # Check rotation of page and add corresponding watermark
        if page.mediabox.width < page.mediabox.height:
            page.merge_page(watermark_portrait.pages[0])
        else:
            page.merge_page(watermark_landscape.pages[0])
        output.add_page(page)
    # Write output PDF file with watermarks
    file_name = input_file.split('.pdf')[0] + '-watermarked.pdf'
    with open(file_name, 'wb') as file:
        output.write(file)
        print(f"Watermarked file written to: \"{file_name}\"")
    # Close files and remove temporary watermark files
    landscape_file.close()
    portrait_file.close()
    os.remove('tmp-portrait.pdf')
    os.remove('tmp-landscape.pdf')


def main():
    # Main function to call other functions with command-line arguments
    watermark_string = sys.argv[1]
    input_file = sys.argv[2]
    create_watermark_files(watermark_string)
    watermark_file(watermark_string, input_file)

if __name__ == "__main__":
    # Execute main function if script is run directly
    main()
