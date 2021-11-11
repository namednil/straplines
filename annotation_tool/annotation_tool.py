from tkinter import ttk

try:
    ttk_themes_available = True
    from ttkthemes import ThemedTk #https://ttkthemes.readthedocs.io/en/latest/installation.htmls
    theme_name = "arc" #which theme you want to use. see https://ttkthemes.readthedocs.io/en/latest/themes.html
except ImportError:
    ttk_themes_available = False

import tkinter
from tkinter.font import Font

import argparse
import json

width = 1024
height = 780

text_width = 90
font_name = "Bitstream Charter"
font_size = 12

SUMMARY = "summary"
STRAPLINE = "strapline"
BOTH = "summary_and_strapline"
NEITHER = "no_summary_no_strapline"
SKIP = "skipped"
PARA = "paraphrase"



class Window(ttk.Frame):

    def __init__(self, master, source_file_loc, annotator_id):
    # ~ def __init__(self, master):
        ttk.Frame.__init__(self, master)        
        self.master = master
    
        self.source_file_loc = source_file_loc
        self.annotator_id = annotator_id
        
        # widget can take all window
        self.pack(fill=tkinter.BOTH, expand=1)
        
        self.columnconfigure(0, pad=5)
        self.columnconfigure(1, pad=5)
        self.columnconfigure(2, pad=5)

        self.rowconfigure(0, pad=10)
        self.rowconfigure(1, pad=10)
        self.rowconfigure(2, pad=10)
        self.rowconfigure(3, pad=5)
        self.rowconfigure(4, pad=5)
        self.rowconfigure(5, pad=5)
        self.rowconfigure(6, pad=10)
        self.rowconfigure(7, pad=10)
        self.rowconfigure(8, pad=10)
        self.rowconfigure(9, pad=10)
        self.rowconfigure(10, pad=10)
        self.rowconfigure(11, pad=10)
        self.rowconfigure(12, pad=10)
        self.rowconfigure(13, pad=10)
        
        
        lbl = ttk.Label(self, text="Headline: ")
        lbl.config(anchor=tkinter.CENTER, font=text_font)
        lbl.grid(row=0, column=0)
        
        
        
        
        self.headline = tkinter.Text(self, height=2, width=text_width, wrap="word")
        self.headline.config(state='disabled')
        # ~ self.sum.config(anchor=tkinter.CENTER)
        self.headline.grid(row=0, column=1, sticky="we")
        self.headline.configure(font=text_font)
        
        # ~ self.lbl = ttk.Label(self, text="Headline")
        # ~ self.lbl.config(anchor=tkinter.W)
        # ~ self.lbl.grid(row=0, column=1, sticky=tkinter.W)
        
        
        lbl = ttk.Label(self, text='"Summary": ')
        lbl.config(anchor=tkinter.CENTER, font=text_font)
        lbl.grid(row=1, column=0)
        
        self.sum = tkinter.Text(self, height=4, width=text_width, wrap="word")
        self.sum.config(state='disabled')
        # ~ self.sum.config(anchor=tkinter.CENTER)
        self.sum.grid(row=1, column=1, sticky="we")
        self.sum.configure(font=text_font)
        
        # create a scrollbar widget and set its command to the text widget
        scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.sum.yview)
        scrollbar.grid(row=1, column=2, sticky='ns')

        #  communicate back to the scrollbar
        self.sum['yscrollcommand'] = scrollbar.set
        
        
        #article text:
        
        lbl = ttk.Label(self, text='Article: ')
        lbl.config(anchor=tkinter.CENTER, font=text_font)
        lbl.grid(row=2, column=0)
        
        self.article = tkinter.Text(self, height=10, wrap="word")
        self.article.config(state='disabled')
        # ~ self.sum.config(anchor=tkinter.CENTER)
        self.article.grid(row=2, column=1, sticky="we")
        self.article.configure(font=text_font)
        
        # create a scrollbar widget and set its command to the text widget
        scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.article.yview)
        scrollbar.grid(row=2, column=2, sticky='ns')

        #  communicate back to the scrollbar
        self.article['yscrollcommand'] = scrollbar.set
        
        
        self.annotation_var = tkinter.IntVar()
        
        self.r1 = ttk.Radiobutton(self, text="Summary", variable=self.annotation_var, value=1)
        self.r2 = ttk.Radiobutton(self, text="Strapline", variable=self.annotation_var, value=2)
        self.r3 = ttk.Radiobutton(self, text="Neither", variable=self.annotation_var, value=3)
        self.r4 = ttk.Radiobutton(self, text="Both", variable=self.annotation_var, value=4)
        self.r5 = ttk.Radiobutton(self, text="Skip", variable=self.annotation_var, value=5)
        self.r6 = ttk.Radiobutton(self, text="Paraphrase", variable=self.annotation_var, value=6)
        self.r1.grid(row=3, column=1,sticky=tkinter.W)
        self.r2.grid(row=4, column=1,sticky=tkinter.W)
        self.r3.grid(row=5, column=1,sticky=tkinter.W)
        self.r4.grid(row=6, column=1,sticky=tkinter.W)
        self.r5.grid(row=7, column=1,sticky=tkinter.W)
        self.r6.grid(row=8, column=1,sticky=tkinter.W)
        
        
        
        lbl2 = ttk.Label(self, text="Shortcuts: Next example: m")
        lbl2.config(anchor=tkinter.S)
        #lbl2.pack(anchor='sw')

        nextButton = ttk.Button(self, text="Next example", command=self.nextClick)
        nextButton.grid(row=9, column=1, sticky=tkinter.W)
        prevButton = ttk.Button(self, text="Previous example", command=self.prevClick)
        prevButton.grid(row=10, column=1, sticky=tkinter.W)
        
        self.extractive = tkinter.IntVar()
        check = ttk.Checkbutton(self, text='"Summary" actually extractive?',variable=self.extractive, onvalue=1, offvalue=0)
        check.grid(row=11, column = 1, sticky=tkinter.W)

        
        lbl = ttk.Label(self, text='Comments: ')
        lbl.config(anchor=tkinter.CENTER, font=text_font)
        lbl.grid(row=12, column=0)
        
        self.comment = tkinter.Text(self, height=3, wrap="word")
        # ~ self.sum.config(anchor=tkinter.CENTER)
        self.comment.grid(row=12, column=1, sticky="we")
        self.comment.configure(font=text_font)
        
        # create a scrollbar widget and set its command to the text widget
        scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.sum.yview)
        scrollbar.grid(row=12, column=2, sticky='ns')

        #  communicate back to the scrollbar
        self.comment['yscrollcommand'] = scrollbar.set
        
        exitButton = ttk.Button(self, text="Write annotations & Exit", command=self.clickExitButton)
        exitButton.grid(row=13, column=1, sticky='ns')
        
        
        
        self.instances = []
        self.load_summaries(source_file_loc)
        self.active_instance = self.next_unannotated(0)
        self.displayInstance(self.active_instance)
        
        
        
    def load_summaries(self, filename):
        self.instances = []
        with open(filename) as f:
            for i, line in enumerate(f):
                self.instances.append(json.loads(line))
                if "annotator" in self.instances[-1] and self.instances[-1]["annotator"] != self.annotator_id:
                    raise ValueError(f'Annotator id {self.instances[-1]["annotator"]} was already used in this file and you ({self.annotator_id}) would overwrite their work.')
                
    def save_summaries(self, filename):
        with open(filename, "w") as f:
            for s in self.instances:
                f.write(json.dumps(s))
                f.write("\n") 
                
    def next_unannotated(self, pos):
        for i, ex in enumerate(self.instances):
            if i < pos:
                continue
            if "annotation" not in self.instances[i] or self.instances[i]["annotation"] == None:
                return i
        return len(self.instances)-1
        
        
    def displayInstance(self, i):
        #todo: save content???
        
        self.headline.config(state='normal')
        self.headline.delete(1.0, "end")
        self.headline.insert(1.0, self.instances[i]["title"])
        self.headline.config(state='disabled')
        
        self.sum.config(state='normal')
        self.sum.delete(1.0, "end")
        self.sum.insert(1.0, self.instances[i]["summary"])
        self.sum.config(state='disabled')
        
        
        self.article.config(state='normal')
        self.article.delete(1.0, "end")
        self.article.insert(1.0, u"{}".format(self.instances[i]["text"]))
        self.article.config(state='disabled')
        
        
        self.comment.delete(1.0, "end")
        
        if "comment" in self.instances[i]:
            self.comment.insert(1.0, self.instances[i]["comment"])
            
        set_a = 0
        if "annotation" in self.instances[i]:
            a = self.instances[i]["annotation"]
            if a is None:
                set_a = 0
            elif a == SUMMARY:
                set_a = 1
            elif a == STRAPLINE:
                set_a = 2
                
            elif a == NEITHER:
                set_a = 3
                
            elif a == BOTH:
                set_a = 4
            elif a == SKIP:
                set_a = 5
                
            elif a == PARA:
                set_a = 6
            else:
                raise ValueError(f"Unknown code {a}")
                
        if "marked_as_extractive" in self.instances[i]:
            self.extractive.set(int(bool(self.instances[i]["marked_as_extractive"])))
                
        self.annotation_var.set(set_a)
        # ~ self.lbl["text"] = self.instances[i]["title"]
        
        self.r1.focus_set()
        
    def save_instance(self):
        try:
            a = self.annotation_var.get()
        except tkinter.TclError:
            a = 0
            
        if a == 0:
            self.instances[self.active_instance]["annotation"] = None
        elif a == 1:
            #summary
            self.instances[self.active_instance]["annotation"] = SUMMARY
        elif a == 2:
            self.instances[self.active_instance]["annotation"] = STRAPLINE
        elif a == 3:
            self.instances[self.active_instance]["annotation"] = NEITHER
        elif a == 4:
            self.instances[self.active_instance]["annotation"] = BOTH
        elif a == 5:
            self.instances[self.active_instance]["annotation"] = SKIP
        elif a == 6:
            self.instances[self.active_instance]["annotation"] = PARA
        else:
            raise ValueError(f"Unknown code {a}")
        
        self.instances[self.active_instance]["annotator"] = self.annotator_id
        
        self.instances[self.active_instance]["marked_as_extractive"] = bool(self.extractive.get())
        
        comment_before = self.instances[self.active_instance].get("comment", "")
        comment = self.comment.get(1.0, "end-1c")
        if comment != comment_before:
            self.instances[self.active_instance]["comment"] = comment
        
        

    def nextClick(self):
        self.save_instance()
        self.active_instance = min(len(self.instances)-1, self.active_instance+1)
        self.displayInstance(self.active_instance)
        
    def prevClick(self):
        self.save_instance()
        self.active_instance = max(0, self.active_instance-1)
        self.displayInstance(self.active_instance)

    def clickExitButton(self):
        self.save_instance()
        self.save_summaries(self.source_file_loc)
        exit()



parser = argparse.ArgumentParser()
parser.add_argument("file_to_annotate")
parser.add_argument("annotator_id")

args = parser.parse_args()

filename=args.file_to_annotate
annotator_id = args.annotator_id

if ttk_themes_available:
    root = ThemedTk(theme=theme_name)
else:
    root = tkinter.Tk() # works without themes

text_font = Font(family=font_name, size=font_size)
# ~ root.option_add('*Font', text_font)
app = Window(root, filename, annotator_id)
root.wm_title("Strapline annotation tool.")
root.geometry(f"{width}x{height}")
root.protocol("WM_DELETE_WINDOW", app.clickExitButton)
root.mainloop()

