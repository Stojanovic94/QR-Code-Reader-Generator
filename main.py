from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror, askyesno
from tkinter import filedialog as fd 
import qrcode
import cv2

def close_window():
    if askyesno(title='Close QR Code Reader & Generator App', 
                message='Are you sure you want to close the application?'):
        root.destroy()

def generate_qrcode():
    qrcode_data = str(data_entry.get())
    qrcode_name = str(filename_entry.get())
    if qrcode_name == '':
        showerror(title='Error', 
                  message='An error occurred\n'
                          'The following is the cause:\n'
                          '->Empty filename entry field\n'
                          'Make sure the filename entry field is filled when generating the QRCode')
    else:
        if askyesno(title='Confirmation', 
                    message=f'Do you want to create a QRCode with the provided information?'):
            try:
                qr = qrcode.QRCode(version=1, box_size=6, border=4)
                qr.add_data(qrcode_data)
                qr.make(fit=True)
                name = qrcode_name + '.png'
                qrcode_image = qr.make_image(fill_color='black', back_color='white')
                qrcode_image.save(name)
                global Image
                Image = PhotoImage(file=name)
                image_label1.config(image=Image)
                reset_button.config(state=NORMAL, command=reset)
            except Exception as e:
                showerror(title='Error', message='Please provide a valid filename')

def reset():
    if askyesno(title='Reset', message='Are you sure you want to reset?'):
        image_label1.config(image='')
        reset_button.config(state=DISABLED)

def open_dialog():
    name = fd.askopenfilename()
    file_entry.delete(0, END)
    file_entry.insert(0, name)

def detect_qrcode():
    image_file = file_entry.get()
    if image_file == '':
        showerror(title='Error', message='Please provide a QR Code image file to detect')
    else:
        try:
            qr_img = cv2.imread(image_file)    
            qr_detector = cv2.QRCodeDetector()  
            global qrcode_image
            qrcode_image = PhotoImage(file=image_file)
            image_label2.config(image=qrcode_image)
            data, pts, st_code = qr_detector.detectAndDecode(qr_img)
            detected_data_entry.delete(0, END)
            detected_data_entry.insert(0, data)
        except Exception as e:
            showerror(title='Error', 
                      message='An error occurred while detecting data from the provided file\n'
                              'The following could be the cause:\n->Wrong image file\n'
                              'Make sure the image file is a valid QRCode')

def copy_text():
    text = detected_data_entry.get()
    if text:
        root.clipboard_clear()
        root.clipboard_append(text)
        showinfo(title="Copied", message="Text copied to clipboard")
    else:
        showerror(title="Error", message="No text to copy")

root = Tk()
root.title('QR Code Reader & Generator App')
root.geometry('500x480+440+180')
root.resizable(height=FALSE, width=FALSE)
root.protocol('WM_DELETE_WINDOW', close_window)

# Stilovi za widgete, labele, entry i dugmad
label_style = ttk.Style()
label_style.configure('TLabel', foreground='#000000', font=('OCR A Extended', 11))

entry_style = ttk.Style()
entry_style.configure('TEntry', font=('arial', 15))

button_style = ttk.Style()
button_style.configure('TButton', foreground='#000000', font=('arial', 10))

tab_control = ttk.Notebook(root)
first_tab = ttk.Frame(tab_control)
second_tab = ttk.Frame(tab_control)
tab_control.add(first_tab, text='QR Code Generator')
tab_control.add(second_tab, text='QR Code Detector')
tab_control.pack(expand=1, fill="both")

first_canvas = Canvas(first_tab, width=500, height=480)
first_canvas.pack()

second_canvas = Canvas(second_tab, width=500, height=480)
second_canvas.pack()

# Widgeti za prvi tab (QR Code Generator)
image_label1 = Label(root)
first_canvas.create_window(250, 150, window=image_label1)

qrdata_label = ttk.Label(root, text='QRcode Data', style='TLabel')
data_entry = ttk.Entry(root, width=55, style='TEntry')
first_canvas.create_window(70, 330, window=qrdata_label)
first_canvas.create_window(300, 330, window=data_entry)

filename_label = ttk.Label(root, text='Filename', style='TLabel')
filename_entry = ttk.Entry(root, width=55, style='TEntry')
first_canvas.create_window(84, 360, window=filename_label)
first_canvas.create_window(300, 360, window=filename_entry)

reset_button = ttk.Button(root, text='Reset', style='TButton', state=DISABLED)
generate_button = ttk.Button(root, text='Generate QRCode', style='TButton', command=generate_qrcode)
first_canvas.create_window(300, 390, window=reset_button)
first_canvas.create_window(410, 390, window=generate_button)

# Widgeti za drugi tab (QR Code Detector)
image_label2 = Label(root)
second_canvas.create_window(250, 150, window=image_label2)

# Entry widget za detektovane podatke radi lakog kopiranja
detected_data_entry = ttk.Entry(root, width=40, style='TEntry')
second_canvas.create_window(200, 300, window=detected_data_entry)

# Dugme za kopiranje odmah pored Entry widgeta
copy_button = ttk.Button(root, text='Copy', style='TButton', command=copy_text)
second_canvas.create_window(400, 300, window=copy_button)

file_entry = ttk.Entry(root, width=60, style='TEntry')
browse_button = ttk.Button(root, text='Browse', style='TButton', command=open_dialog)
second_canvas.create_window(200, 350, window=file_entry)
second_canvas.create_window(430, 350, window=browse_button)

detect_button = ttk.Button(root, text='Detect QRCode', style='TButton', command=detect_qrcode)
second_canvas.create_window(65, 385, window=detect_button)

root.mainloop()
