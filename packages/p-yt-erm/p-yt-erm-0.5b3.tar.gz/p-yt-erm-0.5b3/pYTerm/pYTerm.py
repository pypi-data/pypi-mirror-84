#!/usr/bin/python3
"""

					player
		Python YouTube Terminal (player)

	commandline tool to play youtube audio easily
		https://gitlab.com/mocchapi/pyterminal

			  made by anne & lynice


(ytdl is a lil fucky rn so excuse any weird logging kthx)

"""
from pathlib import Path

source_path = Path(__file__).resolve()
source_dir = str(source_path).replace('player', '')
# gets the realsies path so the debug file doesnt get put innthe current dir
# did the janky string thing because windows uses \ instead of / and i hate it and dont want to deal with it

import os
import vlc
import re
import time
import sys
import datetime
import random
import pafy

try:
    from pypresence import Presence
except Exception as e:
    print(f'"{e}", discord rich presence wont work')

import requests
import json
from bs4 import BeautifulSoup
# just look at all these imports wow
# also bs4 is a dependency now :::::) -a
from importlib import metadata
import threading
import argparse
import logging
import warnings

warnings.filterwarnings("ignore")  # gets rid of bs4 complaints

# TODO:
# improved logging should be the next focus
# improve logging and add more use of it(and also make different language outputs)
# add function to more easily use mutliple langauge return functions
# clean logging file up and seperate vlc and ytdl logging into other files
# lynice to learn more about french verbs and culutral things to do localisation and just to learn and imrpove really
# impossible to debug everything before goign to bed, rule of thumb is if something double prints, forgot a else case, was gonna explain more but lost train fo thougth um
# a dict of common additions on youtube videos to be removed from the title string on rich presence -a
# couldve just made this a list but i guess its handy for future proofing?
# gay
replaceDict = {
    '\\(': '',
    '\\)': '',
    '\\[': '',
    '\\]': '',
    '\\"': '',
    "\\'": '',
    'official music video': '',
    'lyrics': '',
    'lyric video': '',
    ' - topic': '',
}


def getRecommended(url, tries=5):
    for i in range(0, tries):
        try:
            soup = BeautifulSoup(requests.get(url, headers={
                'User-Agent': 'Mozilla/5.0 (Android 4.4; Mobile; rv:41.0) Gecko/41.0 Firefox/41.0'}).text)
            jsono = soup.find_all(id='initial-data')[0]
            data = json.loads(str(jsono.string))
            return 'https://www.youtube.com/watch?v=' + \
                   data["contents"]["singleColumnWatchNextResults"]["results"]["results"]["contents"][3][
                       "itemSectionRenderer"]["contents"][0]["compactAutoplayRenderer"]["contents"][0][
                       'compactVideoRenderer']['videoId']
        
        except BaseException as e:
            pass


def updateRPC(RPC, title, timestamp, channel, version):
    # this updates rich presence & formats the title into one of several possible formats, depending on which is possible -a
    if title.find(' - ') > -1:
        # uses the common "artist - songname" title format to get real artist & songname
        titleList = title.split(' - ')
        title = reIncDict(' '.join(titleList[1:]), replaceDict)
        artist = titleList[0]
    
    elif title.find(' by ') > -1:
        # way less common but occasionally some titles will have "songname by artist"
        titleList = title.split(' by ')
        title = reIncDict(' '.join(titleList[:-1]), replaceDict)
        artist = titleList[-1]
    
    else:
        # if all else fails, simply use the name of the channel who uploaded the video
        # songname will be the full video title
        # this is both a fallback and support for youtube-music songs
        title = reInc(title, channel, '')
        artist = reIncDict(channel, replaceDict)
    timestamp = f'{timestamp[0]}/{timestamp[1]}'
    
    # put the version number as pop up text in the big icon of the rich presence bop -a
    RPC.update(details=title, state=f'by {artist}', large_image="logo-2", small_image='clock', small_text=timestamp,
               large_text=version)


def reIncDict(text, replaceDict):
    # runs reInc with a dictionary to make it easier to remove a bunch of things from the rich presence title string
    # added this because i kept chaining reInc and it was getting too long -a
    for item in replaceDict:
        text = reInc(str(text), str(item), str(replaceDict[item]))
    return text


def reInc(text, replacethis, withthis):
    # replaces x with y in a string but ignores case sensitivity
    # this only exists because python's .replace() doesnt have a case-insensitive option -a
    
    return re.sub(replacethis, withthis, text, flags=re.IGNORECASE)


