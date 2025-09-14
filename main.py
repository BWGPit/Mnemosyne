import tkinter
from tkinter import messagebox
import time
from PIL import ImageTk, Image
import subprocess
import os
import random
from gestoreP import neopass as password

win = tkinter.Tk()
win.iconbitmap("img/icon.ico")
win.geometry("1920x1080")#+1920+40
win.title("Mnemosyne")

PADX = 40

imgfile = ImageTk.PhotoImage(Image.open(random.choice([x for x in os.listdir() if x.endswith(".png")])).resize((1920, 1080)))
img = tkinter.Label(master=win, image=imgfile)
img.place(x=0, y=0)

# TEMPVS

timers = []

def timer():
    if entry_hours.get().isnumeric():
        hours = int(entry_hours.get())
    else:
        hours = 0
    if entry_minutes.get().isnumeric():
        minutes = int(entry_minutes.get())
    else:
        minutes = 0
    if entry_seconds.get().isnumeric():
        seconds = int(entry_seconds.get())
    else:
        seconds = 0
    title = entry_title.get()
    current = time.time()
    for x in [entry_hours, entry_minutes, entry_seconds, entry_title]:
        x.delete(0, tkinter.END)
    end = current + hours*3600 + minutes*60 + seconds
    timers.append({"name": title, "end": end})


orario = time.strftime("%H:%M:%S")
ora = tkinter.Label(master=win, text=orario, bg="grey", fg="black", font=("Consolas", 40))
ora.pack(anchor="nw", padx=PADX, pady=50)

timerbar = tkinter.Canvas(master=win)
timerbar.pack(anchor="nw", padx=PADX, pady=20, ipady=10)

space = tkinter.Label(master=timerbar, text="Timer", font=("Consolas", 14))
space.grid(row=0, column=0, pady=2)
addtimer = tkinter.Button(master=timerbar, text="[+] aggiungi", command=timer)
addtimer.grid(row=1, column=0, ipadx=5, padx=2)
entry_hours = tkinter.Entry(master=timerbar)
entry_hours.grid(row=1, column=1)
entry_hours_text = tkinter.Label(master=timerbar, text="h")
entry_hours_text.grid(row=1, column=2)
entry_minutes = tkinter.Entry(master=timerbar)
entry_minutes.grid(row=1, column=3)
entry_minutes_text = tkinter.Label(master=timerbar, text="m")
entry_minutes_text.grid(row=1, column=4)
entry_seconds = tkinter.Entry(master=timerbar)
entry_seconds.grid(row=1, column=5)
entry_seconds_text = tkinter.Label(master=timerbar, text="s")
entry_seconds_text.grid(row=1, column=6)
for k in [entry_hours, entry_minutes, entry_seconds]:
    k["width"] = 5
entry_title_text = tkinter.Label(master=timerbar, text="Nome")
entry_title_text.grid(row=1, column=7, padx=4)
entry_title = tkinter.Entry(master=timerbar, width=20)
entry_title.grid(row=1, column=8, padx=2)

active_timers = tkinter.Label(master=timerbar, text="Aggiungi un timer", font=("Consolas", 11), justify="center")
active_timers.grid(row=2, column=0, padx=2, pady=4, columnspan=9)

# UTILIA

utilia = tkinter.Canvas(master=win)
utilia.pack(anchor="nw", padx=PADX, pady=10, ipady=0)

# PASSWORD

win3bgfile = ImageTk.PhotoImage(Image.open("img/pwdbg.png").resize((600, 600)))

def openpwd():
    global win3bgfile
    win3 = tkinter.Toplevel(master=win)
    win3.title("Gestore password")
    win3.geometry(f"600x600+{str(int((1920/4)))}+200") #1920 + 
    win3.resizable(0, 0)

    win3bg = tkinter.Label(master=win3, image=win3bgfile)
    win3bg.place(x=0, y=0)
    
    add = tkinter.Canvas(master=win3, bg="black")
    add.pack(padx=PADX, pady=10)
    INBETWEEN_X = 2
    INBETWEEN_Y = 4
    add_site_text = tkinter.Label(master=add, text="Nome del sito", bg="black", fg="yellow")
    add_site_text.grid(row=0, column=0, padx=INBETWEEN_X, pady=INBETWEEN_Y)
    add_site_name = tkinter.Entry(master=add, bg="black", fg="yellow")
    add_site_name.grid(row=0, column=1, padx=INBETWEEN_X, pady=INBETWEEN_Y)
    add_pwd_e = tkinter.Entry(master=add, bg="black", fg="yellow")
    add_pwd_text = tkinter.Label(master=add, text="Password", bg="black", fg="yellow")
    add_pwd_text.grid(row=0, column=2, padx=INBETWEEN_X, pady=INBETWEEN_Y)
    add_pwd_e.grid(row=0, column=3, padx=INBETWEEN_X, pady=INBETWEEN_Y)

    pwd_list = tkinter.Listbox(master=win3, width=50, bg="black", fg="yellow", font=("Consolas", 14))
    pwd_list.pack(padx=PADX, pady=10)
    
    def fill():
        for i in password.do(password.lookup, "", "x"):
            pwd_list.insert(tkinter.END, i.replace(" --> ", " | "))
    def listrefresh():
        pwd_list.delete(0, tkinter.END)
        fill()
    fill()

    def apwd():
        password.do(password.set_password, add_site_name.get(), add_pwd_e.get())
        add_site_name.delete(0, tkinter.END)
        add_pwd_e.delete(0, tkinter.END)
        listrefresh()

    def rpwd():
        confirmed = messagebox.askyesno(title="Gestore password - conferma", message="L'operazione rimuoverà la password selezionata. Confermare?")
        if confirmed:
            got = pwd_list.get(pwd_list.curselection()).split(" | ")
            if got != None:
                s = got[0]
                p = got[1]
                password.do(password.remove_password, s, p)
            listrefresh()

    add_pwd_b = tkinter.Button(master=add, text="Aggiungi password", command=apwd, bg="black", fg="yellow")
    add_pwd_b.grid(row=0, column=4, padx=INBETWEEN_X, pady=INBETWEEN_Y)
    remove = tkinter.Button(master=win3, text="Rimuovi password", command=rpwd, bg="black", fg="yellow")
    remove.pack(padx=PADX, pady=10)

