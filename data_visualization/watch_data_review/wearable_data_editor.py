import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import filedialog
import tkinter.scrolledtext as scrolledtext
import tkinter.messagebox as messagebox

class DataVisualizer:
    def __init__(self, master):
        self.master = master
        self.file_index = 0
        self.files = self.get_files()
        self.readme_content = self.get_readme_content()

        self.figure = plt.Figure(figsize=(6, 5), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=master)
        self.canvas.get_tk_widget().grid(row=0, column=0, columnspan=2)

        self.text_area = Text(master, width=30, height=10)
        self.text_area.insert(INSERT, self.readme_content)
        self.text_area.grid(row=0, column=2)  # column updated

        self.back_button = Button(master, text="Back", command=self.prev_file)
        self.back_button.grid(row=1, column=0)

        self.next_button = Button(master, text="Next", command=self.next_file)
        self.next_button.grid(row=1, column=1)

        self.delete_button = Button(master, text="Delete", command=self.delete_file)
        self.delete_button.grid(row=1, column=2)

        self.edit_button = Button(master, text="Edit README", command=self.edit_readme)
        self.edit_button.grid(row=2, column=2)

        self.home_button = Button(master, text="Home", command=self.go_home)
        self.home_button.grid(row=3, column=1)  # row와 column은 필요에 따라 조정 가능

        # 총 파일 수와 현재 파일 인덱스를 표시하기 위한 Label 추가
        self.file_status = StringVar()
        self.file_status_label = Label(master, textvariable=self.file_status)
        self.file_status_label.grid(row=2, column=0, columnspan=2)
        self.update_file_status()


        self.plot_data(self.files[self.file_index])

    def go_home(self):
        self.files = self.get_files()  # 폴더 선택 창 띄우고, 새로운 파일 목록 얻기
        self.file_index = 0  # 파일 인덱스 초기화
        if self.files:  # 새로운 폴더에 파일이 있으면 첫 번째 파일 표시
            self.plot_data(self.files[self.file_index])
            self.readme_content = self.get_readme_content()  # README 내용 업데이트
            self.update_readme_content()  # Text 위젯 내용 업데이트
        else:  # 새로운 폴더에 파일이 없으면 알림 메시지 표시
            messagebox.showinfo("Info", "No .txt files found in the selected directory.")

    def update_file_status(self):
        # 현재 파일 인덱스와 총 파일 수를 업데이트하는 함수
        self.file_status.set(f"{self.file_index + 1}/{len(self.files)}")

    def get_files(self):
        global directory
        directory = filedialog.askdirectory()
        print(directory)
        files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".txt") and not f.endswith("readme.txt")]
        return sorted(files)

    def get_readme_content(self):
        global readme_file
        readme_file = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith("readme.txt")]
        with open(readme_file[0], "r") as file:
            content = file.read()
        return content

    def update_readme_content(self):
        """Text 위젯의 내용을 업데이트하는 메서드"""
        self.text_area.delete(1.0, END)  # 현재 내용 삭제
        self.text_area.insert(INSERT, self.readme_content)  # 새로운 README 내용 삽입

    def plot_data(self, filename):
        data = pd.read_csv(filename, sep="\t", header=None)
        self.ax.cla()
        self.ax.plot(data.iloc[:, 2:10])
        self.canvas.draw()
        self.update_file_status()

    def next_file(self):
        self.file_index += 1
        if self.file_index >= len(self.files):
            self.file_index = 0
        self.plot_data(self.files[self.file_index])
        self.update_file_status()

    def prev_file(self):
        self.file_index -= 1
        if self.file_index < 0:
            self.file_index = len(self.files) - 1
        self.plot_data(self.files[self.file_index])
        self.update_file_status()

    def delete_file(self):
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this file?"):
            os.remove(self.files[self.file_index])
            self.files.pop(self.file_index)
            self.file_index = min(self.file_index, len(self.files) - 1)
            if self.files:
                self.plot_data(self.files[self.file_index])
                self.update_file_status()

    def edit_readme(self):
        self.text_area.config(state=NORMAL)  # Make the text area editable
        self.text_area.focus_set()  # Set focus to the text area

        new_content = self.text_area.get(1.0, END)
        with open(readme_file[0], "w") as file:
            file.write(new_content)
        self.text_area.delete(1.0, END)
        self.text_area.insert(INSERT, new_content)


def main():
    root = Tk()
    root.title("Wearable Data Editor")
    app = DataVisualizer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
