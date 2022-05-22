from tkinter import Tk, PhotoImage, Frame, IntVar, Label, Radiobutton, LEFT, DISABLED, NORMAL
from tkinter.font import Font
from tkmacosx import Button
import random

# ---------------------------- General Parameters ------------------------------- #
game_info = {}
btn_game_list = []
player_ai_active = False


# ---------------------------- Functions ------------------------------- #
# AI search for priority
def find_priority_pos(pos, value):
    # Find the available positions and divide them in priorities
    first_priority = []
    second_priority = []
    third_priority = []
    fourth_priority = []
    fifth_priority = []
    sixth_priority = []

    # 6th priority -> Human-tick has 1 tick and 2 empty ticks
    if value.count('O') == 1 and value.count('') == 2:
        for n in [i for i, x in enumerate(value) if x == ""]:
            sixth_priority.append(pos[n])
    # 5th priority -> AI-tick has 1 tick and Human-tick has 1 tick and 1 empty tick
    if value.count('X') == 1 and value.count('O') == 1 and value.count('') == 1:
        fifth_priority.append(pos[value.index('')])
    # 4ft priority -> All three positions are empty
    if value.count('') == 3:
        for n in pos:
            fourth_priority.append(n)
    # 3rd priority -> AI-ticks is one and the other two are empty
    if value.count('X') == 1 and value.count('O') == 2:
        for i in [i for i, x in enumerate(value) if x == ""]:
            third_priority.append(pos[i])
    # 2nd priority -> Human-ticks are two and the third one is empty
    if value.count('O') == 2 and value.count('') == 1:
        second_priority.append(pos[value.index('')])
    # 1st priority -> AI-ticks are two and the third one is empty
    if value.count('X') == 2 and value.count('') == 1:
        first_priority.append(pos[value.index('')])

    priority_list = [first_priority, second_priority, third_priority, fourth_priority, fifth_priority, sixth_priority]
    return priority_list


# Player AI Game Mode
def player_ai_mode():
    priority_list_final = []

    # Check the rows
    for i in [0, 3, 6]:
        pos = [i, i+1, i+2]
        value = []
        for n in pos:
            value.append(btn_game_list[n]["text"])
        priority_list_final.append(find_priority_pos(pos, value))

    # Check the columns
    for i in [0, 1, 2]:
        pos = [i, i+3, i+6]
        value = []
        for n in pos:
            value.append(btn_game_list[n]["text"])
        priority_list_final.append(find_priority_pos(pos, value))

    # Check the first cross
    pos = [0, 4, 8]
    value = []
    for n in pos:
        value.append(btn_game_list[n]["text"])
    priority_list_final.append(find_priority_pos(pos, value))

    # Check the second cross
    pos = [2, 4, 6]
    value = []
    for n in pos:
        value.append(btn_game_list[n]["text"])
    priority_list_final.append(find_priority_pos(pos, value))

    # Select AI choice
    ai_choices = []
    for i in range(6):
        for pr in priority_list_final:
            if len(pr[i]) > 0:
                for n in pr[i]:
                    ai_choices.append(n)
        if len(ai_choices) > 0:
            break

    ai_choice = random.choice(list(set(ai_choices)))
    btn_game_list[ai_choice]["font"] = font_tick
    btn_game_list[ai_choice]["bg"] = "#FD3A69"
    btn_game_list[ai_choice]["text"] = "X"

    game_info["status"][ai_choice] = "X"
    game_info["num_turn"] += 1
    check_win(2)


# Show the Player turn
def show_player_turn(turn):
    if turn % 2 == 0:
        btn_player1["bg"] = "white"
        btn_player2["bg"] = "green"
    else:
        btn_player1["bg"] = "green"
        btn_player2["bg"] = "white"


# Show Winning Cell
def show_win_cell(pos_list, player):
    i = 0
    for win_btn in btn_game_list:
        win_btn["bg"] = "white"
        if i not in pos_list:
            win_btn["state"] = DISABLED
            win_btn["bg"] = "white"
        if i in pos_list:
            win_btn["bg"] = "green"
        i += 1

    label = Label(window, text=f"Winner is Player {player}!", font=font_winner)
    label.grid(row=3, column=1)
    window.after(2000, destroy_widget, label)
    show_player_turn(game_info["num_turn"])


# Start Button
def bt_start_clicked():
    game_info["num_turn"] = 1
    game_info["status"] = ["0", "1", "2", "3", "4", "5", "6", "7", "8"]

    for btn in btn_game_list:
        btn["state"] = NORMAL
        btn["text"] = ""
        btn["bg"] = "white"

    show_player_turn(game_info["num_turn"])


