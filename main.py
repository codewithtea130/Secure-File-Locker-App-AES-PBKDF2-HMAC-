# success instead of SUCCESS



import os
import time
import hmac
import hashlib
import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinterdnd2 import TkinterDnD, DND_FILES
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad 

SALT_SIZE = 16
KEY_SIZE = 32
ITERATIONS = 100000
BLOCK_SIZE = AES.block_size
HMAC_KEY_SIZE = 32
MAX_ATTEMPTS = 5
LOCKOUT_TIME = 30

failed_attempts = {}
MASTER_FILE = "master.lock" 


BG_MAIN = "#121212"
BG_CARD = "#1b1b1b"
BG_DROP = "#1f1f1f"
ACCENT = "#4cc9f0"
TEXT_PRIMARY = "#ffffff"
TEXT_SECONDARY = "#aaaaaa"
SUCCESS = "#2ecc71"
ERROR = "#e74c3c"

FONT_TITLE = ("Segoe UI", 22, "bold")
FONT_NORMAL = ("Segoe UI", 11)
FONT_SMALL = ("Segoe UI", 9) 

def is_locked(filepath):
    try:
        with open(filepath,"rb") as f:
            return f.read(6) == b"LOCKED"
    except:
        return False 

def setup_master():
    root.withdraw()
    if not os.path.exists(MASTER_FILE):
        pw = simpledialog.askstring("setup Master Password","Create Master Password:",show="*")
        if not pw:
            exit()
        with open(MASTER_FILE,"wb") as f:
            f.write(hashlib.sha256(pw.encode()).digest())
        messagebox.showinfo("Success","Master Password set successfully.")
    else:
        pw = simpledialog.askstring("Master Login","Enter Master Password:",show="*")
        if not pw:
            exit()
        with open(MASTER_FILE,"rb") as f:
            stored = f.read()
        if hashlib.sha256(pw.encode()).digest() != stored:
            messagebox.showerror("Access Denied","Wrong Master Password")
            exit()
    root.deiconify() 


def encrypt_file(filepath,password):
    with open(filepath,"rb") as f:
        data = f.read()
    salt = get_random_bytes(SALT_SIZE)
    key = PBKDF2(password,salt,dkLen=KEY_SIZE,count=ITERATIONS)
    hmac_key = PBKDF2(password,salt,dkLen=HMAC_KEY_SIZE,count=ITERATIONS)
    cipher = AES.new(key,AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(data,BLOCK_SIZE))
    tag = hmac.new(hmac_key,ciphertext,hashlib.sha256).digest()
    with open(filepath, "wb") as f:
        f.write(b"LOCKED")
        f.write(salt)
        f.write(cipher.iv)
        f.write(tag)
        f.write(ciphertext) 


def decrypt_file(filepath,password):
    if filepath in failed_attempts:
        if failed_attempts[filepath]["count"] >= MAX_ATTEMPTS:
            if time.time() - failed_attempts[filepath]["time"] < LOCKOUT_TIME:
                return False, "Too many failed attempts. wait 30 seconds."
    try:
        with open(filepath,"rb") as f:
            if f.read(6) != b"LOCKED":
                return False,"File is not locked."
            salt = f.read(SALT_SIZE)
            iv = f.read(16)
            tag = f.read(32)
            ciphertext = f.read()
        key = PBKDF2(password,salt,dkLen=KEY_SIZE,count=ITERATIONS)
        hmac_key = PBKDF2(password,salt,dkLen=HMAC_KEY_SIZE,count=ITERATIONS)
        calc_tag = hmac.new(hmac_key,ciphertext,hashlib.sha256).digest()
        if not hmac.compare_digest(tag,calc_tag):
            raise ValueError
        cipher = AES.new(key,AES.MODE_CBC,iv)
        decrypted = unpad(cipher.decrypt(ciphertext),BLOCK_SIZE)
        with open(filepath,"wb") as f:
            f.write(decrypted)  
        if filepath in failed_attempts:
            del failed_attempts[filepath]
        return True, "File unlocked successfully."
    except:
        if filepath not in failed_attempts:
            failed_attempts[filepath] = {"count":1,"time":time.time()}
        else:
            failed_attempts[filepath]["count"] += 1
            failed_attempts[filepath]["time"] = time.time()
        return False, "Incorrect password or corrupted file."  
            


