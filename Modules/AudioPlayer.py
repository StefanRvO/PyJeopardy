import vlc
import threading
import time
import queue
import traceback
import sys
class AudioPlayer:
    class _AudioPlayer:
        def __init__(self, qwidget = None):
            self.lock = threading.RLock()
            self.release_queue = queue.Queue()
            self.i = vlc.Instance()
            print(self.i)
            self.p = self.i.media_player_new()
            print(self.p)
            self.media = None
            self.release_thread = threading.Thread(target = self.release_thread)
            self.release_thread.daemon = True
            self.release_thread.start()
            self.q_widget = qwidget
            self.cnt = 0
            self.prev_media = {}

        def play_url(self, url, time):
            self.renew_player()
            self.p.set_mrl(url)
            self.p.play()
            #self.p.set_time(time)

        def play_file(self, filename, time):
            self.renew_player()
            try:
                self.media = self.prev_media[filename]
            except KeyError:
                self.media = self.i.media_new(filename)
                self.prev_media[filename] = self.media
            print(self.media)
            self.p.set_media(self.media)
            self.p.play()
            self.p.set_time(int(time) * 1000)

        def pause(self):
            self.p.set_pause(1)

        def play(self):
            self.p.set_pause(0)

        def stop(self):
            self.renew_player()

        def renew_player(self):
            if self.p:
                self.p.pause()
                self.release_queue.put(self.p)
                self.p = self.i.media_player_new()
                #We need to attach the player to a widget to prevent it from popping up.
                if self.q_widget:
                    self.p.set_xwindow(self.q_widget[self.cnt].winId())
                    self.cnt = (self.cnt + 1) % len(self.q_widget)


        def release_thread(self):
            next_release = None
            while(True):
                if next_release == None:
                    time.sleep(1)
                next_release = None
                if self.release_queue.qsize() <= 10:
                    continue
                next_release = self.release_queue.get()
                if next_release:
                    try:
                        print("releasing", next_release)
                        next_release.release()
                        print("released")
                    except:
                        traceback.print_exc()

    instance = None
    def __init__(self, q_widget = None):
        if AudioPlayer.instance == None:
            AudioPlayer.instance = AudioPlayer._AudioPlayer(q_widget)
    def __getattr__(self, name):
        return getattr(self.instance, name)





def main():
    a_player = AudioPlayer()
    a_player.play_url("https://r4---sn-bavc5ajvooxju-j2ie.googlevideo.com/videoplayback?id=7b474959f40717c6&itag=140&source=youtube&initcwndbps=3467500&pl=21&mv=m&pcm2cms=yes&ms=au&mm=31&mn=sn-bavc5ajvooxju-j2ie&ei=QU_-WOjwOJO2cNXjt_AM&ratebypass=yes&mime=audio/mp4&gir=yes&clen=3084133&lmt=1490924594491581&dur=194.142&key=dg_yt0&mt=1493061334&upn=9vratB8NogQ&signature=288D1AD2079A464D4B0ACDCCCFBFE455C4410563.61D724E784431335C287DBE959E6DCE1958B4F7C&ip=145.255.60.129&ipbits=0&expire=1493083042&sparams=ip,ipbits,expire,id,itag,source,initcwndbps,pl,mv,pcm2cms,ms,mm,mn,ei,ratebypass,mime,gir,clen,lmt,dur", 10000)


if __name__ == "__main__":
    main()
    while(True):
        pass
