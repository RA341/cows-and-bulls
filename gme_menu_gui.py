from tkinter import *

top = Tk()

_bgcolor = '#d9d9d9'  # X11 color: 'gray85'
_fgcolor = '#000000'  # X11 color: 'black'
_compcolor = '#d9d9d9'  # X11 color: 'gray85'
_ana1color = '#d9d9d9'  # X11 color: 'gray85'
_ana2color = '#ececec'  # Closest X11 color: 'gray92'

top.geometry("600x448+1007+19")
top.minsize(148, 1)
top.maxsize(1924, 1055)
top.resizable(1, 1)
top.title("New Toplevel")
top.configure(background="#d9d9d9")

Frame2 = Frame(top)
Frame2.place(relx=0.117, rely=0.268, relheight=0.658
                  , relwidth=0.758)
Frame2.configure(relief='groove')
Frame2.configure(borderwidth="2")
Frame2.configure(relief="groove")
Frame2.configure(background="#d9d9d9")

new_game_button = Button(Frame2)
new_game_button.place(relx=0.114, rely=0.149, height=43, width=136)
new_game_button.configure(activebackground="#ececec")
new_game_button.configure(activeforeground="#000000")
new_game_button.configure(background="#d9d9d9")
new_game_button.configure(disabledforeground="#a3a3a3")
new_game_button.configure(foreground="#000000")
new_game_button.configure(highlightbackground="#d9d9d9")
new_game_button.configure(highlightcolor="black")
new_game_button.configure(pady="0")
new_game_button.configure(text="New Game")

Back_button = Button(Frame2)
Back_button.place(relx=0.352, rely=0.712, height=43, width=136)
Back_button.configure(activebackground="#ececec")
Back_button.configure(activeforeground="#000000")
Back_button.configure(background="#d9d9d9")
Back_button.configure(disabledforeground="#a3a3a3")
Back_button.configure(foreground="#000000")
Back_button.configure(highlightbackground="#d9d9d9")
Back_button.configure(highlightcolor="black")
Back_button.configure(pady="0")
Back_button.configure(text="Back")

Continue = Button(Frame2)
Continue.place(relx=0.552, rely=0.149, height=43, width=136)
Continue.configure(activebackground="#ececec")
Continue.configure(activeforeground="#000000")
Continue.configure(background="#d9d9d9")
Continue.configure(disabledforeground="#a3a3a3")
Continue.configure(foreground="#000000")
Continue.configure(highlightbackground="#d9d9d9")
Continue.configure(highlightcolor="black")
Continue.configure(pady="0")
Continue.configure(text="Continue")

Frame1 = Frame(top)
Frame1.place(relx=0.117, rely=0.045, relheight=0.167
                  , relwidth=0.758)
Frame1.configure(relief='groove')
Frame1.configure(borderwidth="2")
Frame1.configure(relief="groove")
Frame1.configure(background="#d9d9d9")

Menu_label = Label(Frame1)
Menu_label.place(relx=0.154, rely=0.267, height=36, width=322)
Menu_label.configure(background="#d9d9d9")
Menu_label.configure(disabledforeground="#a3a3a3")
Menu_label.configure(foreground="#000000")
Menu_label.configure(text="Game Settings")

top.mainloop()