def milForm(milliseconds, subtractH=True):
    # this function formats a miliseconds time int into a nice [HH*:MM:SS] format
    # only does HH if its required (time is longer than 59:59) -a
    
    # for some reason it adds 1 hour on my system and idk why it should do that
    # so i added subtractH so it subtracts 1h from the time
    # if it errors (because on windows it doesnt seem to add an hour?) itll not subtract an hour so
    # no matter what you get a clean and true return -a
    try:
        if subtractH:
            millisecondos = milliseconds - 3600000
        if millisecondos > 3600000:
            return datetime.datetime.fromtimestamp(millisecondos / 1000).strftime('%H:%M:%S')
        else:
            return datetime.datetime.fromtimestamp(millisecondos / 1000).strftime('%M:%S')
    
    except:
        try:
            millisecondos = milliseconds
            if millisecondos > 3600000:
                return datetime.datetime.fromtimestamp(millisecondos / 1000).strftime('%H:%M:%S')
            else:
                return datetime.datetime.fromtimestamp(millisecondos / 1000).strftime('%M:%S')
        except:
            return '?'


def getRPC(rpc_id):
    """(i made this, complain to me if it doesnt work) -a
    # mofidied version of lynices getClientID
    # will return rich presence object instead of ID
    # returns None on faillure"""
    # u spelt failurre wrong anne
    
    # i gutted this function to make it easier to understand but now its just 3 lines so might just remove this function -a
    RPC = Presence(rpc_id)
    RPC.connect()
    return RPC


def prevLine():
    sys.stdout.write("\033[F")


def clrLine():
    sys.stdout.write("\033[K")


def clrPrevLine():
    prevLine()
    clrLine()


# dangling logging defintion, idk what to do with it lol
# also the various logging levels are all a blob in my head so we are using debug \(=^w^=)/
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(message)s \nthread_id: %(thread)d\n',
                    datefmt='%d/%m/%y  %I:%M:%S %p',
                    handlers=[logging.FileHandler(source_dir + 'pytermDEBUG.log', encoding='utf-8')])


# happy to help with logging more if you want, i actually really enjoy it for some reaosn
# also might be good to always create the log file and have things write to it no matte r what so people dont have
# to either anticipate errors or try to recreate a random bug with debug ON -l


def debugoutput(tofile='', toconsole=''):
    """a function to call to simultaenously send console error message
    and file error message. most usage of this command will be directed to
    `file` unless we specifically want the user to see it
    added verb 'to' at the beginning to avoid cluttering variables/bugging with namespaces/overloading? """
    try:
        if toconsole != '':
            print(toconsole)  # was going to use stderr but im not too familiar using it in python and im scared -l
        if tofile != '':
            logging.debug(tofile)
    # improve this function to make more dynamic and conveinet
    except PermissionError:
        pass


