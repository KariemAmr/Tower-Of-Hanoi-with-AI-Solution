import tkinter as tk
from collections import deque

class TowersOfHanoi:
    def __init__(self, master, num_discs):
        self.master = master
        self.master.title("Towers of Hanoi")

        self.num_discs = num_discs
        self.initial_state = (tuple(range(num_discs, 0, -1)), (), ())
        self.goal_state = ((), (), tuple(range(num_discs, 0, -1)))

        self.canvas = tk.Canvas(self.master, width=450, height=300, bg="white")
        self.canvas.pack()

        self.draw_towers()
        self.create_buttons()

    def draw_towers(self):
        self.canvas.delete("all")

        for i in range(3):
            x = i * 150 + 75
            y = 250
            self.canvas.create_rectangle(x - 50, y, x + 50, y - 200, fill="gray", outline="black")

            for j, disc in enumerate(self.initial_state[i]):
                disc_width = disc * 20
                self.canvas.create_rectangle(x - disc_width / 2, y - j * 20, x + disc_width / 2, y - (j + 1) * 20,
                                             fill="red", outline="black")

    def create_buttons(self):
        tk.Button(self.master, text="Solve", command=self.solve).pack()

    def move_disc(self, from_tower, to_tower, state):
        state = list(state)
        if state[from_tower]:
            disc = state[from_tower][-1]
            if not state[to_tower] or disc < state[to_tower][-1]:
                state[from_tower] = state[from_tower][:-1]
                state[to_tower] += (disc,)
                return tuple(state)
        return None

    def is_goal_state(self, state):
        return state == self.goal_state

    def get_successors(self, state):
        successors = []
        for from_tower in range(3):
            for to_tower in range(3):
                if from_tower != to_tower:
                    successor_state = self.move_disc(from_tower, to_tower, state)
                    if successor_state:
                        successors.append((successor_state, (from_tower, to_tower)))
        return successors

    def bfs(self):
        queue = deque([(self.initial_state, [])])
        visited = set([self.initial_state])

        while queue:
            state, path = queue.popleft()
            if self.is_goal_state(state):
                return path
            for successor_state, move in self.get_successors(state):
                if successor_state not in visited:
                    queue.append((successor_state, path + [move]))
                    visited.add(successor_state)
        return None

    def animate_solution(self, solution):
        if solution:
            for from_tower, to_tower in solution:
                self.move_disc_and_redraw(from_tower, to_tower)
                self.master.update()  # Update the GUI to show the move
                self.master.after(1000)
            self.canvas.create_text(230, 150, text="The Towers of Hanoi puzzle has been solved!",
                                    font=("Helvetica", 14), fill="green")
        else:
            self.canvas.create_text(200, 150, text="Solution Not Found!",
                                    font=("Helvetica", 14), fill="green")

    def move_disc_and_redraw(self, from_tower, to_tower):
        move = self.move_disc(from_tower, to_tower, self.initial_state)
        if move:
            self.initial_state = move
            self.draw_towers()

    def solve(self):
        solution = self.bfs()
        self.animate_solution(solution)

if __name__ == "__main__":
    root = tk.Tk()
    hanoi_game = TowersOfHanoi(root, num_discs = 4)
    root.mainloop()