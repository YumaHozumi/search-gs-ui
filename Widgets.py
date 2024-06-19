import tkinter as tk
from tkinter import ttk
import threading
import subprocess
import os

class Widgets:
    def __init__(self, root):
        self.root = root
        self.create_widgets()

    def create_widgets(self):
        # エントリーウィジェット（文字入力エリア）の作成
        self.entry = tk.Entry(self.root, width=50)
        self.entry.insert(0, "")  # 追加
        self.entry.grid(row=0, column=0, padx=10, pady=10)

        # 検索ボタンの作成
        self.button = tk.Button(self.root, text="検索", command=self.search)
        self.button.grid(row=0, column=1, padx=10, pady=10, columnspan=2, sticky='ew')

        # オプションのチェックボックスとエントリーフィールドの作成
        self.sortby_var = tk.BooleanVar()
        self.sortby_check = tk.Checkbutton(self.root, text="Sort by cit/year", variable=self.sortby_var)
        self.sortby_check.grid(row=1, column=1, sticky='w')

        self.nresults_var = tk.BooleanVar()
        self.nresults_check = tk.Checkbutton(self.root, text="Number of results", variable=self.nresults_var)
        self.nresults_check.grid(row=2, column=1, sticky='w')
        self.nresults_entry = tk.Entry(self.root, width=50)
        self.nresults_entry.insert(0, "")  # 追加
        self.nresults_entry.grid(row=2, column=0, padx=10, pady=5)

        self.csvpath_var = tk.BooleanVar()
        self.csvpath_check = tk.Checkbutton(self.root, text="CSV path", variable=self.csvpath_var)
        self.csvpath_check.grid(row=3, column=1, sticky='w')
        self.csvpath_entry = tk.Entry(self.root, width=50)
        self.csvpath_entry.insert(0, "")  # 追加
        self.csvpath_entry.grid(row=3, column=0, padx=10, pady=5)

        self.notsavecsv_var = tk.BooleanVar()
        self.notsavecsv_check = tk.Checkbutton(self.root, text="Do not save CSV", variable=self.notsavecsv_var)
        self.notsavecsv_check.grid(row=4, column=1, sticky='w')

        self.plotresults_var = tk.BooleanVar()
        self.plotresults_check = tk.Checkbutton(self.root, text="Plot results", variable=self.plotresults_var)
        self.plotresults_check.grid(row=5, column=1, sticky='w')

        self.startyear_var = tk.BooleanVar()
        self.startyear_check = tk.Checkbutton(self.root, text="Start year", variable=self.startyear_var)
        self.startyear_check.grid(row=6, column=1, sticky='w')
        self.startyear_entry = tk.Entry(self.root, width=50)
        self.startyear_entry.insert(0, "")  # 追加
        self.startyear_entry.grid(row=6, column=0, padx=10, pady=5)

        self.endyear_var = tk.BooleanVar()
        self.endyear_check = tk.Checkbutton(self.root, text="End year", variable=self.endyear_var)
        self.endyear_check.grid(row=7, column=1, sticky='w')
        self.endyear_entry = tk.Entry(self.root, width=50)
        self.endyear_entry.insert(0, "")  # 追加
        self.endyear_entry.grid(row=7, column=0, padx=10, pady=5)

        self.debug_var = tk.BooleanVar()
        self.debug_check = tk.Checkbutton(self.root, text="Debug mode", variable=self.debug_var)
        self.debug_check.grid(row=8, column=1, sticky='w')

        # ヘルプボタンの作成
        self.help_button = tk.Button(self.root, text="ヘルプ", command=self.show_help)
        self.help_button.grid(row=9, column=0, padx=10, pady=10)

        # ステータスラベルの作成
        self.status_label = ttk.Label(self.root, text="")
        self.status_label.grid(row=10, column=0, columnspan=2, padx=10, pady=10)

    def search(self):
        """検索を実行する関数
        """
        keyword = self.entry.get()
        command = f'sortgs "{keyword}"'

        # バリデーションチェック
        if self.nresults_var.get():
            if not self.nresults_entry.get().isdigit():
                self.status_label.config(text="数値を入力してください（Number of results）", foreground="red")
                return
            command += f' --nresults {self.nresults_entry.get()}'
        
        if self.csvpath_var.get():
            if not os.path.isdir(self.csvpath_entry.get()):
                self.status_label.config(text="存在するディレクトリを入力してください（CSV path）", foreground="red")
                return
            command += f' --csvpath "{self.csvpath_entry.get()}"'
        
        if self.startyear_var.get():
            if not self.startyear_entry.get().isdigit():
                self.status_label.config(text="数値を入力してください（Start year）", foreground="red")
                return
            command += f' --startyear {self.startyear_entry.get()}'
        
        if self.endyear_var.get():
            if not self.endyear_entry.get().isdigit():
                self.status_label.config(text="数値を入力してください（End year）", foreground="red")
                return
            command += f' --endyear {self.endyear_entry.get()}'
        
        if self.sortby_var.get():
            command += ' --sortby "cit/year"'
        if self.notsavecsv_var.get():
            command += ' --notsavecsv'
        if self.plotresults_var.get():
            command += ' --plotresults'
        if self.debug_var.get():
            command += ' --debug'
        
        # ボタンを無効化
        self.button.config(state=tk.DISABLED)
        
        # 処理中であることを示すラベルを表示
        self.status_label.config(text="検索中...", foreground="black")
        
        # バックグラウンドでコマンドを実行
        thread = threading.Thread(target=self.run_command, args=(command,))
        thread.start()

    def run_command(self, command):
        """sortgsのコマンドを実行する関数

        Args:
            command (str): 実行したいコマンド
        """
        subprocess.run(command, shell=True)
        
        # 処理が完了したらラベルを更新し，ボタンを有効化
        self.status_label.config(text="検索完了", foreground="black")
        self.button.config(state=tk.NORMAL)
        
        # 入力欄を空にする
        self.entry.delete(0, tk.END)

    def show_help(self):
        help_window = tk.Toplevel(self.root)
        help_window.title("ヘルプ")
        
        help_text = """
    1. デフォルト検索:
    sortgs "machine learning"
    このコマンドは「machine learning」に関連する上位100件の結果を検索し、CSVファイルとして保存します。

    2. 年ごとの引用数でソート:
    sortgs "machine learning" --sortby "cit/year"
    「machine learning」を検索し、年ごとの引用数でソートします。

    3. 日付範囲を指定:
    sortgs "machine learning" --startyear 2005 --endyear 2015
    2005年から2015年までの論文を検索します。

    4. 正確なキーワードで検索:
    sortgs "'machine learning'"
    正確なキーワード「machine learning」を検索します。

    5. 特定のパスに結果を保存:
    sortgs 'neural networks' --csvpath './examples/'
    結果を「examples」というサブフォルダに保存します。

    6. 複数のキーワード:
    sortgs "'deep learning' OR 'neural networks' OR 'machine learning'" --sortby "cit/year"
    複数のキーワードを検索し、年ごとの引用数でソートします。
"""
        
        help_label = tk.Label(help_window, text=help_text, justify=tk.LEFT)
        help_label.pack(padx=10, pady=10)
