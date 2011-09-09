#!/usr/bin/env python

import sys
from pyPdf import PdfFileWriter, PdfFileReader
import sys

def pdfsew(output_filename,pdflist):
    output = PdfFileWriter()
    for pdf in pdflist:
        input1 = PdfFileReader(file(pdf, "rb"))
        for page in input1.pages:
            output.addPage(page)
    print output_filename
    outputStream = file(output_filename, "wb")
    output.write(outputStream)
    outputStream.close()

if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser("pdfsew <options> <pdflist>\n\tsews pdfs in <pdflist> together")
    parser.add_option("-n", "--name", dest="name",
                                        help="Filename (output.pdf)",
                                        action = "store", default = "output.pdf")
    (options, args) = parser.parse_args()
    pdfsew(options.name,args) 
#end
