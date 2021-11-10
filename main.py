# Password Manager GUI

#########################
# Created by 4bd3ss4m4d #
#########################

from tkinter import *
from tkinter import messagebox
import random
import pyperclip  # Module to copy string automatically
import json

# ---------------------------- CONSTANTS ------------------------------- #
# GUI CONSTANTS
BG_COLOR = '#F7F6E7'
BUTTON_BG_COLOR = '#F7F6E7'
BUTTON_FG_COLOR = 'black'
GENERATE_BG = '#d4483b'
GENERATE_FG = '#F7F6E7'
ADD_BG = '#d4483b'
ADD_FG = '#F7F6E7'
FONT = ('Open Sans', 12, 'bold')
LABEL_FRAME_PADX = 10
LABEL_FRAME_PADY = 5
LABELS_PADX = 5
LABELS_PADY = 5
ENTRIES_FRAME_PADX = 10
ENTRIES_FRAME_PADY = 5
ADD_BUTTON_FRAME_PADX = 10
ADD_BUTTON_FRAME_PADY = 5
WEBSITE_WIDTH = 25
WEBSITE_PADX = 5
WEBSITE_PADY = 5
ENTRY_PADX = 5
ENTRY_PADY = 5
BUTTON_PADX = 5
BUTTON_PADY = 5
ENTRY_WIDTH = 40
PASSWORD_WIDTH = 25
GENERATE_BUTTON_WIDTH = 15
SEARCH_BUTTON_WIDTH = 15
ADD_BUTTON_WIDTH = 50
STICKY = 'W'

# PASSWORD GENERATOR CONSTANTS
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

# ---------------------------- PASSWORD GENERATOR ---------------------------- #
nr_letters = random.randint(8, 10)
nr_symbols = random.randint(2, 4)
nr_numbers = random.randint(2, 4)


def generate_password():
    # Empty password entry field
    password_entry.delete(0, END)

    # Generate Password
    password_list = []
    for char in range(nr_letters):
        password_list.append(random.choice(letters))
    for char in range(nr_symbols):
        password_list += random.choice(symbols)
    for char in range(nr_numbers):
        password_list += random.choice(numbers)
    random.shuffle(password_list)
    password = ""
    for char in password_list:
        password += char

    # Insert randomly generated password in password entry field
    password_entry.insert(0, password)
    # Automatically copy the password generated
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ---------------------------- #
def save_data():
    # Get Data entered
    website_entered = website_entry.get().capitalize()
    em_us_entered = em_us_entry.get()
    password_chosen = password_entry.get()
    new_data = {
        website_entered: {
            "email/username": em_us_entered,
            "password": password_chosen
        }
    }

    # Check if User didn't fill all fields
    if website_entered == '' or em_us_entered == '' or password_chosen == '':
        message = "You've left one or more fields empty!"
        messagebox.showinfo("Ops!", message)

    else:

        # Confirm data added by user
        proceed = messagebox.askyesno(title=website_entered, message=f"These are the details entered: \
                                                        \nEmail\\Username: {em_us_entered}\nPassword: {password_chosen}\n"
                                                                     f"Would you like to proceed?")
        if proceed:
            # Export data to a file as JSON
            # Try to open JSON file that contains accounts
            try:
                # Opening file that contains accounts
                with open('accounts.json', 'r') as read_accounts:
                    # Convert JSON data to dict
                    json_data_dict = json.load(read_accounts)
                    # Update accounts.json with new data
                    json_data_dict.update(new_data)
                    # create new accounts.json that appends the new data
                    with open('accounts.json', 'w') as write_accounts:
                        json.dump(json_data_dict, write_accounts, indent=4)
            except FileNotFoundError:
                # Create a new JSON file
                with open('accounts.json', 'w') as write_accounts:
                    # Transfer new data to the newly created accounts.json
                    json.dump(new_data, write_accounts, indent=4)

            # Show Message box
            messagebox.showinfo("Successful", "Password successfully added.")

            # Clear entries
            website_entry.delete(0, END)
            em_us_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- SEARCH ACCOUNT ---------------------------- #
def search_account():
    # Get input fromWebsite entry
    account_searched = website_entry.get().capitalize()

    try:
        # Open accounts.json file
        read_file = open('accounts.json', 'r')
        # Convert accounts.json to dict
        json_data_dict = json.load(read_file)
        # Try to search the for the account
        account_details = json_data_dict[account_searched]
        # Show Details of the account searched by the user
        show_details = messagebox.showinfo(title=account_searched, message=f"Email/Username: " \
                                                                           f"{account_details['email/username']}\nPassword: {account_details['password']}")
    # Handle FileNotFoundError
    except FileNotFoundError:
        not_found_message = 'Accounts file not found!'
        show_not_found = messagebox.showerror(title='Ops!', message=not_found_message)

    # Handle KeyError
    except KeyError:
        show_not_found = messagebox.showwarning(title='Ops!', message=f'There is no details for {account_searched}!')


