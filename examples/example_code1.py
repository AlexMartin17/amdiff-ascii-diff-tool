class Diff:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("amdiff")

        self.window_width = 265
        self.window_height = 120

        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        x = (self.screen_width - self.window_width) // 2
        y = (self.screen_height - self.window_height) // 2

        self.root.geometry(f"{self.window_width}x{self.window_height}+{int(x)}+{int(y)}")
        self.root.resizable(False, False)

        self.entry1 = tk.Entry(self.root, width=30)
        self.entry1.grid(row=1, column=0, padx=10, pady=10)
        self.button1 = tk.Button(self.root, text="File 1", command=lambda: self.browse_file(1))
        self.button1.grid(row=1, column=1, padx=10)

        self.entry2 = tk.Entry(self.root, width=30)
        self.entry2.grid(row=2, column=0, padx=10, pady=10)
        self.button2 = tk.Button(self.root, text="File 2", command=lambda: self.browse_file(2))
        self.button2.grid(row=2, column=1, padx=10)

        self.button3 = tk.Button(self.root, text="Diff", width=10, command=self.diff)
        self.button3.grid(row=3, column=0, padx=10)