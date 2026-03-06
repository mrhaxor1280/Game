# -----------------------------
# FAHAD'S RACE TO 16 GAME
# -----------------------------

players = ["Ali", "Sara", "Ahmed", "Ayesha"]
positions = [0,0,0,0]

turn = 0
round_count = 1

# 8 papers in jar
jar = [
    2, 3, 4, 5,   # forward papers
    2, 3,         # more forward
    -1, -2        # backward papers
]

random.shuffle(jar)

def draw_board():
    canvas.delete("all")

    center_x = 500
    center_y = 350

    # draw cross paths
    for i in range(1,17):

        canvas.create_rectangle(center_x-25, center_y-(i*25), center_x+25, center_y-(i*25)+50, fill="white")
        canvas.create_text(center_x, center_y-(i*25)+25, text=i)

        canvas.create_rectangle(center_x-25, center_y+(i*25), center_x+25, center_y+(i*25)+50, fill="white")
        canvas.create_text(center_x, center_y+(i*25)+25, text=i)

        canvas.create_rectangle(center_x-(i*25), center_y-25, center_x-(i*25)+50, center_y+25, fill="white")
        canvas.create_text(center_x-(i*25)+25, center_y, text=i)

        canvas.create_rectangle(center_x+(i*25), center_y-25, center_x+(i*25)+50, center_y+25, fill="white")
        canvas.create_text(center_x+(i*25)+25, center_y, text=i)

    draw_players()

def draw_players():

    colors = ["red","blue","green","yellow"]

    for i in range(4):
        pos = positions[i]

        x = 500
        y = 350 - (pos*25)

        canvas.create_oval(x-10,y-10,x+10,y+10,fill=colors[i])
        canvas.create_text(x,y-15,text=players[i])


def play_turn():

    global turn

    player = turn % 4

    # player with jar paper
    if turn % 4 == player:

        if len(jar) > 0:
            move = jar.pop()

        else:
            move = 1

    else:
        move = 1

    positions[player] += move

    if positions[player] < 0:
        positions[player] = 0

    if positions[player] >= 16:
        messagebox.showinfo("Winner", players[player] + " Wins!")
        root.quit()

    turn += 1

    draw_board()


canvas = Canvas(root,width=1000,height=700,bg="darkgreen")
canvas.pack()

btn = Button(root,text="Next Turn",command=play_turn)
btn.pack()

draw_board()