# ---------------------------- UI SETUP ------------------------------- #


###################
# Set Root Window #
###################

root = Tk()
root.title("Password Manager")
root.config(padx=20, pady=20, bg=BG_COLOR)

####################
# Set Image Canvas #
####################

# Set a Canvas
canvas = Canvas(width=200, height=200, bg=BG_COLOR, highlightthickness=0)
# Define variable to hold logo image
logo_image = PhotoImage(file="logo.png")
# Set Logo image on canvas
canvas.create_image(100, 100, image=logo_image)
# Set Grid for Canvas
canvas.grid(column=1, row=0)

####################
# Add Labels Frame #
####################

# Set Labels Frame
labels_frame = Frame(root)
labels_frame.config(bg=BG_COLOR)
labels_frame.grid(column=0, row=1, padx=LABEL_FRAME_PADX, pady=LABEL_FRAME_PADY, sticky=STICKY)

# Website label
website_label = Label(labels_frame)
website_label.config(text='Website: ', bg=BG_COLOR, font=FONT)
website_label.grid(column=0, row=0, padx=LABELS_PADX, pady=LABELS_PADY, sticky=STICKY)

# Email/Username label
em_us_label = Label(labels_frame)
em_us_label.config(text='Email/Username: ', bg=BG_COLOR, font=FONT)
em_us_label.grid(column=0, row=1, padx=LABELS_PADX, pady=LABELS_PADY, sticky=STICKY)

# Password label
password_label = Label(labels_frame)
password_label.config(text='Password: ', bg=BG_COLOR, font=FONT)
password_label.grid(column=0, row=2, padx=LABELS_PADX, pady=LABELS_PADY, sticky=STICKY)

#####################
# Add Entries Frame #
#####################

# Set Entries Frame
entries_frame = Frame(root)
entries_frame.config(bg=BG_COLOR)
entries_frame.grid(column=1, row=1, padx=ENTRIES_FRAME_PADX, pady=ENTRIES_FRAME_PADX, sticky=STICKY)

# Website entry
website_entry = Entry(entries_frame)
website_entry.config(width=WEBSITE_WIDTH, font=FONT)
website_entry.focus()
website_entry.grid(column=0, row=0, padx=ENTRY_PADX, pady=ENTRY_PADY, sticky=STICKY)

# Search button
search_button = Button(entries_frame)
search_button.config(width=GENERATE_BUTTON_WIDTH,
                     text="Search",
                     font=('Open Sans', 10, 'bold'),
                     bg=GENERATE_BG,
                     fg=GENERATE_FG,
                     command=search_account)
search_button.grid(column=1, row=0, padx=BUTTON_PADX, pady=BUTTON_PADY)

# Email/Username entry
em_us_entry = Entry(entries_frame)
em_us_entry.config(width=ENTRY_WIDTH, font=FONT)
em_us_entry.grid(column=0, row=1, columnspan=2, padx=ENTRY_PADX, pady=ENTRY_PADY, sticky=STICKY)

# Password entry
password_entry = Entry(entries_frame)
password_entry.config(width=PASSWORD_WIDTH, font=FONT)
password_entry.grid(column=0, row=2, padx=ENTRY_PADX, pady=ENTRY_PADY, sticky=STICKY)

# Generate button
generate_button = Button(entries_frame)
generate_button.config(width=GENERATE_BUTTON_WIDTH,
                       text="Generate",
                       font=('Open Sans', 10, 'bold'),
                       bg=GENERATE_BG,
                       fg=GENERATE_FG,
                       command=generate_password)
generate_button.grid(column=1, row=2, padx=BUTTON_PADX, pady=BUTTON_PADY)

# ####################
# # Add Button Frame #
# ####################

# Add Button Frame
add_button_frame = Frame(root)
add_button_frame.grid(column=1, row=2, padx=ADD_BUTTON_FRAME_PADX, pady=ADD_BUTTON_FRAME_PADY, sticky=STICKY)

# Add button
add_button = Button(add_button_frame)
add_button.config(width=ADD_BUTTON_WIDTH,
                  text="Add",
                  font=('Open Sans', 10, 'bold'),
                  bg=ADD_BG,
                  fg=ADD_FG,
                  highlightthickness=1,
                  command=save_data)
add_button.grid(column=0, row=0, padx=BUTTON_PADX, pady=BUTTON_PADY)

root.mainloop()
