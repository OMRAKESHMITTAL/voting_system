import tkinter as tk
from tkinter import ttk
import hashlib
import json
from datetime import datetime

# Define candidates and their initial vote counts
candidates = {
    "BJP": 0,
    "INC": 0,
    "AAP": 0
}

# Blockchain implementation (simplified)
blocks = []
# Set to keep track of voters who have already voted
voted_voters = set()

# Admin credentials
admin_username = "admin"
admin_password = "admin123"

# Variable to track admin login status
is_admin = False

# Function to show voting options
def show_vote_options():
    voter_id_label.pack()
    voter_id_entry.pack()
    candidate_label.pack()
    candidate_BJP.pack()
    candidate_INC.pack()
    candidate_AAP.pack()
    vote_button.pack()

# Function to hide voting options
def hide_vote_options():
    voter_id_label.pack_forget()
    voter_id_entry.pack_forget()
    candidate_label.pack_forget()
    candidate_BJP.pack_forget()
    candidate_INC.pack_forget()
    candidate_AAP.pack_forget()
    vote_button.pack_forget()

# Function to show admin options
def show_admin_options():
    admin_username_label.pack()
    admin_username_entry.pack()
    admin_password_label.pack()
    admin_password_entry.pack()
    admin_login_button.pack()

# Function to hide admin options
def hide_admin_options():
    admin_username_label.pack_forget()
    admin_username_entry.pack_forget()
    admin_password_label.pack_forget()
    admin_password_entry.pack_forget()
    admin_login_button.pack_forget()

# Function to show voter registration options


# Function to hide voter registration options

# Function to handle option selection
def handle_option_selection(option_var):
    if option_var.get() == "admin":
        hide_vote_options()
        show_admin_options()
    elif option_var.get() == "vote":
        hide_admin_options()
        show_vote_options()

# Admin login function
def admin_login(username, password, vote_count_labels, status_label):
    global is_admin
    # Check admin credentials
    if username == admin_username and password == admin_password:
        is_admin = True
        status_label.config(text="Admin login successful.", fg="green")
        # Show the vote count labels
        for count_label in vote_count_labels.values():
            count_label.pack()
        # Show the Admin Logout button
        admin_logout_button.pack()

    else:
        is_admin = False
        status_label.config(text="Invalid admin credentials.", fg="red")


# Admin logout function
def admin_logout(vote_count_labels):
    global is_admin
    is_admin = False
    # Hide the vote count labels
    for count_label in vote_count_labels.values():
        count_label.pack_forget()
    # Hide the Admin Logout button
    admin_logout_button.pack_forget()



# Blockchain functions
def add_block(vote):
    # Create a new block with timestamp, previous block hash, and vote data
    block = {
        "timestamp": str(datetime.now()),
        "previous_hash": get_latest_block_hash(),
        "data": vote
    }

    # Calculate block hash using SHA-256
    block_hash = hashlib.sha256(json.dumps(block, sort_keys=True).encode('utf-8')).hexdigest()
    block['hash'] = block_hash

    # Add block to blockchain
    blocks.append(block)

def get_latest_block_hash():
    if len(blocks) == 0:
        return "0"
    else:
        return blocks[-1]['hash']

# Voting function
def cast_vote(voter_id, candidate, vote_count_labels, status_label):
    # Check if the user is an admin
    if is_admin:
        status_label.config(text="Admin cannot cast votes.", fg="red")
        return

    # Check if the voter has already voted
    if voter_id in voted_voters:
        status_label.config(text="Voter has already cast a vote.", fg="red")
        return

    # Check if candidate is valid
    if candidate not in candidates:
        status_label.config(text="Invalid candidate.", fg="red")
        return

    # Update vote count for the selected candidate
    candidates[candidate] += 1
    status_label.config(text="Vote cast successfully.", fg="green")

    # Mark the voter as voted
    voted_voters.add(voter_id)

    # Create vote record and add it to blockchain
    vote_record = {
        "voter_id": voter_id,
        "candidate": candidate
    }

    add_block(vote_record)

    # Update vote count labels
    for candidate, count_label in vote_count_labels.items():
        count_label.config(text=f"{candidate}: {candidates[candidate]}")

# Create Tkinter GUI
root = tk.Tk()
root.title("Vote")

# Create variable to store the selected option
option_var = tk.StringVar()

# Create radio buttons for selecting an option
option_vote = tk.Radiobutton(root, text="Cast Vote", value="vote", variable=option_var, command=lambda: handle_option_selection(option_var))
option_admin = tk.Radiobutton(root, text="Admin Login", value="admin", variable=option_var, command=lambda: handle_option_selection(option_var))

# Pack the radio buttons
option_vote.pack()
option_admin.pack()

# Create label and entry field for admin username
admin_username_label = tk.Label(root, text="Admin Username:")
admin_username_label.pack()

admin_username_entry = tk.Entry(root)
admin_username_entry.pack()

# Create label and entry field for admin password
admin_password_label = tk.Label(root, text="Admin Password:")
admin_password_label.pack()

admin_password_entry = tk.Entry(root, show="*")
admin_password_entry.pack()

# Create button for admin login
admin_login_button = ttk.Button(root, text="Admin Login", command=lambda: admin_login(admin_username_entry.get(), admin_password_entry.get(), vote_count_labels, status_label))
admin_login_button.pack()

# Create button for admin logout
admin_logout_button = ttk.Button(root, text="Admin Logout", command=lambda: admin_logout(vote_count_labels))
admin_logout_button.pack()

# Hide the Admin Logout button initially
admin_logout_button.pack_forget()

# Create label and entry field for voter ID
voter_id_label = tk.Label(root, text="Enter Voter ID:")
voter_id_label.pack()

voter_id_entry = tk.Entry(root)
voter_id_entry.pack()

# Create label and radio buttons for candidate selection
candidate_label = tk.Label(root, text="Select Candidate:")
candidate_label.pack()

# Create a variable to store the selected candidate
candidate_selection = tk.StringVar()

candidate_BJP = tk.Radiobutton(root, text="BJP", value="BJP", variable=candidate_selection)
candidate_BJP.pack()

candidate_INC = tk.Radiobutton(root, text="INC", value="INC", variable=candidate_selection)
candidate_INC.pack()

candidate_AAP = tk.Radiobutton(root, text="AAP", value="AAP", variable=candidate_selection)
candidate_AAP.pack()

# Create button for casting vote
vote_button = ttk.Button(root, text="Vote", command=lambda: cast_vote(voter_id_entry.get(), candidate_selection.get(), vote_count_labels, status_label))
vote_button.pack()

# Create status label
status_label = tk.Label(root, text="", fg="black")
status_label.pack()

# Create labels to display vote counts
vote_count_labels = {}
for candidate in candidates:
    vote_count_labels[candidate] = tk.Label(root, text=f"{candidate}: {candidates[candidate]}")

root.mainloop()