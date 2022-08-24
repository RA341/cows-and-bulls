from tkinter import *
from tkinter import messagebox
import random
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE IF NOT EXISTS playerdatabase")

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="playerdatabase"
)

mycursor = mydb.cursor()
mycursor.execute(
    "CREATE TABLE IF NOT EXISTS playerdatabase.players (player_id INT(2) PRIMARY KEY, player_name VARCHAR(255), score INTEGER (4))")


########################################################################################
# Database functions

def insert(name):
    i = 0
    mycursor.execute("SELECT * FROM players ORDER BY player_id DESC LIMIT 1")
    for x in mycursor:
        if x == None:
            i = 1
        else:
            p = x
            (id, player, score) = p
            i = id + 1

    sql = "INSERT INTO players (player_id, player_name, score) VALUES (%s, %s, %s)"
    val = (i, name, 0)

    mycursor.execute(sql, val)
    mydb.commit()


def display():
    l = []
    mycursor.execute("SELECT * FROM players")
    myresult = mycursor.fetchall()
    for x in myresult:
        l.append(x)
    return l


def update(score, name):
    sql = "UPDATE players SET score = %s WHERE player_name = %s"
    val = (score, name)
    mycursor.execute(sql, val)
    mydb.commit()


def search(name):
    sql = "SELECT * FROM players WHERE player_name = %s"
    adr = (name,)
    mycursor.execute(sql, adr)
    myresult = mycursor.fetchone()
    return myresult


########################################################################################
# Game functions

def player_window():
    def apply():
        global player_data, current_player
        s = selected.get()
        e = player_entry.get()
        if len(s) == 0 and len(e) > 0:
            n = search(e)
            if n == e:
                messagebox.showerror("error", "Error: Name already exists try again")
                player_entry.delete(0, END)
            else:
                insert(e)
                player_data = search(e)

            player_data = list(player_data)
            mycursor.execute("SELECT MAX(score) FROM players")
            for x in mycursor:
                highscore_Label.configure(text="Global High Score:" + str(x[0]) + "\nYour score:" + str(player_data[2]))
            title_Label.configure(text="Welcome " + player_data[1])
            info_label.configure(text="No Difficulty selected.\nSelect Difficulty")
            player_title.configure(text=player_data[1])

            play_button.configure(state=DISABLED)
            difficulty_Button.configure(state=NORMAL)

            root2.destroy()

        elif len(s) > 0 and len(e) == 0:
            player_data = search(s)
            player_data = list(player_data)
            mycursor.execute("SELECT MAX(score) FROM players")
            for x in mycursor:
                highscore_Label.configure(text="High Score:" + str(x[0]) + "\nYour last score:" + str(player_data[2]))

            title_Label.configure(text="Welcome back " + player_data[1])
            info_label.configure(text="No Difficulty selected.\nSelect Difficulty")
            player_title.configure(text=player_data[1])

            play_button.configure(state=DISABLED)
            difficulty_Button.configure(state=NORMAL)
            root2.destroy()

        elif len(s) >= 0 and len(e) >= 0:
            messagebox.showerror("error", "Select from existing user list or\nEnter as new user")
            player_entry.delete(0, END)
            selected.set("")

        current_player = player_data[1]

    root2 = Toplevel(top)

    root2.title("Player")
    root2.geometry("250x230")

    player_title_2 = Label(root2, text="Existing Player")
    player_title_2.pack()

    options = optionlist()
    selected = StringVar()

    if options == []:
        menu = OptionMenu(root2, selected, options)
        menu.pack(pady=20)
    else:
        menu = OptionMenu(root2, selected, *options)
        menu.pack(pady=20)

    player_title = Label(root2, text="New Player")
    player_title.pack()

    player_entry = Entry(root2)
    player_entry.pack(pady=20)

    ok_button = Button(root2, text="OK", command=apply)
    ok_button.pack()


