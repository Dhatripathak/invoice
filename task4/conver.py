import pdfkit
import os

filename = os.path.join(os.path.dirname(__file__), 'f.csv')
print(filename)



html_file_path =  "C:/Users/Umesh Pathak/newproj/abc/task4/cv.html"


pdf_file_path = "C:/Users/Umesh Pathak/newproj/abc/task4/cv.pdf"



pdfkit.from_file("C:/Users/Umesh Pathak/newproj/abc/task4/cv.html", "C:/Users/Umesh Pathak/newproj/abc/task4/cv.pdf")
