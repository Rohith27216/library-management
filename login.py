import tkinter as tk
from tkinter import messagebox
from db import get_connection
import dashboard

def login_user():
    username = user_entry.get()
    password = pass_entry.get()

    db = get_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s",
                   (username, password))
    result = cursor.fetchone()
    db.close()

    if result:
        root.destroy()
        dashboard.open_dashboard()
    else:
        messagebox.showerror("Login Failed", "Invalid Username or Password")

root = tk.Tk()
root.title("Login System")
root.geometry("300x200")

tk.Label(root, text="Username").pack()
user_entry = tk.Entry(root)
user_entry.pack()

tk.Label(root, text="Password").pack()
pass_entry = tk.Entry(root, show="*")
pass_entry.pack()

tk.Button(root, text="Login", command=login_user).pack(pady=10)

root.mainloop()