def lock_action(filepath):
    if is_locked(filepath):
        status_label.config(text="File is already locked.",fg=ERROR)
        messagebox.showwarning("Already Locked","This file is already locked.")
        return
    password = simpledialog.askstring("Set Password","Enter Password:",show="*")
    if not password:
        return
    encrypt_file(filepath,password)
    status_label.config(text="File locked successfully.",fg=SUCCESS)
    messagebox.showinfo("Success","File locked successfully.") 


def unlock_action(filepath):
    if not is_locked(filepath):
        status_label.config(text="File is alrady unlocked.",fg=ERROR)
        messagebox.showwarning("Already Unlocked","This file is not locked.")
        return
    password = simpledialog.askstring("Unlock File","Enter Password:",show="*")
    if not password:
        return
    success, msg = decrypt_file(filepath,password)
    if success:
        status_label.config(text=msg,fg=SUCCESS)
        messagebox.showinfo("Success",msg)
    else:
        status_label.config(text=msg,fg=ERROR)
        messagebox.showerror("Error",msg) 

drop_queue = []

def process_next_file():
    if not drop_queue:
        return
    file = drop_queue.pop(0)
    if not os.path.isfile(file):
        process_next_file()
        return
    
    action_window = tk.Toplevel(root)
    action_window.title("Choose Action")
    action_window.configure(bg=BG_CARD)
    action_window.geometry("350x150")
    action_window.resizable(False,False)
    action_window.grab_set() 

    tk.Label(
        action_window,
        text= os.path.basename(file),
        font=FONT_NORMAL,
        bg=BG_CARD,
        fg=TEXT_PRIMARY
    ).pack(pady=15)

    btn_frame = tk.Frame(action_window,bg=BG_CARD)
    btn_frame.pack(pady=10)

    def close_window_and_continue(func):
        func(file)
        action_window.destroy()
        root.after(100,process_next_file) 

    tk.Button(
        btn_frame,
        text="Lock",
        bg=ACCENT,
        fg="black",
        width=12,
        relief="flat",
        command=lambda: close_window_and_continue(lock_action)
    ).pack(side="left",padx=10)

    tk.Button(
        btn_frame,
        text="Unlock",
        bg="#333333",
        fg="white",
        width=12,
        relief="flat",
        command=lambda: close_window_and_continue(unlock_action)
    ).pack(side="right",padx=10) 

def handle_drop(event):
    global drop_queue
    drop_queue.extend(root.tk.splitlist(event.data))
    if len(drop_queue) == len(root.tk.splitlist(event.data)):
        process_next_file() 





root = TkinterDnD.Tk()
root.title("Advanced Image Vault")
root.geometry("560x360")
root.resizable(False,False)
root.configure(bg=BG_MAIN)

container = tk.Frame(root,bg=BG_MAIN)
container.pack(expand=True) 


title = tk.Label(
    container,
    text="Secure Image Vault",
    font=FONT_TITLE,
    bg=BG_MAIN,
    fg=TEXT_PRIMARY
)
title.pack(pady=(30,10)) 

subtitle = tk.Label(
    container,
    text="Drag & drop files below to encrypt or decrypt securely",
    font=FONT_SMALL,
    bg=BG_MAIN,
    fg=TEXT_SECONDARY
)
subtitle.pack() 

drop_area = tk.Label(
    container,
    text="Drag & Drop Files Here",
    width=45,
    height=6,
    bg=BG_DROP,
    fg=TEXT_PRIMARY,
    relief="ridge",
    bd=2
)
drop_area.pack(pady=30) 

drop_area.drop_target_register(DND_FILES)
drop_area.dnd_bind("<<Drop>>",handle_drop)

status_label = tk.Label(
    container,
    text="Ready",
    font=FONT_SMALL,
    bg=BG_MAIN,
    fg=TEXT_SECONDARY
)
status_label.pack(pady=10)

setup_master()
root.mainloop() 
