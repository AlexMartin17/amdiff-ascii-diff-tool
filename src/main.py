import os
import re
import sys
import tkinter
import tkinter as tk
import difflib
import platform
import xml.etree.ElementTree as ET
import webbrowser
from tkinter import filedialog
from tkinter import messagebox

os_name = platform.system()
is_windows = os_name == 'Windows'
is_mac = os_name == 'Darwin'
is_linux = os_name == 'Linux'


class SyntaxHighlight:
    def __init__(self, widget, language):
        self.widget = widget
        self.language = language
        global is_windows
        global is_mac
        global is_linux

    def word_highlight(self, word, tag_code):
        self.widget.tag_remove(word, "1.0", "end")

        pattern = r'\b' + re.escape(word) + r'\b'
        start_index = "1.0"

        while True:
            match = re.search(pattern, self.widget.get(start_index, "end"))
            if not match:
                break
            start_pos = start_index + "+%dc" % match.start()
            end_pos = start_index + "+%dc" % match.end()
            self.widget.tag_add(word, start_pos, end_pos)
            start_index = end_pos

        self.widget.tag_configure(word, foreground=tag_code)

    def string_highlight(self):
        self.widget.tag_remove("strings", "1.0", "end")

        pattern = r'(["\'])(.*?)\1'

        start_index = "1.0"
        while True:
            start_index = self.widget.search(pattern, start_index, stopindex="end-1c", regexp=True)
            if not start_index:
                break
            match = re.match(pattern, self.widget.get(start_index, "end"))
            if match:
                start, end = start_index, f"{start_index}+{len(match.group(0))}c"
                self.widget.tag_add("strings", start, end)
                start_index = end

        self.widget.tag_configure("strings", foreground="#229008")

    def highlight(self):
        if is_windows:
            xml_tree = ET.parse(f'{os.path.dirname(os.path.abspath(__file__))}\\config\\{self.language}.xml')
        else:
            xml_tree = ET.parse(f'{os.path.dirname(os.path.abspath(__file__))}/../config/{self.language}.xml')
        xml_root = xml_tree.getroot()

        styles_info = {}
        style_elements = xml_root.findall(".//style")

        for style_element in style_elements:
            name = style_element.get("name")
            foreground = style_element.get("foreground")
            styles_info[name] = foreground

        for name, foreground in styles_info.items():
            self.word_highlight(name, foreground)

        self.string_highlight()


