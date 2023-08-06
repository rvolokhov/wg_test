from tkinter import *
import random
from tkinter.messagebox import showinfo
from Node import Node


columns_count = 20
rows_count = 10
# the more the ratio the less land cells are on the map, 3 means 30% probability of land cells
random_ratio = 3
player_cell: Node = None
target_cell: Node = None
square_side = 50
maze = [[]]
maze_steps: [[]]
# instance of tkinter
root = Tk()
root.title("test task 3")
# creating canvas
canvas = Canvas(width=columns_count * square_side, height=rows_count * square_side, bg="white")
# stores found target node
foundNode: Node = None
# stores all points leads from player node to target node
min_path = []


# mouse left button callback func
def click_mlb(event):
    global player_cell, target_cell, min_path, foundNode
    player_x = event.x // 50
    player_y = event.y // 50
    if maze[player_y][player_x] == 1:
        showinfo(title="Warning", message="You should click on water.")
    else:
        player_cell = Node(player_x, player_y)
        foundNode = None
        generate_maze_steps()
        draw()
        min_path = []
        if target_cell:
            find_path()
        init()


# mouse right button callback func
def click_mrb(event):
    global player_cell, target_cell, min_path, foundNode
    target_x = event.x // 50
    target_y = event.y // 50
    if maze[target_y][target_x] == 1:
        showinfo(title="Warning", message="You should click on water.")
    else:
        target_cell = Node(target_x, target_y)
        foundNode = None
        draw()
        min_path = []
        if player_cell:
            find_path()
        init()


def generate_map():
    global maze
    maze = []
    for i in range(rows_count):
        col = []
        for j in range(columns_count):
            a = random.randint(0, random_ratio-1)
            if a == 0:
                col.append(1)
            else:
                col.append(0)
        maze.append(col)


# generate auxiliary list of lists consists of number of steps, cell of Player marked as -1
def generate_maze_steps():
    global maze_steps
    maze_steps = []
    for i in range(rows_count):
        col = []
        for j in range(columns_count):
            col.append(0)
        maze_steps.append(col)
    maze_steps[player_cell.pos_y][player_cell.pos_x] = -1


def init():
    canvas.pack()
    draw()
    root.mainloop()


def draw():
    canvas.delete("all")
    for i in range(0, columns_count):
        for j in range(0, rows_count):
            color = "sienna"
            if maze[j][i] == 0:
                color = "skyblue"
            canvas.create_rectangle(i * square_side, j * square_side, i * square_side + square_side, j * square_side + square_side, fill=color)
    if player_cell:
        canvas.create_rectangle(player_cell.pos_x * square_side + 10, player_cell.pos_y * square_side + 10, player_cell.pos_x * square_side + 40, player_cell.pos_y * square_side + 40, fill="black")
    if target_cell:
        canvas.create_rectangle(target_cell.pos_x * square_side + 10, target_cell.pos_y * square_side + 10, target_cell.pos_x * square_side + 40, target_cell.pos_y * square_side + 40, fill="gray")
    if len(min_path) > 0:
        for i in range(len(min_path) - 1):
            canvas.create_line(min_path[i].pos_x * 50 + 25, min_path[i].pos_y * 50 + 25, min_path[i + 1].pos_x * 50 + 25, min_path[i + 1].pos_y * 50 + 25, fill="black", width=2)


def find_path():
    global maze_steps
    current_node = Node(player_cell.pos_x, player_cell.pos_y)
    # nullify maze_steps
    generate_maze_steps()
    check_neighbours(current_node, 1)
    if foundNode:
        backtrack(foundNode)
    else:
        showinfo(title="Warning", message="Can't reach. Path not found.")
    draw()


