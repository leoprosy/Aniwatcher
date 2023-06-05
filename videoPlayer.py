import vlc
from tkinter import *
from time import *

def player(videoSource, episode):
    root=Tk(className=str(episode))
    root.state('zoomed')

    def full(event):
        if root.attributes('-fullscreen'):
            root.attributes('-fullscreen', False)
        else:
            root.attributes('-fullscreen', True)
    
    def unfull(event):
        root.attributes('-fullscreen', False)
            
    def pause(event):
        if p.is_playing():
            p.set_pause(1)
        else: 
            p.play()
    
    def right(event):
        p.set_time(p.get_time()+15*1000)
    
    def left(event):
        p.set_time(p.get_time()-15*1000)
    
    root.bind("<Key-f>", full)
    root.bind("<Escape>", unfull)
    root.bind('<space>', pause)
    root.bind('<Right>', right)
    root.bind('<Left>', left)

    instance=vlc.Instance()
    p=instance.media_player_new()
    p.set_hwnd(root.winfo_id())
    p.set_media(instance.media_new(videoSource))
    p.play()

    root.mainloop()


# get_time()
# get_lenght()
# print("after" + strftime("%M:%S", gmtime(p.get_time()/1000)))