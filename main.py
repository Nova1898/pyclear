import tkinter as tk
import psutil
import os

def check_unresponsive_windows():
    unresponsive_windows = []
    for process in psutil.process_iter(['pid', 'name', 'status']):
        if process.info['status'] == 'not responding':
            unresponsive_windows.append(process)

    return unresponsive_windows

def close_window(process):
    try:
        os.kill(process.info['pid'], 9)
    except Exception as e:
        print(f"Failed to close the window with PID {process.info['pid']}: {e}")

def refresh_listbox():
    unresponsive_windows = check_unresponsive_windows()
    listbox.delete(0, tk.END)
    for process in unresponsive_windows:
        listbox.insert(tk.END, f"PID: {process.info['pid']} | Name: {process.info['name']}")

def close_selected_window():
    selected_index = listbox.curselection()
    if selected_index:
        selected_process = check_unresponsive_windows()[selected_index[0]]
        close_window(selected_process)
        refresh_listbox()

# Create the main window
window = tk.Tk()
window.title("Unresponsive Windows")
window.geometry("400x300")

# Create a listbox to display the unresponsive windows
listbox = tk.Listbox(window)
listbox.pack(fill=tk.BOTH, expand=True)

# Create a Refresh button
refresh_button = tk.Button(window, text="Refresh", command=refresh_listbox)
refresh_button.pack(pady=5)

# Create a Close button
close_button = tk.Button(window, text="Close Selected", command=close_selected_window)
close_button.pack(pady=5)

# Initial refresh of the listbox
refresh_listbox()

# Start the main event loop
window.mainloop()