class Diff:
    def __init__(self, file1=None, file2=None):
        global is_windows
        global is_mac
        global is_linux

        if file1 and file2:
            self.file1 = file1
            self.file2 = file2
            self.diff(self.file1, self.file2)
            self.run(self.file1, self.file2)
        else:
            self.root = tk.Tk()
            self.root.title("amdiff")

            padding = 10

            self.entry1 = tk.Entry(self.root, width=30)
            self.entry1.grid(row=1, column=0, padx=padding, pady=padding)
            self.button1 = tk.Button(self.root, text="File 1", command=lambda: self.browse_file(1))
            self.button1.grid(row=1, column=1, padx=padding)

            self.entry2 = tk.Entry(self.root, width=30)
            self.entry2.grid(row=2, column=0, padx=padding, pady=padding)
            self.button2 = tk.Button(self.root, text="File 2", command=lambda: self.browse_file(2))
            self.button2.grid(row=2, column=1, padx=padding)

            self.button3 = tk.Button(self.root, text="Diff", width=10, command=self.diff)
            self.button3.grid(row=3, column=0, columnspan=2, padx=padding)

            self.screen_width = self.root.winfo_screenwidth()
            self.screen_height = self.root.winfo_screenheight()

            self.window_width = self.entry1.winfo_reqwidth() + self.button1.winfo_reqwidth() + (padding * 4)
            self.window_height = (self.entry1.winfo_reqheight() * 2) + self.button3.winfo_reqheight() + (padding * 5)

            x = (self.screen_width - self.window_width) // 2
            y = (self.screen_height - self.window_height) // 2

            self.root.geometry(f"{int(self.window_width)}x{int(self.window_height)}+{int(x)}+{int(y)}")
            self.root.resizable(False, False)
            self.root.bind("<F1>", self.on_f1_key)

            try:
                if is_mac:
                    self.root.wm_iconphoto(False, tk.PhotoImage(file=f"{os.path.dirname(os.path.abspath(__file__))}/../img/apple-icon-57x57.png"))
                elif is_windows:
                    self.root.wm_iconphoto(False, tk.PhotoImage(file=f"{os.path.dirname(os.path.abspath(__file__))}\\img\\icon_120x120.png"))
                elif is_linux:
                    self.root.wm_iconphoto(False, tk.PhotoImage(file=f"{os.path.dirname(os.path.abspath(__file__))}/../img/icon_120x120.png"))
            except tkinter.TclError:
                pass

    def on_f1_key(self, event):
        def open_link(link):
            webbrowser.open(link)

        try:
            window = tk.Toplevel(self.root)
        except AttributeError:
            window = tk.Toplevel(self.diff_window)

        window.title(f"Information")
        developed_by_link = "https://github.com/AlexMartin17/"
        report_issues_link = "https://github.com/AlexMartin17/amdiff-ascii-diff-tool/issues"

        label1 = tk.Label(window, text="Developed by")
        label1.grid(row=0, column=0, sticky="w")

        label2 = tk.Label(window, text=f"{developed_by_link}", fg="blue", cursor="hand2")
        label2.grid(row=0, column=1, sticky="w")

        label3 = tk.Label(window, text="Report issues at")
        label3.grid(row=1, column=0, sticky="w")

        label4 = tk.Label(window, text=f"{report_issues_link}", fg="blue", cursor="hand2")
        label4.grid(row=1, column=1, sticky="w")

        try:
            if is_mac or is_linux:
                logo_path = f"{os.path.dirname(os.path.abspath(__file__))}/../img/apple-icon-57x57.png"
            elif is_windows:
                logo_path = f"{os.path.dirname(os.path.abspath(__file__))}\\img\\apple-icon-57x57.png"
        except tkinter.TclError:
            pass

        image = tk.PhotoImage(file=logo_path)
        image_label = tk.Label(window, image=image)
        image_label.grid(row=0, column=2, rowspan=2)

        label1.bind("<Button-1>", lambda event, link=developed_by_link: open_link(link))
        label2.bind("<Button-1>", lambda event, link=report_issues_link: open_link(link))

        try:
            if is_mac:
                window.wm_iconphoto(False, tk.PhotoImage(file=f"{os.path.dirname(os.path.abspath(__file__))}/../img/apple-icon-57x57.png"))
            elif is_windows:
                window.wm_iconphoto(False, tk.PhotoImage(file=f"{os.path.dirname(os.path.abspath(__file__))}\\img\\icon_120x120.png"))
            elif is_linux:
                window.wm_iconphoto(False, tk.PhotoImage(file=f"{os.path.dirname(os.path.abspath(__file__))}/../img/icon_120x120.png"))
        except tkinter.TclError:
            pass

        window.mainloop()

    """def on_ctrl_scroll(self, event):
        if event.state & 0x4:
            if event.delta > 0:
                # Ctrl+ScrollUp detected
                print("Ctrl+ScrollUp")
            elif event.delta < 0:
                # Ctrl+ScrollDown detected
                print("Ctrl+ScrollDown")"""

    def browse_file(self, entry_num):
        file_path = filedialog.askopenfilename()
        if file_path and entry_num == 1:
            self.entry1.delete(0, tk.END)
            self.entry1.insert(0, file_path)
        elif file_path and entry_num == 2:
            self.entry2.delete(0, tk.END)
            self.entry2.insert(0, file_path)

    def diff(self, file1=None, file2=None):
        def find_extension(input_file):
            file_extension = os.path.splitext(input_file)[1]

            return file_extension

        if file1 and file2:
            try:
                f1 = open(file1, "r").readlines()
                f1_ext = find_extension(file1)
            except FileNotFoundError:
                messagebox.showwarning("Warning", "File1 does not exist!")
                return
            try:
                f2 = open(file2, "r").readlines()
                f2_ext = find_extension(file2)
            except FileNotFoundError:
                messagebox.showwarning("Warning", "File2 does not exist!")
                return

            self.diff_window = tk.Tk()
            self.diff_window.title(f"{file1} vs {file2}")
            self.diff_window.columnconfigure(1, weight=1)
            self.diff_window.rowconfigure(0, weight=1)

        else:
            if len(self.entry1.get()) == 0 or len(self.entry2.get()) == 0:
                messagebox.showwarning("Warning", "No file selected!")
                return
            else:
                try:
                    f1 = open(self.entry1.get(), "r").readlines()
                    f1_ext = find_extension(self.entry1.get())
                except FileNotFoundError:
                    messagebox.showwarning("Warning", "File1 does not exist!")
                    return
                except IsADirectoryError:
                    messagebox.showwarning("Warning", "You are trying to browse directory in File1")
                    return
                try:
                    f2 = open(self.entry2.get(), "r").readlines()
                    f2_ext = find_extension(self.entry2.get())
                except FileNotFoundError:
                    messagebox.showwarning("Warning", "File2 does not exist!")
                    return
                except IsADirectoryError:
                    messagebox.showwarning("Warning", "You are trying to browse directory in File2")
                    return

                self.diff_window = tk.Toplevel(self.root)
                self.diff_window.title(f"{self.entry1.get()} vs {self.entry2.get()}")
                self.diff_window.columnconfigure(1, weight=1)
                self.diff_window.rowconfigure(0, weight=1)

        if is_windows:
            self.diff_window.state("zoomed")
        elif is_linux:
            self.diff_window.attributes("-zoomed", 1)
        elif is_mac:
            self.diff_window.attributes("-alpha", 1)

        line_nums = tk.Text(self.diff_window, width=4, borderwidth=0, padx=0, highlightthickness=0, wrap="none")
        line_nums.grid(row=0, column=0, sticky="ns")
        line_nums.configure(bg="#2B2B2B")

        text_widget = tk.Text(self.diff_window, wrap="none")
        text_widget.grid(row=0, column=1, sticky="nsew")
        text_widget.configure(bg="#2B2B2B")

        scrollbar = tk.Scrollbar(self.diff_window, orient="vertical", command=text_widget.yview)
        scrollbar.grid(row=0, column=2, sticky="ns")

        text_widget.config(yscrollcommand=scrollbar.set)

        text_widget.tag_config("red", background="#802E34", foreground="#E6F0FA", selectbackground="blue", selectforeground="white")
        text_widget.tag_config("green", background="#4A5943", foreground="#E6F0FA", selectbackground="blue", selectforeground="white")
        text_widget.tag_config("def", foreground="#D4D4D4", selectbackground="blue", selectforeground="white")

        def update_line_numbers(event):
            line_number = 1
            text_content = text_widget.get("1.0", "end")
            lines_list = text_content.split("\n")
            lines = lines_list[:-2]
            new_lines = []

            for l in lines:
                if l.strip().startswith("?  ") or l.strip().startswith("-  "):
                    new_lines.append("")
                else:
                    new_lines.append(str(line_number))
                    line_number += 1

            updated_line_numbers = "\n".join(new_lines)
            line_nums.config(state="normal")
            line_nums.delete(1.0, "end")
            line_nums.insert("1.0", updated_line_numbers)
            line_nums.config(state="disabled")

        text_widget.bind("<KeyRelease>", update_line_numbers)

        differ = difflib.Differ()
        diff = list(differ.compare(f1, f2))

        for line in diff:
            line = line.replace('\n', '')
            if line.startswith("-"):
                text_widget.insert(tk.END, f"{line}\n", "red")
            elif line.startswith("+"):
                text_widget.insert(tk.END, f"{line}\n", "green")
            else:
                text_widget.insert(tk.END, f"{line}\n", "def")

        text_widget.tag_configure("custom_font_tag", font=("Consolas", 11), foreground="#D4D4D4")
        text_widget.tag_add("custom_font_tag", "1.0", "end")
        line_nums.configure(font=("Consolas", 11), foreground="#D4D4D4")

        update_line_numbers(None)

        if f1_ext == f2_ext == ".py":
            SyntaxHighlight(text_widget, "python").highlight()
        elif f1_ext == f2_ext == ".c" or f1_ext == f2_ext == ".cpp":
            SyntaxHighlight(text_widget, "cpp").highlight()

        self.diff_window.bind("<F1>", self.on_f1_key)

        try:
            if is_mac:
                self.diff_window.wm_iconphoto(False, tk.PhotoImage(file=f"{os.path.dirname(os.path.abspath(__file__))}/../img/apple-icon-57x57.png"))
            elif is_windows:
                self.diff_window.wm_iconphoto(False, tk.PhotoImage(file=f"{os.path.dirname(os.path.abspath(__file__))}\\img\\icon_120x120.png"))
            elif is_linux:
                self.diff_window.wm_iconphoto(False, tk.PhotoImage(file=f"{os.path.dirname(os.path.abspath(__file__))}/../img/icon_120x120.png"))
        except tkinter.TclError:
            pass
        # self.diff_window.bind("<Control-MouseWheel>", self.on_ctrl_scroll)

    def run(self, file1=None, file2=None):
        if file1 and file2:
            self.diff_window.mainloop()
        else:
            self.root.mainloop()


def main():
    if len(sys.argv) == 3:
        Diff(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 1:
        Diff().run()
    else:
        print("USAGE: amdiff <file1> <file2>")


if __name__ == "__main__":
    main()