def diff_window():
    def apply():
        global number, difficulty
        number = ""
        difficulty = selected.get()
        if difficulty == "Easy":
            difficulty = 4
            info_label.configure(text="Number will be 4 digits long")
        elif difficulty == "Medium":
            difficulty = 6
            info_label.configure(text="Number will be 6 digits long")
        elif difficulty == "Hard":
            difficulty = 10
            info_label.configure(text="Number will be 10 digits long")

        for x in range(difficulty):
            p = str(random.randrange(10))
            number += p

        if cheat_var.get() == 1:
            print(number)

        difficulty_Button.configure(state=DISABLED)
        result_button.configure(state="normal")
        root.destroy()

    root = Toplevel(top)
    root.title("")
    root.geometry("250x200")

    options = ["Easy", "Medium", "Hard", ]

    title = Label(root, text="Select difficulty")
    title.pack()

    cheat_var = IntVar()
    selected = StringVar()
    selected.set(options[0])

    menu = OptionMenu(root, selected, *options)
    menu.pack(pady=20)

    apply_button = Button(root, text="Apply", command=apply)
    apply_button.pack()

    cheat_check = Checkbutton(root, text="Enable Cheat", variable=cheat_var, onvalue=1, offvalue=0, height=5, width=10)
    cheat_check.pack()


def check(number):
    global tries
    bull_check = []
    cow_check = []
    double_check = {}
    bulls = 0
    guess = guess_box.get()
    info_label.configure(text="")

    if len(guess) != difficulty:
        messagebox.showerror("error", "Error:Guess must be " + str(difficulty) + " digits long")
        guess_box.delete(0, END)
    else:
        last_guess.configure(text=guess)

        for x in number:
            if x not in double_check.keys():
                p = number.count(x)
                double_check[x] = p

        if guess != number:
            tries += 1
            guess = list(guess)
            number = list(number)
            for x in range(len(number)):
                if guess[x] == number[x]:
                    bulls += 1
                    bull_check.append(guess[x])
                elif guess[x] in number:
                    cow_check.append(guess[x])

            # print(bull_check)
            # print(cow_check)

            o = [x for x in cow_check if x not in bull_check]  # filtering
            for x in o:
                if o.count(x) > double_check[x]:
                    o.remove(x)

            # print("Test"+str(o))

            cows = len(o)
            result_box.configure(text="Bulls: " + str(bulls) + " " + "Cows: " + str(cows))
            guess = ''.join([str(x) for x in guess])
            guess_box.delete(0, END)
            last_guess.configure(text="last guess : " + guess)
        else:
            score()


def optionlist():
    options = []
    player_list = []
    l = display()
    for x in l:
        player_list.append(x)
    for x in player_list:
        player = x
        (id, name, score) = player
        options.append(name)
    return options


def score():
    global difficulty, player_data, tries, player_score

    player_score = int(player_score)
    if difficulty == 4:
        player_score += 25
    elif difficulty == 6:
        player_score += 50
    elif difficulty == 8:
        player_score += 100

    if tries <= 7:
        player_score += 100
    elif tries <= 10:
        player_score += 50
    else:
        player_score += 25

    if play_state == True:
        player_data[2] += int(player_score)
    else:
        player_data[2] = int(player_score)

    update(player_data[2], player_data[1])
    guess_box.delete(0, END)
    result_button.configure(state=DISABLED)
    result_box.configure(text="")
    last_guess.configure(text="Congratulations!! You have found the correct Number\nYour score is " + str(player_score))
    reset()


def reset():
    global tries, play_state
    tries = 0
    msg = messagebox.askquestion("Confirm", "Play Again?")
    if msg == 'yes':
        info_label.configure(text="No Difficulty selected.\nSelect Difficulty")
        last_guess.configure(text="0")
        result_box.configure(text="")
        difficulty_Button.configure(state=NORMAL)
        play_state = True
    else:
        play_button.configure(state=NORMAL)
        difficulty_Button.configure(state=DISABLED)
        highscore_Label.configure(text="")
        title_Label.configure(text="Cows and Bulls")
        info_label.configure(text="No player selected.\nClick play")
        last_guess.configure(text="")
        result_box.configure(text="")
        play_state = False

    result_button.configure(state=DISABLED)


