from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk
import cv2
import datetime
#Make this Streamable: https://stackoverflow.com/questions/59587166/send-webcam-stream-from-server-in-python-using-sockets#

# Create an instance of TKinter Window or frame
win = Tk()
win.title('Cam&Chat')
win.iconbitmap(r'logo.ico')




# Set the size of the window
win.geometry("645x485")
win.eval('tk::PlaceWindow . center')

# Create a Label to capture the Video frames
label = Label(win)
label.grid(row=0, column=0) 
cap= cv2.VideoCapture(0)
#Button will release the camera and destroy the current window
destroy_button = Button(win, text="Close Connection", command=lambda:[cap.release(),win.destroy()])
destroy_button.place(x=436, y=455)
def open_new_window():
    global newWindow
    newWindow = Toplevel(win, bg="#CBE8EB")
    input_user = StringVar()
    input_field = Entry(newWindow, text=input_user)
    #Event listener when ENTER is pressed on the user keyboard
    def Enter_pressed(event):
        input_get = input_field.get()
        
        dt = datetime.datetime.now()
        hour = '{:02d}'.format(dt.hour)
        minute = '{:02d}'.format(dt.minute)
        second = '{:02d}'.format(dt.second)
        hms = '{}:{}:{}'.format(hour, minute, second)
        #print(input_get)
        label = Label(newWindow, text=[hms,input_get], borderwidth=2, relief="solid", anchor="e", wraplength=200, justify=LEFT, state="normal")
        #label.configure(state="disabled")
        input_user.set('')
        label.pack(side=TOP, anchor=W)
        return "break"
    #places the box for typing in at the bottom of the screen and stretches it to fit the window
    input_field.place(x=0,y=465, relwidth=1.0)
    
    #makes the ENTER button on the keyboard into a method of adding text to the widget
    input_field.bind("<Return>", Enter_pressed)
    newWindow.title("Chat")
    newWindow.geometry("200x485")
    newWindow.resizable(False, False)
    newWindow.attributes('-fullscreen', False)
    #Label(newWindow,text="Chat Window").grid(row=0,column=0)
    
chat_button = Button(win, text="Open Chat", command=open_new_window)
chat_button.place(x=550,y=455)


# Define function to show frame
def show_frames():
    # Get the latest frame and convert into Image
    cv2image= cv2.cvtColor(cap.read()[1],cv2.COLOR_BGR2RGB)
    img = Image.fromarray(cv2image)
    # Convert image to PhotoImage
    imgtk = ImageTk.PhotoImage(image = img)
    label.imgtk = imgtk
    label.configure(image=imgtk)
    # Repeat after an interval to capture continuously
    label.after(20, show_frames)
def move_together(event):
    try:
        if newWindow != None:
            x = win.winfo_x()+645
            y = win.winfo_y()
            newWindow.geometry(f"+{x}+{y}")
    except NameError:
        pass
win.bind("<Configure>", move_together)

show_frames()

win.mainloop()
