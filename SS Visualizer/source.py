import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk

import sorts
import random
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import matplotlib

matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def generate_list(n):
    lst = []
    for x in range(pow(2, n)):
        lst.append(random.randint(1, pow(10, 4)))

    return lst


def randomize(lst):
    random.seed(time.time())
    random.shuffle(lst)


def sort(loops):
    s = 0.0
    t1 = time.clock()

    dataset = []

    for x in range(loops):
        lst = generate_list(pow(2, x))

        if OptionMenu.get() == "Insertion":
            sorts.insertionsort(lst)
        elif OptionMenu.get() == "Bubble":
            sorts.bubblesort(lst)
        elif OptionMenu.get() == "Merge":
            sorts.mergesort(lst, lst[0], len(lst) - 1)
        elif OptionMenu.get() == "Quick":
            sorts.quicksort(lst, lst[0], len(lst) - 1)
        elif OptionMenu.get() == "Selection":
            sorts.selectionsort(lst)

        t2 = time.clock()
        s += t2 - t1

        dataset.append(tuple(pow(2, x), s))


class SSV(tk.Tk):
    def __init__(self, height=None, width=None, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        for F in (StartPage, SortingVisualizer, SearchingVisualizer):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        if cont == StartPage:
            res = "320x240"
        elif cont == SortingVisualizer or cont == SearchingVisualizer:
            res = "1280x600"

        frame.config(bg="powder blue")
        frame.tkraise()
        frame.winfo_toplevel().geometry(res)


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Searching & Sorting Algorithm Visualizer \n\nPowered by",
                         font=("arial", 10, "bold"), bg="powder blue").place(x=25, y=0)
        label2 = Label(self, text="Coded by \n\n AwesomenessWithin & 7enTropy7", font=("arial", 10, "bold"),
                       bg="powder blue").place(x=40, y=150)

        # image = Image.open("pyTkinter.jpg")
        # image = image.resize((35, 35), Image.ANTIALIAS)
        # photo = ImageTk.PhotoImage(image)
        # label_img = Label(image=photo)
        # label_img.image = photo  # keep a reference!
        # label_img.place(x=135, y=55)

        button_sort = tk.Button(self, text="Sorting Visualizer", bg="brown", fg="white", font=("arial", 10, "bold"),
                                command=lambda: controller.show_frame(SortingVisualizer)).place(x=10, y=100)

        button_search = tk.Button(self, text="Searching Visualizer", bg="brown", fg="white", font=("arial", 10, "bold"),
                                  command=lambda: controller.show_frame(SearchingVisualizer)).place(x=165, y=100)
        tk.Frame.config(self, height=640, width=480)


class SortingVisualizer(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Sorting Visualizer", font=("arial", 10, "bold"), bg="powder blue")
        label.pack(pady=10, padx=10)

        data = {
            'Insertion': 'Insertion Sort',
            'Bubble': 'Bubble Sort',
            'Merge': 'Merge Sort',
            'Quick': 'Quick Sort',
            'Selection': 'Selection Sort',
        }

        var = tk.StringVar()
        var.set('Select...')
        p = OptionMenu(self, var, *data, command=self.boxtext)
        p.pack()

        menu = tk.Label(self)
        menu.pack(pady=10, padx=10)

        button1 = Button(self, text="Back to Home", bg="brown", fg="white",
                         command=lambda: controller.show_frame(StartPage)).place(x=0, y=0)

        button2 = Button(self, text="Searching Visualizer", bg="brown", fg="white",
                         command=lambda: controller.show_frame(SearchingVisualizer)).place(x=90, y=0)

        spin = Spinbox(self, from_=0, to=22, width=3, font=("arial", 10, "bold")).place(x=50, y=550)

        button3 = Button(self, text="Randomize Data", bg="brown", fg="white", width=15,
                         command=lambda: controller.randomize(spin)).place(x=120, y=550)

        button4 = Button(self, text="Sort", bg="brown", fg="white", width=10,
                         command=lambda: controller.sort(spin, p)).place(x=800, y=550)

        button5 = Button(self, text="Reset", bg="brown", fg="white", width=10,
                         command=lambda: controller.reset()).place(x=900, y=550)

        bar_rect = Figure(figsize=(5, 4), dpi=100)
        plot2 = bar_rect.add_subplot(1, 1, 1)

        plot2.plot(0.5, 0.3, color="blue", marker="o", linestyle="")

        x = [0.1, 0.2, 0.3]
        y = [-0.1, -0.2, -0.3]

        plot2.plot(x, y, color="blue", marker="x", linestyle="")

        canvas2 = FigureCanvasTkAgg(bar_rect, self)
        canvas2.get_tk_widget().place(x=750, y=100)

        graph = Figure(figsize=(5, 4), dpi=100)
        plot1 = graph.add_subplot(1, 1, 1)

        plot1.plot(0.5, 0.3, color="red", marker="o", linestyle="")

        x = [0.1, 0.2, 0.3]
        y = [-0.1, -0.2, -0.3]
        plot1.plot(x, y, color="blue", marker="x", linestyle="")

        canvas1 = FigureCanvasTkAgg(graph, self)
        canvas1.get_tk_widget().place(x=30, y=100)

    def boxtext(self, data):
        yield menu.config(text=data[self], font=("arial", 10, "bold"), bg="powder blue")


class SearchingVisualizer(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Searching Visualizer", font=("arial", 10, "bold"), bg="powder blue")
        label.pack(pady=10, padx=10)

        button1 = Button(self, text="Back to Home", bg="brown", fg="white",
                         command=lambda: controller.show_frame(StartPage)).place(x=0, y=0)

        button2 = Button(self, text="Sorting Visualizer", bg="brown", fg="white",
                         command=lambda: controller.show_frame(SortingVisualizer)).place(x=90, y=0)


if __name__ == "__main__":
    root = SSV()
    root.title("Welcome")
    root.resizable(False, False)

    root.mainloop()