passbutton = tkinter.Button(master=utilia, text="Gestisci password", command=openpwd)
passbutton.grid(row=0, column=0, padx=0, pady=0, ipadx=2, ipady=10)

# COMMENTARII

cliplabel = tkinter.Label(master=win, text="Appunti", font=("Consolas", 20))
cliplabel.pack(anchor="nw", padx=PADX, pady=0)
clipboard = tkinter.Text(master=win, width=50, height=10)
clipboard.pack(anchor="nw", padx=PADX, pady=0)

spazio = tkinter.Frame(master=win)
spazio.pack(anchor="nw", padx=PADX, pady=20)

def add2todo():
    with open("todo.txt", "a") as f:
        f.write(clipboard2.get("1.0", tkinter.END))
        clipboard2.delete("1.0", tkinter.END)

def opentodo():
    subprocess.Popen(["notepad.exe", "todo.txt"])

cliplabel2 = tkinter.Label(master=win, text="TODO", font=("Consolas", 20))
cliplabel2.pack(anchor="nw", padx=PADX, pady=0)
todotext = open("todo.txt", "r").read()
todolines = tkinter.Label(master=win, text=todotext, width=50, font=("Consolas", 11), justify="left")
todolines.pack(anchor="nw", padx=PADX, pady=0)
clipboard2 = tkinter.Text(master=win, width=50, height=5)
clipboard2.pack(anchor="nw", padx=PADX, pady=0)
todobutton = tkinter.Button(master=win, text="Aggiungi alla lista dei TODO", command=add2todo, width=57)
todobutton.pack(anchor="nw", padx=PADX, pady=0)
todobutton2 = tkinter.Button(master=win, text="Apri il file dei TODO", command=opentodo, width=57)
todobutton2.pack(anchor="nw", padx=PADX, pady=0)

# SCHERMO INTERO

def fullscreen_on(a):
    win.attributes("-fullscreen", True)

def fullscreen_off(b):
    win.attributes("-fullscreen", False)

win.bind("<F11>", fullscreen_on)
win.bind("<Escape>", fullscreen_off)


bg_count = 0
bg_list = []
for file in os.listdir():
    if file.endswith(".png"):
        bg_list.append(file)
random.shuffle(bg_list)

# MAINLOOP

def nextbg():
    global bg_count, bg_list
    if bg_count < len(bg_list)-1:
        bg_count += 1
    else:
        bg_count = 0

    new_bg = ImageTk.PhotoImage(Image.open(bg_list[bg_count]).resize((1920, 1080)))
    img.configure(image=new_bg)
    img.image = new_bg

def refresh():
    ora["text"] = time.strftime("%H:%M:%S")
    todolines["text"] = open("todo.txt", "r").read()
    timers2display = []
    for t in timers:
        if int(time.time()) == int(t["end"]):
            messagebox.showwarning(title="Timer scaduto!", message=f"""Timer {t["name"]} scaduto!""")
            timers.remove(t)
        else:
            end = t["end"]
            end_h = time.localtime(end)[3]
            end_m = time.localtime(end)[4]
            end_s = time.localtime(end)[5]
            timers2display.append(f"""{t["name"]} | {end_h}:{end_m}:{end_s}""")
        
    if len(timers2display) != 0:
        active_timers["text"] = "\n".join(timers2display)
    else:
        active_timers["text"] = "Aggiungi un timer"
    
    if time.strftime("%H:%M:%S").endswith("30:00") or time.strftime("%H:%M:%S").endswith("00:00"):
        nextbg()

    win.after(1000, refresh)

refresh()
win.mainloop()
