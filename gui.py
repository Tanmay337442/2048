# 2048 github link: https://github.com/Tanmay337442/2048

from tkinter import (Button, Entry, IntVar, Label, Menu, Radiobutton, Tk,
                     Toplevel, messagebox)
import game


def main():
    
    def intro():
            messagebox.showinfo("Help", "WASD / arrow keys / HJKL to move numbers\n\
R: reset current game\nN: create game in new window\nC: clear high score\nU: undo\n\
Q: close current game\nEsc: close all games\nI: open help menu")
    
    # get highscore from highscorefile
    try:
        highscore = int(open('highscorefile.txt', 'r').read())
    # handle error if file does not exist or int() throws an error
    except:
        highscore = open('highscorefile.txt', 'w').write('0')
        highscore = 0

    # set colours of squares
    square_colour = {
        2: "#eee4da",
        4: "#eee1c9",
        8: "#f3b27a",
        16: "#f69664",
        32: "#f77c5f",
        64: "#f75f3b",
        128: "#e5c96e",
        256: "#e8c85e",
        512: "#ecc850",
        1024: "#edc53f",
        2048: "#f0c02f",
        4096: "#3c3a32",
        8192: "#3c3a32",
        16384: "#3c3a32",
        32768: "#3c3a32",
        65536: "#3c3a32",
    }

    # set colours of numbers in squares
    text_colour = {
        2: "#776e65",
        4: "#776e65",
        8: "#f9f6f2",
        16: "#f9f6f2",
        32: "#f9f6f2",
        64: "#f9f6f2",
        128: "#f9f6f2",
        256: "#f9f6f2",
        512: "#f9f6f2",
        1024: "#f9f6f2",
        2048: "#f9f6f2"
    }

    def newgame():
        # create window
        win = Tk()
        win.title("2048")
        x, y = int((win.winfo_screenwidth() - 416)/2), int((win.winfo_screenheight() - 400)/2)
        win.geometry(f'{416}x{400}+{x}+{y}')
        win.config(bg="#bbada0")

        # set relative size of rows/cols used by squares - allows squares to be resizeable
        win.rowconfigure(0, weight=1)
        win.columnconfigure(0, weight=1)
        win.rowconfigure(1, weight=1)
        win.columnconfigure(1, weight=1)
        win.rowconfigure(2, weight=1)
        win.columnconfigure(2, weight=1)
        win.rowconfigure(3, weight=1)
        win.columnconfigure(3, weight=1)

        # initialize game
        matrix = game.board()
        pts = 0
        past_matrices = []
        past_matrices.append([matrix, pts, highscore])

        # store squares (labels) to update throughout game
        squaremat = [[] for x in range(4)]
        for x in range(4):
            for y in range(4):
                # create squares
                square = Label(win, text=str(), font=("Clear Sans", 20, "bold"), bg="#cdc1b4", width=100, height=100)
                square.grid(row=x, column=y, padx=4, pady=4, sticky="news")
                # add squares to matrix to change later
                squaremat[x].append(square)
        
        # labels to show points
        pointslabel = Label(win, text="Points", font=("Clear Sans", 10, "bold"), bg="#cdc1b4")
        pointslabel.grid(row=4, column=2, padx=4, pady=4, sticky="news")
        showpts = Label(win, text="", font=("Clear Sans", 15, "bold"), bg="#cdc1b4")
        showpts.grid(row=5, column=2, padx=4, pady=4, sticky="news")

        # labels to show high score
        highlabel = Label(win, text="Best", font=("Clear Sans", 10, "bold"), bg="#cdc1b4")
        highlabel.grid(row=4, column=3, padx=4, pady=4, sticky="news")
        showhigh = Label(win, text="", font=("Clear Sans", 15, "bold"), bg="#cdc1b4")
        showhigh.grid(row=5, column=3, padx=4, pady=4, sticky="news")

        # set variable for light/dark mode
        mode = IntVar()
        mode.set(1)

        # configure all widgets for light/dark mode
        def configbg():
            choice = mode.get()
            if choice == 1:
                win.config(bg="#bbada0")
                for item in [modelabel, light, dark, pointslabel, highlabel, showpts, showhigh, undobutton]:
                    item.config(bg="#cdc1b4")
            else:
                win.config(bg="#333333")
                for item in [modelabel, light, dark, pointslabel, highlabel, showpts, showhigh, undobutton]:
                    item.config(bg="#444444")

        # create mode radiobuttons and label
        modelabel = Label(win, text="Mode", font=("Clear Sans", 10, "bold"), bg="#cdc1b4")
        light = Radiobutton(win, variable=mode, value=1, text="Light UI", font=("Clear Sans", 10, "bold"), bg="#cdc1b4", command=lambda: [configbg(), change()])
        dark = Radiobutton(win, variable=mode, value=2, text="Dark UI", font=("Clear Sans", 10, "bold"), bg="#cdc1b4", command=lambda: [configbg(), change()])
        modelabel.grid(row=4, column=0, columnspan=2, padx=4, pady=4, sticky='news')
        light.grid(row=5, column=0, padx=4, pady=4, sticky='news')
        dark.grid(row=5, column=1, padx=4, pady=4, sticky='news')

        # create blank board for beginning of game
        def reset():
            nonlocal squaremat, matrix, pts, showpts, past_matrices
            matrix = game.board()
            past_matrices = []
            pts = 0
            for x in range(4):
                for y in range(4):
                    # create squares
                    squaremat[x][y].config(text="")
                    # add squares to matrix to change later
                    squaremat[x].append(square)
            change()

        # configure square colours based on light/dark mode
        def change():
            choice = mode.get()
            if choice == 1:
                for x in range(4):
                    for y in range(4):
                        num = matrix[x][y]
                        if num:
                            squaremat[x][y].config(text=str(num), bg=square_colour[num], fg=text_colour[num])
                        else:
                            squaremat[x][y].config(text="", bg="#cdc1b4")
            else:
                for x in range(4):
                    for y in range(4):
                        num = matrix[x][y]
                        if num:
                            squaremat[x][y].config(text=str(num), bg="#000000", fg="#333333")
                        else:
                            squaremat[x][y].config(text="", bg="#111111")
            # update points and highscore labels
            showpts.config(text=pts)
            showhigh.config(text=highscore)

        # create window to enter number of steps to undo
        def undoinput():
            win2 = Toplevel()
            win2.title("Undo")
            undolabel = Label(win2, text="Enter number of steps")
            steps = Entry(win2)
            undolabel.grid()
            steps.grid()

            # go back by entered number of steps - changes highscore, matrix, previous matrices
            def undo():
                nonlocal past_matrices, matrix, pts, highscore
                try:
                    if len(past_matrices) > int(steps.get()):
                        past_matrices = past_matrices[0:len(past_matrices)-int(steps.get())]
                        matrix = past_matrices[-1][0]
                        pts = past_matrices[-1][1]
                        highscore = past_matrices[-1][2]
                        # update colours
                        change()
                        win2.destroy()
                    else:
                        messagebox.showerror("Invalid value")
                except ValueError:
                    messagebox.showerror("Invalid value")

            submit = Button(win2, text="Submit", command=undo)
            submit.grid()
            win2.mainloop()
        
        # sets highscore to 0 in txt file, updates highscore variable
        def clearhigh():
            nonlocal highscore
            open('highscorefile.txt', 'w').write('0')
            open('highscorefile.txt').close()
            highscore = 0
            showhigh.config(text=highscore)
        
        undobutton = Button(win, text="Undo", font=("Clear Sans", 10, "bold"), bg="#bbada0", command=undoinput)
        undobutton.grid(row=6, column=3, padx=4, pady=4, sticky="news")

        # set movement keys
        movekeys = {
            "Up": game.up,
            "Down": game.down,
            "Left": game.left,
            "Right": game.right,
            "w": game.up,
            "s": game.down,
            "a": game.left,
            "d": game.right,
            "h": game.left,
            "j": game.down,
            "k": game.up,
            "l": game.right,
        }

        otherkeys = {
            "Escape": quit, # close all games
            "q": win.destroy, # close current game
            "n": newgame, # create new game
            "r": reset, # reset current game
            "c": clearhigh, # set high score to 0
            "u": undoinput, # undo moves
            "i": intro # get instructions for game
        }

        # tell program what to do after keyboard event occurs
        def keypress(event):
            nonlocal matrix, pts, highscore
            if event.keysym in movekeys:
                # if movement key pressed, test move on temporary matrix
                # if matrix is changed, move is valid
                future = movekeys[event.keysym](matrix)
                if future[0] != matrix:
                    matrix_pts = movekeys[event.keysym](matrix)
                    matrix = matrix_pts[0]
                    pts += matrix_pts[1]
                    # set highscore if points have exceeded highscore
                    if pts > highscore:
                        highscore = pts
                    # add matrix to history
                    past_matrices.append([matrix, pts, highscore])
                    matrix = game.addnum(matrix)
                    # update squares
                    change()
                # test for win/loss after move is made
                if game.state(matrix) == 'loss':
                    messagebox.showinfo(title="Uh-oh!", message="You lost!")
                elif game.state(matrix) == 'win':
                    messagebox.showinfo(title="Yay!", message="You won!")
            # run function if key pressed to perform other function
            elif event.keysym in otherkeys:
                if event.keysym != "Escape":
                    otherkeys[event.keysym]()
                else:
                    # escape quits game - highscore must be saved first
                    # write highscore to txt if higher than previous
                    open('highscorefile.txt', 'w').write(str(highscore))
                    open('highscorefile.txt').close()
                    # quit
                    otherkeys[event.keysym]()


        # create menubar in window
        menubar = Menu(win)
        game_menu = Menu(menubar, tearoff=False)
        game_menu.add_command(label='New game', command=newgame)
        game_menu.add_command(label='Reset', command=reset)
        game_menu.add_command(label='Clear high score', command=clearhigh)
        game_menu.add_separator()
        game_menu.add_command(label='Close', command=win.destroy)
        game_menu.add_command(label='Close all', command=win.destroy)
        menubar.add_cascade(label='Game', menu=game_menu)
        menubar.add_command(label="Help", command=intro)
        win.config(menu=menubar)

        # update squares with numbers before game starts
        change()

        # bind all keyboard events to keypress function
        win.bind("<Key>", keypress)
        # move current window to top
        # instructions opened before first window - first window must therefore be in focus
        win.focus_force()
        win.mainloop()

        # write highscore to txt on window destruction
        open('highscorefile.txt', 'w').write(str(highscore))
        open('highscorefile.txt').close()
    
    # show keybinds
    intro()
    # open first window
    newgame()

# run program
main()
