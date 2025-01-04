import tkinter as tk
from tkinter import messagebox

def start_gui(dense_index_db):
    root = tk.Tk()
    root.title("Dense Index DB")

    # Search Section
    search_frame = tk.Frame(root)
    search_frame.pack(pady=10)

    tk.Label(search_frame, text="Search Key: ").grid(row=0, column=0)
    search_entry = tk.Entry(search_frame)
    search_entry.grid(row=0, column=1)

    def on_search():
        key_str = search_entry.get().strip()
        if not key_str.isdigit():
            messagebox.showerror("Error", "Key must be an integer")
            return
        key = int(key_str)
        found, comparisons = dense_index_db.search_with_comparisons(key)
        if found is not None:
            messagebox.showinfo("Found", f"Value: {found}\nComparisons: {comparisons}")
        else:
            messagebox.showinfo("Not Found", f"Record not found.\nComparisons: {comparisons}")

    tk.Button(search_frame, text="Search", command=on_search).grid(row=0, column=2, padx=5)

    # Insert Section
    insert_frame = tk.Frame(root)
    insert_frame.pack(pady=10)

    tk.Label(insert_frame, text="Insert Key: ").grid(row=0, column=0)
    ins_key_entry = tk.Entry(insert_frame)
    ins_key_entry.grid(row=0, column=1)

    tk.Label(insert_frame, text="Insert Value: ").grid(row=1, column=0)
    ins_val_entry = tk.Entry(insert_frame)
    ins_val_entry.grid(row=1, column=1)

    def on_insert():
        k_str = ins_key_entry.get().strip()
        val = ins_val_entry.get().strip()
        if not k_str.isdigit():
            messagebox.showerror("Error", "Key must be an integer")
            return
        key = int(k_str)
        dense_index_db.insert(key, val)
        messagebox.showinfo("Inserted", "Record inserted successfully")

    tk.Button(insert_frame, text="Insert", command=on_insert).grid(row=2, column=0, columnspan=2, pady=5)

    # Delete Section
    delete_frame = tk.Frame(root)
    delete_frame.pack(pady=10)

    tk.Label(delete_frame, text="Delete Key: ").grid(row=0, column=0)
    del_key_entry = tk.Entry(delete_frame)
    del_key_entry.grid(row=0, column=1)

    def on_delete():
        k_str = del_key_entry.get().strip()
        if not k_str.isdigit():
            messagebox.showerror("Error", "Key must be integer")
            return
        key = int(k_str)
        success = dense_index_db.delete(key)
        if success:
            messagebox.showinfo("Deleted", "Record deleted successfully")
        else:
            messagebox.showinfo("Failed", "Record not found")

    tk.Button(delete_frame, text="Delete", command=on_delete).grid(row=1, column=0, columnspan=2, pady=5)

    # Edit Section
    edit_frame = tk.Frame(root)
    edit_frame.pack(pady=10)

    tk.Label(edit_frame, text="Edit Key: ").grid(row=0, column=0)
    edit_key_entry = tk.Entry(edit_frame)
    edit_key_entry.grid(row=0, column=1)

    tk.Label(edit_frame, text="New Value: ").grid(row=1, column=0)
    edit_val_entry = tk.Entry(edit_frame)
    edit_val_entry.grid(row=1, column=1)

    def on_edit():
        k_str = edit_key_entry.get().strip()
        new_val = edit_val_entry.get().strip()
        if not k_str.isdigit():
            messagebox.showerror("Error", "Key must be integer")
            return
        key = int(k_str)
        success = dense_index_db.edit(key, new_val)
        if success:
            messagebox.showinfo("Edited", "Record updated successfully")
        else:
            messagebox.showinfo("Failed", "Record not found")

    tk.Button(edit_frame, text="Edit", command=on_edit).grid(row=2, column=0, columnspan=2, pady=5)

    root.mainloop()