# main class
class player():
    # some general info to keep track of
    # dont forget to update this lol -a
    
    __VERSION_BRANCH = 'rewrite'  # r for rewrite -a
    
    # A brief explaination of what i'm doing here, Basically it trys grabbing the version from the package data if it was installed from pip.
    #  then it will try grabbing the commit hash of what its running from git. If all else fails it just says "unknown".
    __VERSION_NUMBER = ""
    try:
        __VERSION_NUMBER = metadata.version("p-yt-erm")
    except metadata.PackageNotFoundError:
        try:
            import subprocess
            hash = subprocess.run(['git', 'rev-parse', '--short', 'HEAD'], stdout=subprocess.PIPE)
            __VERSION_NUMBER = str(hash.stdout)[2:9]
        except FileNotFoundError:
            __VERSION_NUMBER = "unknown/inconnue"

    __AUTHORS = ['Anne', 'lynice <lynhxano@gmail.com>']
    
    NOTICE = f"""
    __     _________
    \\ \\   / /__   __|
  _ _\\ \\_/ /   | | ___ _ __ _ __ ___
 | '_ \\   /    | |/ _ \\ '__| '_ ` _ \\
 | |_) | |     | |  __/ |  | | | | | |
 | .__/|_|     |_|\\___|_|  |_| |_| |_|
 | | "{__VERSION_BRANCH}" {__VERSION_NUMBER}
 |_| created by {" & ".join(__AUTHORS)}"""
    NOTICEFR = f"""
    __     _________
    \\ \\   / /__   __|
  _ _\\ \\_/ /   | | ___ _ __ _ __ ___
 | '_ \\   /    | |/ _ \\ '__| '_ ` _ \\
 | |_) | |     | |  __/ |  | | | | | |
 | .__/|_|     |_|\\___|_|  |_| |_| |_|
 | | "{__VERSION_BRANCH}" {__VERSION_NUMBER}
 |_| développés par {" & ".join(__AUTHORS)}"""
    
    def __init__(self, richPresenceID=True, quiet=False, debug=False,
                 vlclogs=False, forceaudiostream=True, wait=True, allowInput=True,
                 songs=None, playlistFile=None, shuffle=False, loop=False, volume=100, fr=False, autoplay=False):
        """all options are initialised here"""
        
        # forceaudiostream uses the youtube audiostream instead of loading the entire video, should reduce data usage and increase audio quality?
        # this is an option because playing "youtube music" videos gives a bunch of errors
        # these "videos" are the ones YT Music uses and are automatically generated it seems -a
        self.forceaudiostream = forceaudiostream
        
        # loop will infinitely loop the music player until exited -a
        self.loop = loop
        # shuffle will shuffle the playlist ONCE when .go() is called
        # maybe there should be a way to shuffle again if loop is on? -a
        self.shuffle = shuffle
        
        # different levels of feedback printing
        # TODO printing should be replaced by the logging module -a
        self.quiet = quiet
        self.debug = debug
        self.fr = fr
        # discord rich presence, will check if it is useable here too
        # richPresenceID can be one of three things:
        # True -> player will use the inbuilt client id
        # False -> player will not use rich presence
        # a discord client ID of type int -> will use supplied client id over inbuild one
        self.richPresenceID = richPresenceID
        if self.richPresenceID:
            if self.richPresenceID == True:
                self.richPresenceID = '737813623967318077'
            try:
                self.RPC = getRPC(self.richPresenceID)
                self.RPC.update()
            except Exception as e:
                debugoutput(tofile='Error initialising rich presence, make sure discord is opened!',
                            toconsole='Error initialising rich presence, make sure discord is opened! / erruer: est discord ouvert?')
                self.RPC = None
        else:
            self.RPC = None
        if self.RPC == None and self.richPresenceID:
            self.richPresence = False
            debugoutput(tofile='Could not connect to discord, Rich Presence disabled.',
                        toconsole='Could not connect to discord, Rich Presence disabled. n\'a pas pu se connecter a discord')
        
        # disables vlc logging since its very annoying and would clog up stdout
        if not vlclogs:
            os.environ['VLC_VERBOSE'] = '-1'
        # defaults set at the start which the user has no input on
        self.vlcInstance = vlc.Instance('--no-video', 'vout=none')
        self.vlcPlayer = self.vlcInstance.media_player_new()
        # internal volumeLvl to 100 just in case
        self._volumeLvl = volume
        self._trgtVol = volume
        self.vlcPlayer.audio_set_volume(self._volumeLvl)
        self._playingUrl = None
        self.playList = []
        self.playListIndex = 0
        self.streamInfo = None
        self.quiet = False
        
        self.autoplay = autoplay
        # enables recommended videos to be added to the queue if it runs out
        
        self.pendingAction = False
        # this communicates to the go() function if it should increase the playlist index after the song ends
        # if True it will do nothing
        # this is used in next() and previous() so it doesnt mess up
        
        # determines if playing a song should halt the program -a
        self.wait = wait
        # TODO figure out how to do input again (threading? would that work?)
        self.allowInput = allowInput
        
        self.addSong(songs, file=playlistFile)
        
        if self.debug:
            print('richPresence:', self.richPresenceID)
            print('vlclogs:', vlclogs)
            print('forceaudiostream:', self.forceaudiostream)
            print('wait:', self.wait)
            print('allowInput:', self.allowInput)
            print('shuffle:', self.shuffle)
            print('loop:', self.loop)
    
    # too much of a mess for me to bother with setting up logging proper
    
    def go(self):
        """starts playing music and iteration trhough the playlist
        starter function for __go__()
        if we are told not to halt execution we'll start __go__ as a thread
        otherwise just call it -a"""
        if len(self.playList) == 0:
            return
        
        if self.shuffle:
            random.shuffle(self.playList)
        
        if self.allowInput:
            y = threading.Thread(target=self.runInput, daemon=True)
            y.start()
        
        if self.wait:
            self.__go__()
        else:
            x = threading.Thread(target=self.__go__, daemon=True)
            x.start()
    
    def pause(self):
        self._trgtVol = self._volumeLvl
        self.setVolume(0, report=False)
        # sets pause state to "1" meaning "paused" in vlc -a
        self.vlcPlayer.set_pause(1)  # i have no idea whats going on with pause so i simply will not touch it -lynice
    
    # thanks anne love u too
    
    def unpause(self):
        """does the same as above, but sets it to "0" meaning "playing" -a"""
        self.vlcPlayer.set_pause(0)
        self.setVolume(self._trgtVol, report=False)
    
    def togglepause(self, report=True):
        if str(self.vlcPlayer.get_state()) == 'State.Playing':
            self.pause()
            if self.fr:
                if report and not self.quiet: print('en pause')
            else:
                if report and not self.quiet: print('paused')
        # instead of the if/else we can just do
        # if report and not self.quiet: return lang["pausetext"]
        # in the french and english dict wed define pausetext as 'en pause' and 'paused respectively'
        elif str(self.vlcPlayer.get_state()) == 'State.Paused':
            self.unpause()
            if self.fr:
                if report and not self.quiet: print('sans pause')
            else:
                if report and not self.quiet: print('unpaused')
        else:
            debugoutput(tofile="pause/unpause failed, likely caused by bad data")
    
    def stop(self):
        self.unpause()
        self.playListIndex = len(self.playList)
        self.loop = False
        self.setVolume(0, fadeTime=0, report=False)
        self.vlcPlayer.stop()
    
    def skip(self):
        """alias for next()"""
        self.next()
    
    def next(self):
        """play next song"""
        self._trgtVol = self._volumeLvl
        self.setVolume(0)
        self.vlcPlayer.stop()
        while not self.isVlcAlive():
            time.sleep(0.05)
        self.setVolume(self._trgtVol)
    
    def previous(self):
        """play previous song"""
        self._trgtVol = self._volumeLvl
        self.setVolume(0)
        self.pendingAction = True  # ALSO STICK UPDATE SDFKJHGLDSFLKJ???? HUH
        self.playListIndex -= 1
        self.vlcPlayer.stop()
        while not self.isVlcAlive():
            time.sleep(0.05)
        self.setVolume(self._trgtVol)
    
    def movePlayhead(self, val):
        """moves current timestamp back or forth, depending if val is a positive int or a negative int"""
        self.vlcPlayer.set_time(player.vlcPlayer.get_time() + (int(val)) * 1000)
    
    def playAtIndex(self, index, report=True):
        if not -1 > index - 1 and not index > len(self.playList):
            self.pendingAction = True
            self.vlcPlayer.stop()
            self.playListIndex = index - 1
            if not self.quiet and report: print(f'Playing song at index {index}')
        else:
            if not self.quiet and report: print('Index out of range')
    
    # self.playSong(self.playList[index])
    
    def runInput(self, loop=True):
        """handles the input if enabled"""
        
        if self.fr == True:
            print(
                'contrôles : [v]olume, [s]auter, [préc]édent, [p]ause, [d]ésplacer, [h]orodatage, [sort]ir')  # dont think sauter should be used in this context but it fits lmao
        else:
            print('Controls: [v]olume,[s]kip,[prev]ious,[p]ause,[m]ove,[t]imestamp,[g]oto,[e]xit')
        while loop:
            try:
                raw = input('')
                clrPrevLine()
                if ' ' in raw:
                    cmd = raw.split(' ')[0]
                    opt = raw.split(' ')[1]
                else:
                    cmd = raw
                    opt = ''
                
                # change volume (with fade)
                # i dont think fade works
                
                if cmd == 'v' or cmd == 'volume':
                    print('          -> ', end='')
                    self.setVolume(opt, report=True)
                    prevLine()
                
                # skips
                elif cmd == 's' or cmd == 'skip' or cmd == 'next' or cmd == 'sauter' or cmd == 'passer':
                    self.next()
                
                
                # previous
                elif cmd == 'previous' or cmd == 'prev' or cmd == 'préc' or cmd == 'prec' or cmd == 'precedent' or cmd == 'précédent':
                    self.previous()
                
                # pauses/resumes depending on state
                elif cmd == 'pause' or cmd == 'play' or cmd == 'resume' or cmd == 'p' or cmd == 'jouer' or cmd == 'reprendre' or cmd == 'a' or cmd == 'arrêter' or cmd == 'arreter':
                    print('          ->', end='')
                    self.togglepause()
                    prevLine()
                
                elif cmd == 'm' or cmd == 'move' or cmd == 'désplacer' or cmd == 'desplacer' or cmd == 'd':
                    try:
                        self.movePlayhead(opt)
                        print(f'          -> moved {opt}s')
                    except:
                        print('          -> usage: "m SECONDS" or "m -SECONDS"')
                    prevLine()
                
                elif cmd == 't' or cmd == 'timestamp':
                    timestamp = self.getFancyTimeStamp()
                    print(f'          -> {timestamp[0]}/{timestamp[1]}')
                    prevLine()
                
                elif cmd == 'g' or cmd == 'goto':
                    print('          -> ', end='')
                    self.playAtIndex(int(opt))
                    prevLine()
                
                # exits the player
                elif cmd == 'e' or cmd == 'exit' or cmd == 'stop':
                    self.stop()
                else:
                    print('          ->', f'unknown command "{cmd}"')
                    prevLine()
            except:
                pass
    
    def addRecommended(self, tries=10):
        url = self.streamInfo.get('YTurl')
        
        print('Looking for autoplay songs...')
        prevLine()
        for i in range(0, tries):
            newsong = getRecommended(url)
            if newsong == None:
                print(f'No results...      [{i}]        ')
                prevLine()
                continue
            
            elif newsong in self.playList:
                print(f'Already in list... [{i}]            ')
                prevLine()
                url = newsong
                continue
            self.playList.append(newsong)
            return
        print('Couldnt find any autoplay songs, sorry :(')
    
    def getFancyTimeStamp(self):
        # returns a formatted timestamp in a tuple -a
        return milForm(self.vlcPlayer.get_time()), milForm(self.vlcPlayer.get_length())
    
    def isVlcAlive(self):
        """returns true if vlc is either paused or playing"""
        if str(self.vlcPlayer.get_state()) == 'State.Playing' or str(self.vlcPlayer.get_state()) == 'State.Paused':
            return True
        else:
            return False
    
    def addSong(self, song=None, file=None):
        # add song(s) to playlist
        if song is None and file is None:
            debugoutput(tofile="no song")
            return
        
        # song can be either str or list containing str
        if type(song) == str:
            self.playList.append(song)
        elif type(song) == list:
            self.playList = self.playList + song
        else:
            debugoutput(tofile="didnt use valid data type")
        
        # if "file" is supplied, load a playlist from a file
        if type(file) == str:
            with open(file, 'r') as f:
                self.playList = self.playList + f.read().split('\n')
        elif type(file) == list:
            for item in file:
                with open(item, 'r') as f:
                    self.playList = self.playList + f.read().split('\n')
        else:
            debugoutput(tofile="didnt use valid data type (playlist file)")
    
    def playSong(self, query):
        # plays da songs
        # query can be either just a string of search terms or a string of a youtube video url
        # yt playlists coming 2021 -a
        # was gonna add logging but got scared away by the code, really got baited by the func name
        while self.isVlcAlive():
            time.sleep(.05)
        # Todo: add a way to play a youtube url -a <<< done -a
        # shouldnt this be built into vlc's api like,,, it just workss,,,
        # idk -a
        if query.startswith('https://'):
            pafyvid = self.__getPafyVideo__(query)
        else:
            pafyvid = self.__search__(query)
        
        if pafyvid is None:
            print(f'Couldnt find video "{query}"')
            return
        stream = self.__getStream__(pafyvid)
        
        self._playingUrl = stream.url
        self.streamInfo = {'title': pafyvid.title, 'channel': pafyvid.author, 'duration': pafyvid.duration,
                           'YTurl': 'https://youtube.com/watch?v=' + pafyvid.videoid}
        if self.streamInfo['duration'].startswith('00:'):
            self.streamInfo['duration'] = self.streamInfo['duration'][3:]
        
        url = self._playingUrl
        if not self.quiet: print(
            f"""playing [{self.playListIndex + 1}/{len(self.playList)}] "{self.streamInfo["title"]}" by {self.streamInfo["channel"]} [{self.streamInfo["duration"]}]""")
        
        if url:
            self.__vlcplay__(url)
            while not self.isVlcAlive():
                time.sleep(.05)
            del url
        else:
            return
    
    def setVolume(self, volumenum, report=False, fadeTime=0.5, fadeInterval=2):
        # changes volume
        
        # dont change volume if it hasnt changed OR is lower than 0 or Too Fucking Loud
        try:
            volumenum = int(volumenum)
        except:
            if report and not self.quiet: print(f'"{volumenum}" is not a number')
        if volumenum < 0 or volumenum > 200 or volumenum == self._volumeLvl:
            if self.fr:
                if report and not self.quiet: print('volume inchangé')
            else:
                if report and not self.quiet: print('volume not changed')
        else:
            if fadeTime:
                if volumenum > self._volumeLvl:
                    fadedelay = fadeTime / (volumenum - self._volumeLvl)
                    for i in range(self._volumeLvl, volumenum, fadeInterval):
                        self.vlcPlayer.audio_set_volume(i)
                        time.sleep(fadedelay)
                else:
                    fadedelay = fadeTime / (self._volumeLvl - volumenum)
                    for i in range(self._volumeLvl, volumenum, -fadeInterval):
                        self.vlcPlayer.audio_set_volume(i)
                        time.sleep(fadedelay)
            
            self._volumeLvl = volumenum
            self.vlcPlayer.audio_set_volume(self._volumeLvl)
            
            if self.fr:
                if report and not self.quiet: print(f'volume changé en {volumenum}')
            else:
                if report and not self.quiet: print(f'volume changed to {volumenum}')
    
    # time.sleep(1.2)
    # print("\033[A", "\033[K")#clears clutter when done, may cause errors in poor terminals
    # ^ this seems to leave a bunch of empty lines after input -a
    
    # functions the user shouldnt call, will be availible through/used by other functions
    def __go__(self):
        """this is __go__ because self.go() will decide if this runs as a thread or not, so calling it directly wouldnt work -a
        # actually it /would/ work but you /shouldnt/ because self.go() handles some other stuff -a"""
        # i dont think she knows how to make docstrings ghdfkjhgfdslkjds
        # i like # more
        # also this isnt really good documentation so ¯\_(ツ)_/¯
        
        # main playlist function
        # this will play the current list index instead of using a for loop
        # so we can travel to any point in the playlist at will
        while self.playListIndex < len(self.playList) or self.loop:
            if self.playListIndex >= len(self.playList): self.playListIndex = len(self.playList) - 1
            self.playSong(self.playList[self.playListIndex])
            
            while self.isVlcAlive():
                if self.richPresenceID:
                    try:
                        updateRPC(self.RPC, self.streamInfo["title"], self.getFancyTimeStamp(),
                                  self.streamInfo["channel"], self.__version__)
                    except:
                        pass
                time.sleep(.5)
            
            if self.autoplay and self.playListIndex + 1 == len(self.playList):
                self.addRecommended()
            if not self.pendingAction:
                self.playListIndex += 1
            else:
                self.pendingAction = False
    
    def __vlcplay__(self, url):
        """this is like, low level ish and is pretty much worthless to outside users -a"""
        
        # tbh not entirely sure what all of this is -a
        self.media = self.vlcInstance.media_new(url, 'vout=none', '--no-video')
        self.vlcPlayer.set_media(self.media)
        self.vlcPlayer.play()
        self.counter = 0
        while self.vlcPlayer.is_playing() == False or self.counter > 160:
            time.sleep(.05)
            self.counter += 1
        del self.counter
        self.vlcPlayer.audio_set_volume(self._volumeLvl)
    
    def __getPafyVideo__(self, url):
        for i in range(0, 5):
            try:
                x = pafy.new(url)
                if self.debug:
                    print(dir(x))
                    print(x.audiostreams)
                    print(x.streams)
                return x
            except BaseException as e:
                # print(e)
                pass
    
    def __getStream__(self, pafyObj):
        if self.forceaudiostream:
            stream = pafyObj.getbestaudio(preftype='m4a')
        else:
            stream = pafyObj.streams[0]
        return stream
    
    def __search__(self, query, maxresults=2):
        """this should get rewritten at some point hmmm, kinda messy -a
        # tried to clean it up, succeeded somewhat kinda -a"""
        
        results = YoutubeSearch(query, maxresults=maxresults)
        if self.debug: print(f'SEARCHING FOR SEARCH TERMS {query}')
        if results is None:
            return None
        for item in results:
            try:
                pafyvid = self.__getPafyVideo__(item)
                # if not self.quiet: print(f"""playing [{self.playListIndex+1}/{len(self.playList)}] "{streamInfo["title"]}" by {streamInfo["channel"]} [{streamInfo["duration"]}]""")
                # return self._playingUrl
                return pafyvid
            except BaseException as e:
                print(e)


