import tkinter as tk


class Login(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.canvas = tk.Canvas(self, borderwidth=0,highlightthickness=0,
                                width=200, height=100)
        ents = self.make_form(parent)
        self.canvas.pack(side="top", fill="both", expand=False, padx=2, pady=2)
        self.canvas.bind('<Return>', (lambda event, e=ents: self.fetch(e)))
        b1 = tk.Button(self.canvas, text='Show',
                       command=(lambda e=ents: self.fetch(e)))
        b1.pack(side=tk.LEFT, padx=5, pady=5)
        b2 = tk.Button(self.canvas, text='Quit', command=self.canvas.quit)
        b2.pack(side=tk.LEFT, padx=5, pady=5)

    def fetch(self, entries):
        for entry in entries:
            field = entry[0]
            text = entry[1].get()
            print('%s: "%s"' % (field, text))

    def make_form(self, root):
        entries = []
        row = tk.Frame(root)
        lab = tk.Label(row, width=15, text='Username', anchor='w')
        ent = tk.Entry(row)
        row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        lab.pack(side=tk.LEFT)
        ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        entries.append(('Username', ent))
        return entries
