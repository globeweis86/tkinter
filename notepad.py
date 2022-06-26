import tkinter as tk
from tkinter import messagebox as tkmb
from pathlib import Path

# first line
root = tk.Tk()

# configure root
root.title('My Notepad')
root.geometry('800x600')
root.columnconfigure(0, weight=1)
root.rowconfigure(3, weight=1)

# subject

subj_frame = tk.Frame(root)
subj_frame.columnconfigure(1, weight=1)
subject_var = tk.StringVar()
tk.Label(
    subj_frame,
    text='Subject: '
).grid(sticky='we', padx=5, pady=5)
tk.Entry(
    subj_frame,
    textvariable=subject_var
).grid(row=0, column=1, sticky=tk.E + tk.W)
subj_frame.grid(sticky='ew')

# category

cat_frame = tk.Frame(root)
cat_frame.columnconfigure(1, weight=1)
cat_var = tk.StringVar()
categories = ['Work', 'Hobbies', 'Health', 'Money']
tk.Label(
    cat_frame,
    text='Category: '
).grid(sticky=tk.E + tk.W, padx=5, pady=5)
cat_inp = tk.OptionMenu(
    cat_frame,
    cat_var,
    *categories
).grid(row=0, column=1, sticky=tk.E + tk.W, padx=5, pady=5)
cat_frame.grid(sticky='ew')

# private

private_var = tk.BooleanVar(value=False)
private_inp = tk.Checkbutton(
    root,
    variable=private_var,
    text='Private'
).grid(sticky='w', ipadx=5, ipady=5)

# message
message_frame = tk.LabelFrame(root, text='Message')
message_frame.columnconfigure(0, weight=1)
message_inp =tk.Text(message_frame)
message_inp.grid(sticky='nesw')

scrollbar = tk.Scrollbar(message_frame)
scrollbar.grid(row=0, column=1, sticky='nse')
message_frame.grid(sticky='nsew')
scrollbar.configure(command=message_inp.yview)
message_inp.configure(yscrollcommand=scrollbar.set)

# save button

save_btn = tk.Button(
    root,
    text='Save'
)
save_btn.grid(sticky=tk.E, ipadx=5, ipady=5)

# status bar

status_var = tk.StringVar()
status_bar = tk.Label(
    root,
    textvariable=status_var
).grid(row=100, ipadx=5, ipady=5)

# functions and bindings
def weaksauce_encrypt(text, password):
    """Weak encryption"""

    offset = sum([ord(x) for x in password])
    encoded = ''.join(
        chr(min(ord(x) + offset, 2**20))
        for x in text
    )
    return encoded

def weaksuace_decrypt(text, password):
    """Weak Decryption"""
    offset = sum([ord(x) for x in password])
    decoded = ''.join(
        chr(max(ord(x) - offset, 0))
        for x in text
    )
    return decoded

def save():
    """Save the data to a file"""

    subject = subject_var.get()
    category = cat_var.get()
    private = private_var.get()
    message = message_inp.get('1.0', tk.END)
    extension = 'txt' if not private else 'secret'
    filename = f'{category} - {subject}.{extension}'
    if private:
        message = weaksauce_encrypt(message, 'password')

    with open(filename, 'w') as fh:
        fh.write(message)

    status_var.set(f'Message was saved to {filename}')
    tkmb.showinfo('Saved', f'Message was saved to {filename}')

save_btn.configure(command=save)

def check_filename(*args):
    """check if filename is already in use"""
    subject = subject_var.get()
    category = cat_var.get()
    private = private_var.get()

    extension = 'txt' if not private else 'secret'
    filename = f'{category} - {subject}.{extension}'

    if Path(filename).exists():
        status_var.set(f'WARNING: {filename} already exists!')
    else:
        status_var.set('')

subject_var.trace_add('write', check_filename)
cat_var.trace_add('write', check_filename)
private_var.trace_add('write', check_filename)

# last line
root.mainloop()