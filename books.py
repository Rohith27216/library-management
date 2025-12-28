import tkinter as tk
from tkinter import ttk, messagebox
from db import get_connection

def open_books():
    win = tk.Tk()
    win.title("Book Management")
    win.geometry("700x500")

    # ---------------- SEARCH BAR ----------------
    tk.Label(win, text="Search Book").grid(row=0, column=0)
    search = tk.Entry(win)
    search.grid(row=0, column=1)

    def search_books():
        key = "%" + search.get() + "%"
        db = get_connection()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM books WHERE title LIKE %s OR author LIKE %s", (key, key))
        rows = cursor.fetchall()
        db.close()

        table.delete(*table.get_children())
        for r in rows:
            table.insert("", tk.END, values=r)

    tk.Button(win, text="Search", command=search_books).grid(row=0, column=2)

    # ---------------- INPUT FIELDS ----------------
    tk.Label(win, text="Title").grid(row=1, column=0)
    title = tk.Entry(win)
    title.grid(row=1, column=1)

    tk.Label(win, text="Author").grid(row=2, column=0)
    author = tk.Entry(win)
    author.grid(row=2, column=1)

    tk.Label(win, text="Year").grid(row=3, column=0)
    year = tk.Entry(win)
    year.grid(row=3, column=1)

    # ---------------- TABLE ----------------
    table = ttk.Treeview(win, columns=("ID", "Title", "Author", "Year"), show="headings")
    for col in ("ID", "Title", "Author", "Year"):
        table.heading(col, text=col)
    table.grid(row=7, column=0, columnspan=3, pady=20)

    def view_all():
        db = get_connection()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM books")
        rows = cursor.fetchall()
        db.close()

        table.delete(*table.get_children())
        for r in rows:
            table.insert("", tk.END, values=r)

    def add_book():
        if title.get()=="" or author.get()=="" or year.get()=="":
            messagebox.showerror("Error", "All fields required")
            return

        db = get_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO books (title, author, year) VALUES (%s, %s, %s)",
                       (title.get(), author.get(), year.get()))
        db.commit()
        db.close()
        view_all()

    def get_selected(event):
        selected = table.focus()
        values = table.item(selected, "values")
        if values:
            id_entry.delete(0, tk.END)
            id_entry.insert(tk.END, values[0])
            title.delete(0, tk.END)
            title.insert(tk.END, values[1])
            author.delete(0, tk.END)
            author.insert(tk.END, values[2])
            year.delete(0, tk.END)
            year.insert(tk.END, values[3])

    table.bind("<ButtonRelease-1>", get_selected)

    # Hidden ID field for update/delete
    id_entry = tk.Entry(win)
    id_entry.grid(row=1, column=3)

    def update_book():
        if id_entry.get()=="":
            messagebox.showerror("Error", "Select a row to update")
            return

        db = get_connection()
        cursor = db.cursor()
        cursor.execute("""
            UPDATE books SET title=%s, author=%s, year=%s WHERE id=%s
        """, (title.get(), author.get(), year.get(), id_entry.get()))
        db.commit()
        db.close()
        view_all()

    def delete_book():
        if id_entry.get()=="":
            messagebox.showerror("Error", "Select a row to delete")
            return

        db = get_connection()
        cursor = db.cursor()
        cursor.execute("DELETE FROM books WHERE id=%s", (id_entry.get(),))
        db.commit()
        db.close()
        view_all()

    # ---------------- BUTTONS ----------------
    tk.Button(win, text="Add Book", command=add_book).grid(row=4, column=0)
    tk.Button(win, text="Update Book", command=update_book).grid(row=4, column=1)
    tk.Button(win, text="Delete Book", command=delete_book).grid(row=4, column=2)
    tk.Button(win, text="View All", command=view_all).grid(row=5, column=1)

    view_all()
    win.mainloop()
