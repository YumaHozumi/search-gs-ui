import unittest
import tkinter as tk
from tkinter import ttk
import threading
import subprocess
import os

# テスト対象のクラスをインポート
from main import Widgets

class TestGoogleScholarSorter(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.widgets = Widgets(self.root)
        self.entry = self.widgets.entry
        self.button = self.widgets.button
        self.status_label = self.widgets.status_label
        self.sortby_var = self.widgets.sortby_var
        self.sortby_entry = self.widgets.sortby_entry
        self.nresults_var = self.widgets.nresults_var
        self.nresults_entry = self.widgets.nresults_entry
        self.csvpath_var = self.widgets.csvpath_var
        self.csvpath_entry = self.widgets.csvpath_entry
        self.notsavecsv_var = self.widgets.notsavecsv_var
        self.plotresults_var = self.widgets.plotresults_var
        self.startyear_var = self.widgets.startyear_var
        self.startyear_entry = self.widgets.startyear_entry
        self.endyear_var = self.widgets.endyear_var
        self.endyear_entry = self.widgets.endyear_entry
        self.debug_var = self.widgets.debug_var

    def tearDown(self):
        self.root.destroy()

    def test_nresults_validation(self):
        self.nresults_var.set(True)
        self.nresults_entry.insert(0, "abc")
        self.widgets.search()
        self.assertEqual(self.status_label.cget("text"), "数値を入力してください（Number of results）")
        self.assertEqual(self.status_label.cget("foreground"), "red")

    def test_csvpath_validation(self):
        self.csvpath_var.set(True)
        self.csvpath_entry.insert(0, "/non/existent/path")
        self.widgets.search()
        self.assertEqual(self.status_label.cget("text"), "存在するディレクトリを入力してください（CSV path）")
        self.assertEqual(self.status_label.cget("foreground"), "red")

    def test_startyear_validation(self):
        self.startyear_var.set(True)
        self.startyear_entry.insert(0, "abc")
        self.widgets.search()
        self.assertEqual(self.status_label.cget("text"), "数値を入力してください（Start year）")
        self.assertEqual(self.status_label.cget("foreground"), "red")

    def test_endyear_validation(self):
        self.endyear_var.set(True)
        self.endyear_entry.insert(0, "abc")
        self.widgets.search()
        self.assertEqual(self.status_label.cget("text"), "数値を入力してください（End year）")
        self.assertEqual(self.status_label.cget("foreground"), "red")

    def test_valid_search(self):
        self.entry.insert(0, "machine learning")
        self.nresults_var.set(True)
        self.nresults_entry.insert(0, "10")
        self.csvpath_var.set(True)
        self.csvpath_entry.insert(0, ".")
        self.startyear_var.set(True)
        self.startyear_entry.insert(0, "2000")
        self.endyear_var.set(True)
        self.endyear_entry.insert(0, "2020")
        self.widgets.search()
        self.assertEqual(self.status_label.cget("text"), "検索中...")
        self.assertEqual(self.status_label.cget("foreground"), "black")

if __name__ == "__main__":
    unittest.main()
