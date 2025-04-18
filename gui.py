import tkinter as tk
from tkinter import messagebox

def start_gui(dense_index_db):
    """Initializes and runs the Tkinter GUI for Dense Index DB operations."""
    root = tk.Tk()
    root.title("Dense Index DB")

    # --- Search Section ---
    search_frame = tk.Frame(root, padx=10, pady=5)
    search_frame.pack(fill=tk.X)
    tk.Label(search_frame, text="Search Key:").pack(side=tk.LEFT)
    search_entry = tk.Entry(search_frame)
    search_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

    def on_search():
        """Handles the search button click event."""
        key_str = search_entry.get().strip()
        try:
            key = int(key_str)
        except ValueError:
            messagebox.showerror("Error", "Key must be an integer.")
            return

        value, comparisons = dense_index_db.search_with_comparisons(key)
        if value is not None:
            messagebox.showinfo("Search Result", f"Record found.\nValue: {value}\nComparisons: {comparisons}")
        else:
            messagebox.showinfo("Search Result", f"Record with key {key} not found.\nComparisons: {comparisons}")
        search_entry.delete(0, tk.END)

    tk.Button(search_frame, text="Search", command=on_search).pack(side=tk.LEFT)

    # --- Insert Section ---
    insert_frame = tk.Frame(root, padx=10, pady=5)
    insert_frame.pack(fill=tk.X)
    tk.Label(insert_frame, text="Key:").grid(row=0, column=0, sticky=tk.W)
    ins_key_entry = tk.Entry(insert_frame)
    ins_key_entry.grid(row=0, column=1, padx=5, sticky=tk.EW)
    tk.Label(insert_frame, text="Value:").grid(row=1, column=0, sticky=tk.W)
    ins_val_entry = tk.Entry(insert_frame)
    ins_val_entry.grid(row=1, column=1, padx=5, pady=2, sticky=tk.EW)
    insert_frame.grid_columnconfigure(1, weight=1)

    def on_insert():
        """Handles the insert button click event."""
        k_str = ins_key_entry.get().strip()
        val = ins_val_entry.get().strip()
        try:
            key = int(k_str)
        except ValueError:
            messagebox.showerror("Error", "Key must be an integer.")
            return
        if not val:
             messagebox.showwarning("Warning", "Value cannot be empty.")
             return

        success, message = dense_index_db.insert(key, val)

        if success:
            messagebox.showinfo("Insert Result", message)
            ins_key_entry.delete(0, tk.END)
            ins_val_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Insert Error", message)

    tk.Button(insert_frame, text="Insert", command=on_insert).grid(row=2, column=0, columnspan=2, pady=5)

    # --- Delete Section ---
    delete_frame = tk.Frame(root, padx=10, pady=5)
    delete_frame.pack(fill=tk.X)
    tk.Label(delete_frame, text="Delete Key:").pack(side=tk.LEFT)
    del_key_entry = tk.Entry(delete_frame)
    del_key_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

    def on_delete():
        """Handles the delete button click event."""
        k_str = del_key_entry.get().strip()
        try:
            key = int(k_str)
        except ValueError:
            messagebox.showerror("Error", "Key must be an integer.")
            return

        success, message = dense_index_db.delete(key)

        if success:
            messagebox.showinfo("Delete Result", message)
            del_key_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Delete Error", message)

    tk.Button(delete_frame, text="Delete", command=on_delete).pack(side=tk.LEFT)

    # --- Edit Section ---
    edit_frame = tk.Frame(root, padx=10, pady=5)
    edit_frame.pack(fill=tk.X)
    tk.Label(edit_frame, text="Key:").grid(row=0, column=0, sticky=tk.W)
    edit_key_entry = tk.Entry(edit_frame)
    edit_key_entry.grid(row=0, column=1, padx=5, sticky=tk.EW)
    tk.Label(edit_frame, text="New Value:").grid(row=1, column=0, sticky=tk.W)
    edit_val_entry = tk.Entry(edit_frame)
    edit_val_entry.grid(row=1, column=1, padx=5, pady=2, sticky=tk.EW)
    edit_frame.grid_columnconfigure(1, weight=1)

    def on_edit():
        """Handles the edit/update button click event."""
        k_str = edit_key_entry.get().strip()
        new_val = edit_val_entry.get().strip()
        try:
            key = int(k_str)
        except ValueError:
            messagebox.showerror("Error", "Key must be an integer.")
            return
        if not new_val:
             messagebox.showwarning("Warning", "New value cannot be empty.")
             return

        success, message = dense_index_db.edit(key, new_val)

        if success:
            messagebox.showinfo("Edit Result", message)
            edit_key_entry.delete(0, tk.END)
            edit_val_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Edit Error", message)

    tk.Button(edit_frame, text="Edit/Update", command=on_edit).grid(row=2, column=0, columnspan=2, pady=5)

    root.mainloop()