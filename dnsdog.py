import pyinotify
import re
import os
import telegram


wm = pyinotify.WatchManager()
mask = pyinotify.IN_MODIFY
#set your token here
bot = telegram.Bot(token=str("__insert_token:here"))


class EventHandler (pyinotify.ProcessEvent):

    def __init__(self, file_path, *args, **kwargs):
        super(EventHandler, self).__init__(*args, **kwargs)
        self.file_path = file_path
        self._last_position = 0
        self.bot= bot

    def process_IN_MODIFY(self, event):
        print "File changed: ", event.pathname
        if self._last_position > os.path.getsize(self.file_path):
            self._last_position = 0
        with open(self.file_path) as f:
            f.seek(self._last_position)
            loglines = f.readlines()
            self._last_position = f.tell()
            for g in loglines:
                g = g.strip()
                #set your domain here
                if "cooking the response of type 'A'" in g:
                    if ".blind.your.domain" in g:
                        if "ns1.blind.your.domain" not in g:
                            try:
                            	#set chat_id here
                                self.bot.sendMessage(chat_id="@__chat_id", text=g)
                                print (g)
                            except:
                                try:
                                    print ('Telegramm error')
                                    sleep(5000);
                                    #set chat_id here
                                    self.bot.sendMessage(chat_id="@__chat_id", text=g)
                                    print (g)
                                except:
                                    print ('Telegramm crit error')
                                    print (g)
        size = os.path.getsize(self.file_path)
        if size > 50000:
       		print ('Log size bigger than the limit. Deleting log.')
       		open(self.file_path, 'w').close()
                                


#Set path to dnschefs log here
handler = EventHandler('/path/to/dns_query.log')
notifier = pyinotify.Notifier(wm, handler)

wm.add_watch(handler.file_path, mask)        
notifier.loop()
