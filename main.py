import tkinter as tk
from tkinter import ttk
import threading
import subprocess

def search():
    """検索を実行する関数
    """
    keyword = entry.get()
    command = f'sortgs "{keyword}"'

    # オプションの追加
    if sortby_var.get():
        command += f' --sortby "{sortby_entry.get()}"'
    if nresults_var.get():
        command += f' --nresults {nresults_entry.get()}'
    if csvpath_var.get():
        command += f' --csvpath "{csvpath_entry.get()}"'
    if notsavecsv_var.get():
        command += ' --notsavecsv'
    if plotresults_var.get():
        command += ' --plotresults'
    if startyear_var.get():
        command += f' --startyear {startyear_entry.get()}'
    if endyear_var.get():
        command += f' --endyear {endyear_entry.get()}'
    if debug_var.get():
        command += ' --debug'
    
    # ボタンを無効化
    button.config(state=tk.DISABLED)
    
    # 処理中であることを示すラベルを表示
    status_label.config(text="検索中...")
    
    # バックグラウンドでコマンドを実行
    thread = threading.Thread(target=run_command, args=(command,))
    thread.start()

def run_command(command: str):
    """sortgsのコマンドを実行する関数

    Args:
        command (str): 実行したいコマンド
    """
    subprocess.run(command, shell=True)
    
    # 処理が完了したらラベルを更新し，ボタンを有効化
    status_label.config(text="検索完了")
    button.config(state=tk.NORMAL)

    # 入力欄を空にする
    entry.delete(0, tk.END)

def show_help():
    help_window = tk.Toplevel(root)
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

if __name__ == '__main__':
    # メインウィンドウの作成
    root = tk.Tk()
    root.title("Google Scholar Sorter")

    # エントリーウィジェット（文字入力エリア）の作成
    entry = tk.Entry(root, width=50)
    entry.grid(row=0, column=0, padx=10, pady=10)

    # 検索ボタンの作成
    button = tk.Button(root, text="検索", command=search)
    button.grid(row=0, column=1, padx=10, pady=10, columnspan=2, sticky='ew')

    # オプションのチェックボックスとエントリーフィールドの作成
    sortby_var = tk.BooleanVar()
    sortby_check = tk.Checkbutton(root, text="Sort by", variable=sortby_var)
    sortby_check.grid(row=1, column=1, sticky='w')
    sortby_entry = tk.Entry(root, width=50)
    sortby_entry.grid(row=1, column=0, padx=10, pady=5)

    nresults_var = tk.BooleanVar()
    nresults_check = tk.Checkbutton(root, text="Number of results", variable=nresults_var)
    nresults_check.grid(row=2, column=1, sticky='w')
    nresults_entry = tk.Entry(root, width=50)
    nresults_entry.grid(row=2, column=0, padx=10, pady=5)

    csvpath_var = tk.BooleanVar()
    csvpath_check = tk.Checkbutton(root, text="CSV path", variable=csvpath_var)
    csvpath_check.grid(row=3, column=1, sticky='w')
    csvpath_entry = tk.Entry(root, width=50)
    csvpath_entry.grid(row=3, column=0, padx=10, pady=5)

    notsavecsv_var = tk.BooleanVar()
    notsavecsv_check = tk.Checkbutton(root, text="Do not save CSV", variable=notsavecsv_var)
    notsavecsv_check.grid(row=4, column=1, sticky='w')

    plotresults_var = tk.BooleanVar()
    plotresults_check = tk.Checkbutton(root, text="Plot results", variable=plotresults_var)
    plotresults_check.grid(row=5, column=1, sticky='w')

    startyear_var = tk.BooleanVar()
    startyear_check = tk.Checkbutton(root, text="Start year", variable=startyear_var)
    startyear_check.grid(row=6, column=1, sticky='w')
    startyear_entry = tk.Entry(root, width=50)
    startyear_entry.grid(row=6, column=0, padx=10, pady=5)

    endyear_var = tk.BooleanVar()
    endyear_check = tk.Checkbutton(root, text="End year", variable=endyear_var)
    endyear_check.grid(row=7, column=1, sticky='w')
    endyear_entry = tk.Entry(root, width=50)
    endyear_entry.grid(row=7, column=0, padx=10, pady=5)

    debug_var = tk.BooleanVar()
    debug_check = tk.Checkbutton(root, text="Debug mode", variable=debug_var)
    debug_check.grid(row=8, column=1, sticky='w')

    # ヘルプボタンの作成
    help_button = tk.Button(root, text="ヘルプ", command=show_help)
    help_button.grid(row=9, column=0, padx=10, pady=10)

    # ステータスラベルの作成
    status_label = ttk.Label(root, text="")
    status_label.grid(row=10, column=0, columnspan=2, padx=10, pady=10)

    # メインループの開始
    root.mainloop()
