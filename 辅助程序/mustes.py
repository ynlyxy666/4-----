from pygame import mixer

mixer.init()
mixer.music.load("bgm.ogg")
mixer.music.play(-1)
mixer.music.set_volume(0.5)
