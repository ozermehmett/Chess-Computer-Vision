import tkinter as tk
from tkinter import messagebox, simpledialog
from chess_engine_ozerm import ChessEngine
from multiprocessing import Process, Queue
import ChessAI
from piece_detector import PieceDetector
from resize_board import ChessResize
import torch
import pyautogui
from PIL import Image, ImageTk

device_type = ('cuda' if torch.cuda.is_available() else 'cpu')
resizer = ChessResize('models/chess_board_last.pt', device_type)
piece_detector = PieceDetector('models/chess_last_tas.pt', device_type)


class ChessInterface:
    def __init__(self, master):
        self.master = master
        self.master.title("Chess Interface")
        self.master.geometry("300x550")  # Larger dimensions

        self.game_state = ChessEngine.GameState()

        self.white_button = tk.Button(self.master, text="White's Turn", command=self.white_turn)
        self.white_button.pack(pady=5)

        self.black_button = tk.Button(self.master, text="Black's Turn", command=self.black_turn)
        self.black_button.pack(pady=5)

        self.best_move_button = tk.Button(self.master, text="Find Best Move", command=self.find_best_move)
        self.best_move_button.pack(pady=5)

        self.x_left_label = tk.Label(self.master, text="Left X:")
        self.x_left_label.pack(pady=5)
        self.x_left_slider = tk.Scale(self.master, from_=0, to=1920, orient=tk.HORIZONTAL)
        self.x_left_slider.pack(pady=5)

        self.y_top_label = tk.Label(self.master, text="Top Y:")
        self.y_top_label.pack(pady=5)
        self.y_top_slider = tk.Scale(self.master, from_=0, to=1080, orient=tk.HORIZONTAL)
        self.y_top_slider.pack(pady=5)

        self.x_right_label = tk.Label(self.master, text="Right X:")
        self.x_right_label.pack(pady=5)
        self.x_right_slider = tk.Scale(self.master, from_=0, to=1920, orient=tk.HORIZONTAL)
        self.x_right_slider.pack(pady=5)

        self.y_bottom_label = tk.Label(self.master, text="Bottom Y:")
        self.y_bottom_label.pack(pady=5)
        self.y_bottom_slider = tk.Scale(self.master, from_=0, to=1080, orient=tk.HORIZONTAL)
        self.y_bottom_slider.pack(pady=5)

    def white_turn(self):
        self.game_state.white_to_move = True
        messagebox.showinfo("Turn", "It's White's turn now")

    def black_turn(self):
        self.game_state.white_to_move = False
        messagebox.showinfo("Turn", "It's Black's turn now")

    def find_best_move(self):
        x_left = self.x_left_slider.get()
        y_top = self.y_top_slider.get()
        x_right = self.x_right_slider.get()
        y_bottom = self.y_bottom_slider.get()

        if x_left >= x_right or y_top >= y_bottom:
            messagebox.showerror("Error", "Invalid coordinates. Please make sure Left X < Right X and Top Y < Bottom Y.")
            return

        screenshot = pyautogui.screenshot()
        screenshot_pil = Image.frombytes('RGB', screenshot.size, screenshot.tobytes())
        selected_area = screenshot_pil.crop((x_left, y_top, x_right, y_bottom))

        # selected_area.show()

        selected_area.save("inputs/input.png")

        output_frame = resizer.resize('inputs/input.png')
        board = piece_detector.detect_piece(output_frame)

        self.game_state.board = board
        valid_moves = self.game_state.get_valid_moves()

        return_queue = Queue()
        move_finder_process = Process(target=ChessAI.findBestMove, args=(self.game_state, valid_moves, return_queue))
        move_finder_process.start()

        move_finder_process.join()

        best_move = return_queue.get()

        messagebox.showinfo("Best Move", f"Best move: {best_move}")


def main():
    root = tk.Tk()
    app = ChessInterface(root)
    root.mainloop()


if __name__ == "__main__":
    main()