def backtrack(current_node: Node) -> int:
    if current_node:
        min_path.append(Node(current_node.pos_x, current_node.pos_y))
        if maze_steps[current_node.pos_y][current_node.pos_x] == -1:
            return 0
        steps_count = maze_steps[current_node.pos_y][current_node.pos_x]
        if current_node.pos_y + 1 < rows_count:
            if maze_steps[current_node.pos_y + 1][current_node.pos_x] < steps_count and maze_steps[current_node.pos_y + 1][current_node.pos_x] != 0:
                backtrack(Node(current_node.pos_x, current_node.pos_y + 1))
                return 0
        if current_node.pos_y - 1 >= 0:
            if maze_steps[current_node.pos_y - 1][current_node.pos_x] < steps_count and maze_steps[current_node.pos_y - 1][current_node.pos_x] != 0:
                backtrack(Node(current_node.pos_x, current_node.pos_y - 1))
                return 0
        if current_node.pos_x + 1 < columns_count:
            if maze_steps[current_node.pos_y][current_node.pos_x + 1] < steps_count and maze_steps[current_node.pos_y][current_node.pos_x + 1] != 0:
                backtrack(Node(current_node.pos_x + 1, current_node.pos_y))
                return 0
        if current_node.pos_x - 1 >= 0:
            if maze_steps[current_node.pos_y][current_node.pos_x - 1] < steps_count and maze_steps[current_node.pos_y][current_node.pos_x - 1] != 0:
                backtrack(Node(current_node.pos_x - 1, current_node.pos_y))
                return 0
    else:
        raise Exception("node for backtracking is None")


def check_neighbours(current_node: Node, steps_count) -> int:
    global foundNode

    # check if we found target point
    if current_node.pos_x == target_cell.pos_x and current_node.pos_y == target_cell.pos_y:
        foundNode = current_node
        return 0

    # check right neighbour
    if current_node.pos_x < columns_count - 1:
        if maze[current_node.pos_y][current_node.pos_x + 1] == 0:
            if maze_steps[current_node.pos_y][current_node.pos_x + 1] == 0 or maze_steps[current_node.pos_y][current_node.pos_x + 1] > steps_count:
                maze_steps[current_node.pos_y][current_node.pos_x + 1] = steps_count
                check_neighbours(Node(current_node.pos_x + 1, current_node.pos_y), steps_count + 1)

    # check left neighbour
    if current_node.pos_x >= 1:
        if maze[current_node.pos_y][current_node.pos_x - 1] == 0:
            if maze_steps[current_node.pos_y][current_node.pos_x - 1] == 0 or maze_steps[current_node.pos_y][current_node.pos_x - 1] > steps_count:
                maze_steps[current_node.pos_y][current_node.pos_x - 1] = steps_count
                check_neighbours(Node(current_node.pos_x - 1, current_node.pos_y), steps_count + 1)

    # check bottom neighbour
    if current_node.pos_y < rows_count - 1:
        if maze[current_node.pos_y + 1][current_node.pos_x] == 0:
            if maze_steps[current_node.pos_y + 1][current_node.pos_x] == 0 or maze_steps[current_node.pos_y + 1][current_node.pos_x] > steps_count:
                maze_steps[current_node.pos_y + 1][current_node.pos_x] = steps_count
                check_neighbours(Node(current_node.pos_x, current_node.pos_y + 1), steps_count + 1)

    # check top neighbour
    if current_node.pos_y >= 1:
        if maze[current_node.pos_y - 1][current_node.pos_x] == 0:
            if maze_steps[current_node.pos_y - 1][current_node.pos_x] == 0 or maze_steps[current_node.pos_y - 1][current_node.pos_x] > steps_count:
                maze_steps[current_node.pos_y - 1][current_node.pos_x] = steps_count
                check_neighbours(Node(current_node.pos_x, current_node.pos_y - 1), steps_count + 1)


if __name__ == "__main__":
    mouse_left_button = "<Button-1>"
    mouse_right_button = "<Button-3>"
    # bind left mouse button click
    canvas.bind(mouse_left_button, click_mlb)
    # bind right mouse button click
    canvas.bind(mouse_right_button, click_mrb)
    generate_map()
    init()
