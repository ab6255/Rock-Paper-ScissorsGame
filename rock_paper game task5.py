import tkinter as tk
import random
import sqlite3

# Function to determine the winner
def determine_winner(user_choice, computer_choice):
    if user_choice == computer_choice:
        return "It's a tie!"
    elif (user_choice == "rock" and computer_choice == "scissors") or \
         (user_choice == "scissors" and computer_choice == "paper") or \
         (user_choice == "paper" and computer_choice == "rock"):
        return "You win!"
    else:
        return "Computer wins!"

# Function to handle user's choice
def user_choice(choice):
    computer_choices = ["rock", "paper", "scissors"]
    computer_choice = random.choice(computer_choices)

    result = determine_winner(choice, computer_choice)
    result_label.config(text=f"Your choice: {choice}\nComputer's choice: {computer_choice}\n{result}")

    if result == "You win!":
        update_score("user")
    elif result == "Computer wins!":
        update_score("computer")

# Function to update the score
def update_score(winner):
    conn = sqlite3.connect("scores.db")
    cursor = conn.cursor()

    if winner == "user":
        cursor.execute("UPDATE scores SET user_wins = user_wins + 1")
    elif winner == "computer":
        cursor.execute("UPDATE scores SET computer_wins = computer_wins + 1")

    conn.commit()
    conn.close()

# Function to display the leaderboard
def display_leaderboard():
    conn = sqlite3.connect("scores.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM scores")
    data = cursor.fetchone()

    if data is not None:
        leaderboard_label.config(text=f"User Wins: {data[0]}\nComputer Wins: {data[1]}")
    else:
        leaderboard_label.config(text="No leaderboard data available")

    conn.close()

# Create the main window
window = tk.Tk()
window.title("Rock-Paper-Scissors Game")

# Create and configure widgets
title_label = tk.Label(window, text="Rock-Paper-Scissors Game", font=("Helvetica", 16))
instruction_label = tk.Label(window, text="Choose your move:")
rock_button = tk.Button(window, text="Rock", command=lambda: user_choice("rock"))
paper_button = tk.Button(window, text="Paper", command=lambda: user_choice("paper"))
scissors_button = tk.Button(window, text="Scissors", command=lambda: user_choice("scissors"))
result_label = tk.Label(window, text="", font=("Helvetica", 14))
leaderboard_label = tk.Label(window, text="", font=("Helvetica", 12))

# Place widgets in the window
title_label.pack(pady=10)
instruction_label.pack()
rock_button.pack()
paper_button.pack()
scissors_button.pack()
result_label.pack(pady=20)
leaderboard_label.pack()

# Initialize the database if it doesn't exist
conn = sqlite3.connect("scores.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS scores (user_wins INTEGER DEFAULT 0, computer_wins INTEGER DEFAULT 0)")
conn.commit()
conn.close()

# Display the initial leaderboard
display_leaderboard()

# Start the main loop
window.mainloop()