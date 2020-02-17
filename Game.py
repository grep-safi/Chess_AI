import tkinter as tk


class Game:
    def __init__(self, master, canvas):
        self.master = master
        self.cv = canvas

        self.bg_image = tk.PhotoImage(file="images/chess_bg.png")

        # Event listeners response
        self.moves = []
        self.circles = []
        self.piece_clicked = False
        self.current_piece = None

        # Binding to get click events
        self.master.bind("<Button-1>", self.bindingFunction)

        self.white_turn = True
        self.piece_clicked = False

    def bindingFunction(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    root.title('Chess AI')

    # 8x8 Grid --> 800px x 800px screen
    cv = tk.Canvas(root, width=800, height=800)
    game = Game(root, cv)

    root.mainloop()