########################################################################################
# Colour
bg = "#ffffff"
foreg = "#000000"

# tkinter initialisation

top = Tk()

top.geometry("569x476")
top.resizable(False, False)
top.title("Cows and Bulls")
top.configure(background=bg)


########################################################################################
# Game variables

number = ""
difficulty = 0
guess = ""
tries = 0
player_score = 0
current_player = ""
player_data = []
play_state = False

########################################################################################
# Gui

# Frames
menu_Frame = Frame(top)
menu_Frame.place(relx=0.013, rely=0.021, relheight=0.284, relwidth=0.975)
menu_Frame.configure(relief='groove', borderwidth="2", background=bg)

main_frame = Frame(top)
main_frame.place(relx=0.013, rely=0.336, relheight=0.641, relwidth=0.975)
main_frame.configure(relief='groove', borderwidth="2", background=bg)

# Menu labels
title_Label = Label(menu_Frame)
title_Label.place(relx=0.342, rely=0.074, height=26, width=162)
title_Label.configure(background=bg, fg=foreg)
title_Label.configure(text="Cows and Bulls")

highscore_Label = Label(menu_Frame)
highscore_Label.place(relx=0.036, rely=0.148, height=30, width=130)
highscore_Label.configure(background=bg, fg=foreg)

info_label = Label(menu_Frame)
info_label.place(relx=0.650, rely=0.148, height=30, width=170)
info_label.configure(background=bg, fg=foreg)
info_label.configure(text="No player selected.\nClick play")

# Menu buttons
exit_button = Button(menu_Frame)
exit_button.place(relx=0.18, rely=0.593, height=33, width=76)
exit_button.configure(background=bg, fg=foreg, disabledforeground="grey")
exit_button.configure(text="Exit")
exit_button.configure(command=quit)

play_button = Button(menu_Frame)
play_button.place(relx=0.432, rely=0.593, height=33, width=76)
play_button.configure(background=bg, fg=foreg, disabledforeground="grey")
play_button.configure(command=lambda: player_window())
play_button.configure(text="Play")

difficulty_Button = Button(menu_Frame)
difficulty_Button.place(relx=0.667, rely=0.593, height=33, width=76)
difficulty_Button.configure(background=bg, fg=foreg, disabledforeground="grey")
difficulty_Button.configure(text="Difficulty")
difficulty_Button.configure(command=lambda: diff_window())
difficulty_Button.configure(state=DISABLED)

# Main Game_ui
guess_box = Entry(main_frame)
guess_box.place(relx=0.324, rely=0.131, height=34, relwidth=0.314)
guess_box.configure(background=bg)
guess_box.configure(font="TkFixedFont")

guess_label = Label(main_frame)
guess_label.place(relx=0.09, rely=0.131, height=36, width=92)
guess_label.configure(background=bg, fg=foreg)
guess_label.configure(text="Enter Guess")

result_button = Button(main_frame)
result_button.place(relx=0.757, rely=0.131, height=33, width=76)
result_button.configure(background=bg, disabledforeground="grey", fg=foreg)
result_button.configure(text="Check")
result_button.configure(command=lambda: check(number))
result_button.configure(state=DISABLED)

result_box = Label(main_frame)
result_box.place(relx=0.234, rely=0.426, height=36, width=292)
result_box.configure(background=bg, fg=foreg)
result_box.configure()

last_guess = Label(main_frame)
last_guess.place(relx=0.234, rely=0.689, height=36, width=292)
last_guess.configure(background=bg, fg=foreg)
last_guess.configure(text=player_score)

top.mainloop()

########################################################################################
