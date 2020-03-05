from tkinter import *
import _thread as thread
import socket
from tkinter import messagebox
import sqlite3
from datetime import date , datetime
import Cipher


db = sqlite3.connect("Client.db" , check_same_thread=False)

cr = db.cursor()

#cr.execute('''CREATE TABLE send_message
 #          (Date text ,time text , send text);''')


#cr.execute('''CREATE TABLE receive_message
 #              (date text ,time text, receive text);''')



s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)


HOST = 'localhost'
PORT = 8011

s.connect((HOST ,PORT))

def ClickAction():
    EntryText = Entry_Box.get("0.0" , END)
    ChatWindow.config(state = NORMAL)

    Entry_Box.delete("0.0" , END)
    ChatWindow.insert(INSERT , "You :  "+EntryText)
    message = Cipher.encrypt(EntryText, key=4)
    message = message.encode("utf-8")

    s.send(message)
    today = date.today()
    d = today.strftime("%B %d, %Y")
    t1 = datetime.now()
    t2 = t1.strftime("%H:%M:%S")
    cr.execute('''INSERT INTO send_message(Date ,time, send) VALUES(?,?,?)''', (d, t2, message))
    db.commit()
    ChatWindow.config(state = DISABLED)


def delete_chat():
    q = messagebox.askquestion("Warning", "Really want to chat delete")
    print(q)
    if q == "yes":
        ChatWindow.config(state=NORMAL)
        ChatWindow.delete("0.0", END)
        ChatWindow.config(state=DISABLED)





root = Tk()
root.title("Client Chat Room")
root.geometry("400x550")
root.resizable(width = False , height = False)


ChatWindow = Text(root , bd =0 , bg = "light blue" ,fg = "blue", height = "8" , width = "50" , font = "Arial"  , state = DISABLED)

ChatWindow.place(x=6 , y=6 , height = 386 , width = 370)




send_button = Button(root , font = 30 , text = "Send" , width = "12" , height = 5 , bd = 0 , bg = "yellow" , command = ClickAction)
send_button.place(x=6 , y = 401 , height = 90)

Entry_Box = Text(root , bd = 0 , bg = "cyan" , width = 29 , height = 5 , font = "Arial")
Entry_Box.place(x=128 , y = 401 , height =90 , width = 265)

delete_chat = Button(root , text = "Delete Conversation" , height = 3 , font = "Arial" , bg ="red" , command = delete_chat)
delete_chat.place(x = 128 , y = 500)


def receive():


    while 1:
        try:

            data = s.recv(1024)

            message1 = data.decode("utf-8")
            message = Cipher.decrypt(message1, key=4)


            ChatWindow.config(state = NORMAL)

            ChatWindow.insert(INSERT, "Server : " + message)
            ChatWindow.config(state =DISABLED )

            today = date.today()
            d = today.strftime("%B %d, %Y")
            t1 = datetime.now()
            t2 = t1.strftime("%H:%M:%S")

            cr.execute('''INSERT INTO receive_message (date ,time, receive) VALUES(?,?,?)''', (d, t2, message1))
            db.commit()


        except ConnectionResetError:
            t = messagebox.showinfo("MSG" , "SERVER OFFLINE")
            if t == "ok":
                root.destroy()


thread.start_new_thread(receive , ())


root.config(bg= "green")
root.mainloop()