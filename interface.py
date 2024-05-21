import tkinter as tk
from tkinter import messagebox


class ChessInterface:
    def __init__(self, master):
        self.master = master
        self.master.title("Satranç Arayüzü")

        self.white_button = tk.Button(self.master, text="Beyaz Oynuyor", command=self.white_turn)
        self.white_button.pack(pady=10)

        self.black_button = tk.Button(self.master, text="Siyah Oynuyor", command=self.black_turn)
        self.black_button.pack(pady=10)

        self.best_move_button = tk.Button(self.master, text="En İyi Hamleyi Bul", command=self.find_best_move)
        self.best_move_button.pack(pady=10)

    def white_turn(self):
        messagebox.showinfo("Hamle Sırası", "Şu anda Beyaz'ın hamle sırası")

    def black_turn(self):
        messagebox.showinfo("Hamle Sırası", "Şu anda Siyah'ın hamle sırası")

    def find_best_move(self):
        messagebox.showinfo("En İyi Hamle", "En iyi hamle bulunuyor...")  # Buraya en iyi hamle hesaplanması eklenebilir


def main():
    root = tk.Tk()
    app = ChessInterface(root)
    root.mainloop()


if __name__ == "__main__":
    main()
