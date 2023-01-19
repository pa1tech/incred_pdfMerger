import tkinter as tk
from PyPDF2 import PdfMerger
from tkinter.filedialog import askopenfilenames
import sys,os,ctypes

myappid = 'pa1tech.pdfmerger.1'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
    

class Example(tk.LabelFrame):
    def __init__(self, *args, **kwargs):
        tk.LabelFrame.__init__(self, *args, **kwargs)
        self.data = []

        self.grid_columnconfigure(1, weight=1, uniform="fred")
        tk.Label(self, text="Sl No.",anchor="w",font=("", 10, 'bold')).grid(row=0, column=0, sticky="ew")
        tk.Label(self, text="File Name", anchor="w",font=("", 10, 'bold')).grid(row=0, column=1, sticky="ew")
        tk.Label(self, text="", anchor="w").grid(row=0, column=2, sticky="ew")
        tk.Label(self, text="", anchor="w").grid(row=0, column=3, sticky="ew")
        tk.Label(self, text="", anchor="w").grid(row=0, column=4, sticky="ew")

        row = 1
        self.labels = []
        for i in range(10):
            text = tk.StringVar()
            self.labels.append(text)
            tk.Label(self, text=str(i+1), anchor="w").grid(row=row, column=0, sticky="ew")
            tk.Label(self, textvariable=self.labels[i], anchor="w").grid(row=row, column=1, sticky="ew")
            tk.Button(self, text="Delete", command=lambda nr=i: self.delete(nr)).grid(row=row, column=4, sticky="ew")
            tk.Button(self, text="  Up  ", command=lambda nr=i: self.up(0,nr)).grid(row=row, column=2, sticky="ew")
            tk.Button(self, text="Down", command=lambda nr=i: self.up(-1,nr)).grid(row=row, column=3, sticky="ew")
            row += 1

        tk.Button(self,text="Add File",command=self.add,font=("", 10, 'bold')).grid(row=row, column=2,columnspan=3, pady=(10,0), sticky="ew")
        tk.Button(self,text="Merge",command=self.merge,font=("", 10, 'bold')).grid(row=row+1, column=2,columnspan=3,pady=(10,0), sticky="ew")

        self.helpTxt = tk.StringVar()
        self.helpTxt.set("Welocme!")
        tk.Label(self, textvariable=self.helpTxt, fg="blue", cursor="hand2",font=("", 10, 'bold')).grid(row=row,column=0,columnspan=2,pady=(10,0),sticky="ew")

        self.helpTxt1 = tk.StringVar()
        self.helpTxt1.set("")
        tk.Label(self, textvariable=self.helpTxt1, fg="blue", cursor="hand2",font=("", 10, 'bold')).grid(row=row+1,column=0,columnspan=2,pady=(10,0),sticky="ew")

    def up(self,j,i):
        if((i < (j+len(self.data))) and (i>j)):
            if(j==0):
                temp = self.data[i-1]
                self.data[i-1] = self.data[i]
                self.data[i] = temp
            else:
                temp = self.data[i+1]
                self.data[i+1] = self.data[i]
                self.data[i] = temp
            self.update()
        
    def update(self):
        for i in range(10) :
            if(i<len(self.data)):
                text = self.data[i]
                if(len(text)>66): text = text[:10] + '...' + text[-56:]
                self.labels[i].set(text)
            else:
                self.labels[i].set("")

    def delete(self, nr):
        if(nr < len(self.data)):
            self.data.pop(nr)
            self.update()

    def add(self):
        files = askopenfilenames(filetypes =[('pdf file','*.pdf')])
        for file in files:
            self.data.append(file)
        self.update()
    
    def merge(self):
        if(len(self.data)>0):
            merger = PdfMerger()
            file = self.data[0].split("/")[-1]

            d = self.data[0].split("/")[:-1]
            pwd = '/'.join([str(elem) for elem in d])

            for pdf in self.data:
                merger.append(pdf)

            saved = pwd+"/Merged_%dfiles_%s"%(len(self.data),file)
            merger.write(saved)
            merger.close()
            
            text = "Merged files saved to ..."
            self.helpTxt.set(text)

            text = saved
            if(len(text)>60): text = text[:30] + '...' + text[-30:]
            self.helpTxt1.set(text)
        else:
            text = "Add some files!"
            self.helpTxt.set(text)



if __name__ == "__main__":
    root = tk.Tk()

    root.title("!ncred PDF Merge")
    root.geometry("600x400")
    root.resizable(width=False, height=False)
    root.iconbitmap(resource_path("smiley.ico"))
    Example(root).pack(side="top", fill="both", expand=True, padx=10, pady=10)
    root.mainloop()

#pyinstaller --noconsole --icon=smiley.ico --add-data="smiley.ico;." --onefile pdfMergerApp.py