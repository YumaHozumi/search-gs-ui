# main.py
import tkinter as tk
from Widgets import Widgets

if __name__ == '__main__':
    # メインウィンドウの作成
    root = tk.Tk()
    root.title("Google Scholar Sorter")

    # ウィジェットの作成
    app = Widgets(root)

    # メインループの開始
    root.mainloop()
