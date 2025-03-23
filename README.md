
# Certificates-Generator

Certificates Generator is the python project to generate certificates. It also serves as GUI based application.
This program automatically generates the certificates of the members by giving their details as input and saves them in both .jpg and .pdf file formats for better compatibility. 
It saves a lot of time by generating certificates of multiple people at the same time within a few seconds, which otherwise takes a lot of time if to be done manually.

## Project is created with:
-	Python programming language

- Python packages used:

    - Tkinter 
    
    - Pillow (for image processing)
    
    - OpenPyXL (for reading Excel)
    
    - SMTP & SSL (for email sending)  

## Setup
To run this project, follow the below instructions:

1.	Make sure all the related files such as sample template certificate_template.png and true type font file lora-bold.ttf are in the same folder.
2.	Make sure that the excel file sample certificates.xlsx, used for the details of the participants, exists on the system.
3.	Run the program.
4.	See that all required packages, modules, and libraries are installed and imported successfully.
5.	Successful generation of certificate for each member mentioned in the excel file is determined 
    when the respective row number along with name is printed on the output terminal.
6.	Finally, Done message will be displayed after successfull execution of program.
7.	All_Certificates folder will be created in the specified directory path. Subfolders named Images and PDFs are created, 
    which stores images and portable document formats(pdf) of all generated certificates respectively.

## Features
1.Certificates are generated and saved in both image(.png) and document(.pdf) formats.

