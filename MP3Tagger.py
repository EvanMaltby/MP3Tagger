import eyed3
from Tkinter import *
import tkFileDialog
from mutagen.mp3 import MP3
from mutagen.id3 import ID3,APIC,error
import Image,ImageTk
import os
import tkMessageBox

class App(Frame):
    """docstring for App"""
    def __init__(self, parent):
        #points to root
        self.parent = parent
        
        #checks to see if you've saved or not
        self.saved = False
        #the file of the .mp3
        self.file_name = None
        
        #declaring the eyed3 audio file
        self.eyed_audio_file = None

        #declaring the mutagen audio file
        self.mut_audio_file = None

        #options for the file dialog
        self.file_opt = options = {}
        options['defaultextension'] = '.mp3'
        options['filetypes'] = [('all files','.*') , ('music files','.mp3')]
        options['initialdir'] = '/home/paragon'
        options['initialfile'] = ''
        options['parent']=self.parent
        options['title']= 'Pick A Music File'


        #Create IU items
        #I/O code
        self.menubar = Menu(self.parent)
        self.file_menu = Menu(self.menubar,tearoff=0)

        self.file_menu.add_command(label="Open",command=self.Open)
        self.file_menu.add_command(label="Save",command=self.Save)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit",command=self.Exit)
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        #Album code
        self.album_label = Label(self.parent,text="Album:")
        self.album_entry = Entry(self.parent)

        #Artist code
        self.artist_label = Label(self.parent,text="Artist:")
        self.artist_entry = Entry(self.parent)

        #Title code
        self.title_label = Label(self.parent,text="Title:")
        self.title_entry = Entry(self.parent)

        #Track num code
        self.track_label = Label(self.parent,text="Track Number:")
        self.track_entry = Entry(self.parent)

        #Album Art code
        self.album_art_image = Image.open("unknown.gif")
        self.album_art_image_tk = ImageTk.PhotoImage(self.album_art_image)
        self.album_art_label = Label(self.parent,image=self.album_art_image_tk)
        self.album_art_label.image = self.album_art_image_tk

        #misc code
        self.length_label = Label(self.parent,text="Length: 0secs")
        self.bitrate_label = Label(self.parent,text="Bitrate: 0kps")

        self.initUI()

    
    def initUI(self):


        
        self.parent.config(menu=self.menubar)
        #Title code
        self.title_label.pack()
        self.title_label.place(x=300,y=30)

        self.title_entry.pack()
        self.title_entry.place(x=345,y=30)

        #Artist code
        self.artist_label.pack()
        self.artist_label.place(x=300,y=50)

        self.artist_entry.pack()
        self.artist_entry.place(x=340,y=50)


        #Album code
        self.album_label.pack()
        self.album_label.place(x=300,y=70)

        self.album_entry.pack()
        self.album_entry.place(x=348,y=70)


        #Track num code
        self.track_label.pack()
        self.track_label.place(x=300,y=90)

        self.track_entry.pack()
        self.track_entry.place(x=390,y=90,width=30)

        #Album Art code
        self.album_art_label.pack()
        self.album_art_label.place(x=-1,y=-1)

        #misc code
        self.length_label.pack()
        self.length_label.place(x=301,y=110)
        
        self.bitrate_label.pack()
        self.bitrate_label.place(x=301,y=130)


    def Open(self):

        #delete all the entrys for new data to be pulled
        self.title_entry.delete(0,END)
        self.artist_entry.delete(0,END)
        self.album_entry.delete(0,END)
        self.track_entry.delete(0,END)

        #open a file dialog allowing the user to open a file
        self.file_name = tkFileDialog.askopenfilename(**self.file_opt)

        #assign the file to the audio variables 
        self.eyed_audio_file = eyed3.load(self.file_name)
        self.mut_audio_file = MP3(self.file_name)
        
        #grab the album art and set it to the album label
        artwork = self.mut_audio_file.tags['APIC:'].data
        with open(self.eyed_audio_file.tag.title+".jpg","wb") as img:
            img.write(artwork)

        #insert all the mp3 meta data to the EntryTk
        self.title_entry.insert(END,self.eyed_audio_file.tag.title)
        self.artist_entry.insert(END,self.eyed_audio_file.tag.artist)
        self.album_entry.insert(END,self.eyed_audio_file.tag.album)

        #only shows the first 3 numbers of the length and the bitrate
        strbit = str(self.mut_audio_file.info.bitrate)
        self.length_label.configure(text="Length: " + str(int(self.mut_audio_file.info.length)) + "secs")
        self.bitrate_label.configure(text="Bitrate: " + str(strbit[0]) + "" + str(strbit[1]) + "" + str(strbit[2]) +"kps")


        #only grabs 2 first chars of the track number due to garabage info at the back
        if self.eyed_audio_file.tag.track_num[1] != None:
            self.track_entry.insert(END,str(self.eyed_audio_file.track_num[0]) + "" + str(self.eyed_audio_file.track_num[1]))
        else:
            self.track_entry.insert(END,str(self.eyed_audio_file.tag.track_num[0]))
        
        #resize the album art to fit the window
        self.album_art_image = Image.open(self.eyed_audio_file.tag.title+".jpg")
        im = self.album_art_image.resize((300,300),Image.NEAREST)
        im.save("newartwork.jpg")
        self.album_art_image = Image.open("newartwork.jpg")
        self.album_art_image_tk = ImageTk.PhotoImage(self.album_art_image)
        self.album_art_label.configure(image=self.album_art_image_tk)
        self.album_art_label = self.album_art_image_tk
        
         #reset the saver
        self.Save = False

        

    def Save(self):
        #shows you've saved
        self.Save = True
        #save the new meta-data to the mp3 
        self.eyed_audio_file.tag.title = unicode(self.title_entry.get())
        self.eyed_audio_file.tag.album = unicode(self.album_entry.get())
        self.eyed_audio_file.tag.artist = unicode(self.artist_entry.get())
        self.eyed_audio_file.tag.track_num = int(self.track_entry.get())
        self.eyed_audio_file.tag.save()

    def Exit(self):
        if self.Save == False:
            if tkMessageBox.askquestion('Are you sure?','You havent saved your current tags would you still like to quit?') == 'yes':                
                os.remove(os.path.dirname(__file__) + '/' + self.eyed_audio_file.tag.title + ".jpg")
                os.remove(os.path.dirname(__file__) + '/' + "newartwork.jpg")
                self.parent.quit()
        else:
                os.remove(os.path.dirname(__file__) + '/' + self.eyed_audio_file.tag.title + ".jpg")
                os.remove(os.path.dirname(__file__) + '/' + "newartwork.jpg")
                self.parent.quit()

def main():
  
    root = Tk()
    root.geometry("600x300")
    app = App(root)
    root.mainloop()  


if __name__ == '__main__':
    main()  

