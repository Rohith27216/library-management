import tkinter as tk
import books

def open_dashboard():
    dash = tk.Tk()
    dash.title("Library Dashboard")
    dash.geometry("400x250")

    tk.Label(dash, text="Library Management Dashboard",
             font=("Arial", 16)).pack(pady=20)

    tk.Button(dash, text="Manage Books", width=20,
              command=books.open_books).pack(pady=10)

    dash.mainloop()
