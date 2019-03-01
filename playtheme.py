import pygame
#from pygame import mixer
# pygame.init()
#mixer.init()
jesse = "Jesse"
nelson = "Nelson"
sang = "Sang"

root = "/home/pi/Development/raspi-sound-test/"
beat = root + "beat.mp3"
trap = root + "trap.mp3"
starwars = root + "starwars.mp3"
pygame.mixer.init()


def playTheme(name):
    #while True:
        #person = input()
    if name == sang:
        pygame.mixer.music.load(starwars)
        print("Itsa " + sang)
    if name == jesse:
        pygame.mixer.music.load(trap)
        print("Itsa " + jesse)
    else:
        pygame.mixer.music.load(starwars)
        print("Itsa " + nelson)
    
    pygame.mixer.music.play()
    
    #while pygame.mixer.music.get_busy() == True:
    #    continue