# Destroy Winner Label
def destroy_widget(widget):
    widget.destroy()


# Check if the player won
def check_win(player):
    found_winner = False
    win_cell_poss = None

    # Check the rows
    for i in [0, 3, 6]:
        pos = [i, i+1, i+2]
        slice_pos = game_info["status"][i:i+3]
        result = all(element == slice_pos[0] for element in slice_pos)
        if result:
            found_winner = True
            win_cell_poss = pos
            break

    # Check the columns
    for i in [0, 1, 2]:
        pos = [i, i+3, i+6]
        slice_pos = game_info["status"][i::3]
        result = all(element == slice_pos[0] for element in slice_pos)
        if result:
            found_winner = True
            win_cell_poss = pos
            break

    # Check the cross -> first cross
    pos = [0, 4, 8]
    slice_pos = game_info["status"][0::4]
    result = all(element == slice_pos[0] for element in slice_pos)
    if result:
        found_winner = True
        win_cell_poss = pos

    # Check the cross -> second cross
    pos = [2, 4, 6]
    slice_pos = game_info["status"][2::2][0:3]
    result = all(element == slice_pos[0] for element in slice_pos)
    if result:
        found_winner = True
        win_cell_poss = pos

    # Winner Message
    if found_winner and win_cell_poss is not None:
        show_win_cell(win_cell_poss, player)


# Game Button
def btn_game_clicked(btn_click, btn_click_index):
    btn_click['state'] = 'disabled'
    btn_click["font"] = font_tick

    if game_info["num_turn"] % 2 != 0:
        btn_click["bg"] = "#FECD1A"
        btn_click["text"] = "O"
        game_info["status"][btn_click_index] = "O"
        check_win(1)

    else:
        btn_click["bg"] = "#FD3A69"
        btn_click["text"] = "X"
        game_info["status"][btn_click_index] = "X"
        check_win(2)

    game_info["num_turn"] += 1
    show_player_turn(game_info["num_turn"])

    # Player AI is active
    if radio_state.get() == 2:
        player_ai_mode()

    # Draw
    if game_info["num_turn"] == 10:
        label = Label(window, text="Draw!", font=font_winner)
        label.grid(row=3, column=1)
        window.after(2000, destroy_widget, label)
        btn_player1["bg"] = "white"
        btn_player2["bg"] = "white"


# ---------------------------- UI SETUP ------------------------------- #
# Window
window = Tk()
window.title("Tic - Tac - Toe")
window.minsize(width=467, height=510)

bg_img = PhotoImage(file="aldebaran.png")
background_label = Label(window, image=bg_img)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
font_tick = Font(family="Arial", size=50, weight="bold", slant="italic")
font_winner = Font(family="Verdana", size=40, weight="bold", slant="italic")

# Game settings -> Start Button & Radio-Buttons
frame_settings = Frame(window)
frame_settings.grid(row=0, column=1, padx=120, pady=10)

btn_start = Button(frame_settings, text="Start", command=bt_start_clicked)
btn_start.pack(side=LEFT)

radio_state = IntVar()
radio_btn_human = Radiobutton(frame_settings, text="vs. Human", value=1, variable=radio_state)
radio_btn_human.select()
radio_btn_human.pack(side=LEFT)

radio_btn_ai = Radiobutton(frame_settings, text="vs. AI", value=2, variable=radio_state)
radio_btn_ai.pack(side=LEFT)

# Players' Turn Buttons
frame_player_turn = Frame(window)
frame_player_turn.grid(row=1, column=1, padx=10, pady=10)

btn_player1 = Button(frame_player_turn, text="Player 1")
btn_player2 = Button(frame_player_turn, text="Player 2")

btn_player1['state'] = 'disabled'
btn_player2['state'] = 'disabled'

btn_player1.pack(side=LEFT)
btn_player2.pack(side=LEFT)

# Game Boxes
frame_game = Frame(window)
frame_game.grid(row=3, column=1, padx=10, pady=15)

index = 0
for r in [1, 2, 3]:
    for c in [1, 2, 3]:
        btn = Button(frame_game, height=125, width=125, text="", state=DISABLED)
        btn["command"] = lambda btn=btn, index=index: btn_game_clicked(btn, index)
        btn_game_list.append(btn)
        btn.grid(row=r, column=c)
        index += 1

window.mainloop()
