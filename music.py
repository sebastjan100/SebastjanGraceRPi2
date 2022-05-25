import youtube_dl
import requests
import pygame

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': 'music/song.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}


def predvajaj(currentLink, playing):
    data = requests.get("https://gracewebapp-sebastjantekavc.online404.repl.co/api/music/").json()

    # Ce dobimo nov komad, ga nalozimo in zacnemo predvajati
    if data['musicLink'] != currentLink:
        currentLink = data["musicLink"]
        musicTitle = data["musicTitle"]
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([currentLink])

        pygame.mixer.music.load("./music/song.mp3")
        pygame.mixer.music.play()

        playing = True
        print("download")
    # Ce na spletni strani ustavimo glasbo, na RPiju pa jo se vedno predvajamo
    if data['status'] != "playing" and playing:
        pygame.mixer.music.pause()
        playing = False
        print("stop playing")
        
    # Ce na spletni strani predvajamo glasbo, na RPiju pa je ne
    if data['status'] == "playing" and not playing:
        pygame.mixer.music.unpause()
        playing = True
        print("playing")

    return currentLink, playing, musicTitle


    