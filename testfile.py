from tkinter import *
from live_audio_reader import speech_to_text
from mp32text import mp3file_to_text
from tkinter import ttk
from tkinter import filedialog
from main import youtube_to_text
import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv
import winsound as wn



def opentextfile():
    filetypes = (
        ('text files', '*.txt'),
        ('All files', '*.*')
    )

    filename = filedialog.askopenfilename(
        title='Open a file',
        filetypes=filetypes)
    file = open(filename,'r')
    filecontents = file.readlines()

    return filecontents

def openmp3file():
    filetypes = (
        ('audio files', '*.mp3'),
        ('All files', '*.*')
    )

    filename = filedialog.askopenfilename(
        title='Open a file',
        #initialdir='/',
        filetypes=filetypes)

def mp3_to_text():
    filetypes = (
        ('audio files', '*.mp3'),
        ('All files', '*.*')
    )

    filename = filedialog.askopenfilename(
        title='Open a file',
        #initialdir='/',
        filetypes=filetypes)
    
    text_file_name = mp3file_to_text(filename)

    view_file()
    
def view_file():
    FileText.delete(1.0, 'end')
    
    textfile = opentextfile()
    
    FileText.insert(1.0, textfile)
   
    FileText.delete(1.0)
    FileText.delete(("end-2c"))
   
def live_text():
    window=Tk()
    window.geometry('200x175')
    
    def record(duration, file):
        freq = 41010
        wn.Beep(700, 1000)
        print("Recording...")
        recording = sd.rec(int(duration * freq), samplerate=freq, channels=2)
        sd.wait()
        write((file + ".mp3"), freq, recording)
        wv.write(file, recording, freq, sampwidth=2)
        print("Recording Stopped...")   
        
    def getdur():
        duration = dur.get()
        return duration
    def getfil():
        file = name.get()
        return file

    L1 = Label(window, text = "Name of file: ")
    L1.place(x=0, y=0, height = 15)
    name = Entry(window)
    name.place(x=0, y=15, height = 15)

    
    L2 = Label(window, text = "Duration: ")
    L2.place(x=0, y=30, height = 15)
    dur = Entry(window)
    dur.place(x=0, y=45, height = 15)

    
    getvalues = Button(window, text = "Record Values Above", command = lambda: get())
    getvalues.place(x=10, y = 100)
    submit = Button(window, text = "Start Recording: ", command =lambda: record(getdur(), getfil()))
    submit.place(x=10, y = 70)
   
def yt_text():
    window=Tk()
    window.geometry('400x100')
    yes = False
    
    def url():
        url = urltext.get()
        
    def work():
        yes = True
        return yes
    urltext = Entry(window)
    urltext.place(x=100)
    URL = Button(window, text='Submit URL', command = url)
    URL.place(x=0, y=0, width = 100)
    if url != None:
        run = Button(window, text='Run', command = work)
        run.place(x=330, y=0)

           
window=Tk()

M2T = Button(window, text="Convert mp3 to text", fg='blue',command=mp3_to_text)
M2T.place(x=0, y=0, height=70, width=145)

S2T = Button(window, text="Live speech to text", fg='blue', command=live_text)
S2T.place(x=0, y=70, height=70, width=145)

S2T = Button(window, text="Youtube Vid to text", fg='blue', command=yt_text)
S2T.place(x=0, y=140, height=70, width=145)

FileText = Text(window)
FileText.insert(1.0, "Use 'View File' to see previous files here.")
FileText.place(x=145, y=0, height=630, width=830)

ViewFile = Button(window, text="View File", command = view_file)
ViewFile.place(x=165, y=645, height=30, width=90)

   
Exit = Button(window, text = "Exit", command = window.destroy)
Exit.place(x=0, y=630, height=70, width=145)

window.title('KeyWords')
window.geometry("1000x700+10+10")

window.lift()
window.mainloop()