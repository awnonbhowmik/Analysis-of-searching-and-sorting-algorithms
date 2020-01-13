import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import random
import time
import sorts
import search
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class SSV(tk.Tk):
    def __init__(self, height=None, width=None, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.width = width
        self.height = height
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

    def sort(self, var, loops):
        sort_algo = var.get()

        lst = [x + 1 for x in range(loops)]
        random.seed(time.time())
        random.shuffle(lst)

        if sort_algo == "Insertion":
            A = sorts.insertionsort(lst)
        elif sort_algo == "Bubble":
            A = sorts.bubblesort(lst)
        elif sort_algo == "Merge":
            A = sorts.mergesort(lst, lst[0], len(lst) - 1)
        elif sort_algo == "Quick":
            A = sorts.quicksort(lst, lst[0], len(lst) - 1)
        elif sort_algo == "Selection":
            A = sorts.selectionsort(lst)

        title = sort_algo + " Sort"
        fig, ax = plt.subplots()
        ax.set_title(title)
        bar_rects = ax.bar(range(len(lst)), lst, align="edge")
        ax.set_xlim(0, len(lst))
        ax.set_ylim(0, int(1.07 * max(lst)))
        text = ax.text(0.02, 0.95, "", transform=ax.transAxes)
        iteration = [0]

        def update_fig(lst, rects, iteration):
            for rect, val in zip(rects, lst):
                rect.set_height(val)
            iteration[0] += 1
            text.set_text("# of operations: {}".format(iteration[0]))

            canvas = FigureCanvasTkAgg(fig, master=self)
            canvas.get_tk_widget().place(x=30, y=80)

        anim = animation.FuncAnimation(fig, func=update_fig,
                                       fargs=(bar_rects, iteration), frames=A, interval=1,
                                       repeat=False, blit=False)
        # return anim
        plt.show()


        """def reset():
            if SearchingVisualizer:
                SearchingVisualizer.destroy()
            elif SortingVisualizer:
                SortingVisualizer.destroy()
"""


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Searching & Sorting Algorithm Visualizer \n\nPowered by",
                         font=("arialloops", 10, "bold"), bg="powder blue").place(x=25, y=0)
        label2 = Label(self, text="Coded by \n\n AwesomenessWithin & 7enTropy7", font=("arial", 10, "bold"),
                       bg="powder blue").place(x=40, y=150)

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
        p = OptionMenu(self, var, *data, command=self.boxtext)
        p.pack()

        menu = tk.Label(self)
        menu.pack(pady=10, padx=10)

        button1 = Button(self, text="Back to Home", bg="brown", fg="white",
                         command=lambda: controller.show_frame(SortingVisualizer)).place(x=0, y=0)

        button2 = Button(self, text="Searching Visualizer", bg="brown", fg="white",
                         command=lambda: controller.show_frame(SearchingVisualizer)).place(x=90, y=0)

        spinner = tk.StringVar()
        spin = Spinbox(self, from_=0, to=22, width=3, font=("arial", 10, "bold"), textvariable=spinner).place(x=50,
                                                                                                              y=570)

        button4 = Button(self, text="Sort", bg="brown", fg="white", width=10,
                         command=lambda: controller.sort(var, int(spinner.get()))).place(x=800, y=550)

    def boxtext(self, data, menu=None):
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