def YoutubeSearch(query, maxresults=5):
    # ill comment this some other time but tldr im tricking yt again into giving us json
    url = 'https://m.youtube.com/results?search_query=' + '+'.join(query.split(' '))
    try:
        soup = BeautifulSoup(requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Android 4.4; Mobile; rv:41.0) Gecko/41.0 Firefox/41.0'}).text)
        # swag = soup.prettify
        output = []
        result = soup.find_all(id='initial-data')[0]
        data = json.loads(str(result.string))
        things = data["contents"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"]
        try:
            things = things[:maxresults]
        except:
            pass
        for item in things:
            try:
                output.append('https://www.youtube.com/watch?v=' + item['compactVideoRenderer']['videoId'])
            except:
                pass
        return output
    except BaseException as e:
        return None


def parseargs():
    # done:
    # 	richPresenceID=True,songs=None,playlistFile=None,shuffle=False,loop=False,allowInput=True,vlclogs=False,forceaudiostream=True,debug=False
    # to add:
    #	quiet=False,
    # wont add:
    # 	wait=True,
    parser = argparse.ArgumentParser(
        description="Play youtube audio from the commandline / écouter l'audio des vidéos youtube sur la ligne de commande")
    parser.add_argument('--version', help='prints version / version imprimé', action='store_true')
    parser.add_argument('-v', '--volume',
                        help='starts with <value> volume / le programme démarrer avec un niveau de volume <value>',
                        action='store', type=int, default=100)
    parser.add_argument('-l', '--loop', help='enable playlist looping', action='store_true')
    parser.add_argument('-s', '--shuffle', help='enable playlist shuffling', action='store_true')
    parser.add_argument('-a', '--autoplay', help='enable automatically playing recommended songs based on the playlist',
                        action='store_true')
    parser.add_argument('-p', '--playlist', help="use playlist file / utiliser une playlist à partir d'un fichier",
                        action='append', type=str)
    parser.add_argument('-rp', '--richpresence',
                        help='either False to disable RP, True or a rich presence ID string to enable', action='store',
                        default=True)
    parser.add_argument('-ni', '--noinput', help='disables player controls / désactiver les contrôles',
                        action='store_true')
    parser.add_argument('-as', '--audiostream',
                        help='forces the use of audio streams, reduces bandwith and might increase quality at the cost of stability',
                        action='store_true')
    parser.add_argument('--verbose', help='enable verbose logging', action='store_true')
    parser.add_argument('-vl', '--vlclogs', help='enable vlc logging', action='store_true')
    parser.add_argument('songs', help='name of the song you want to play / nom de la chanson à jouer tu veux jouer',
                        action='store', type=str, nargs=argparse.REMAINDER)
    parser.add_argument('--fr', help='enable french output / activer mode français', action='store_true')
    # i have no idea how argparser works so honestly, its messier but might just fork with a translation hkjhdglkdsfjh -l
    return parser.parse_args()


# This function is what gets run whenever player is being rubn in a CLI setting.
def commandline():
    # this is where the stuff related to running the file instead of importing it will go
    # there shouldnt be too much here
    
    # collect arguments
    args = parseargs()
    # if args.verbose: print(args)
    
    if args.richpresence == 'True':
        args.richpresence = True
    elif args.richpresence == 'False':
        args.richpresence = False
    
    # prints the version notice if --version is supplied
    if args.version:
        if args.fr:
            print(player.NOTICEFR)
        else:
            print(player.NOTICE)
        exit()
    
    # gets the player object with all the arguments
    playerinuse = player(debug=args.verbose, volume=args.volume, richPresenceID=args.richpresence,
                         forceaudiostream=args.audiostream, allowInput=not args.noinput, vlclogs=args.vlclogs,
                         loop=args.loop, shuffle=args.shuffle, songs=args.songs, playlistFile=args.playlist, fr=args.fr,
                         autoplay=args.autoplay)
    # launches the player
    playerinuse.go()


if __name__ == '__main__':
    commandline()
