class VideoFile:
    def __init__(self, filename):
        self.filename = filename

    def decode(self):
        print(f'decoding video file {self.filename}')
    
class AudioFile:
    def __init__(self, filename):
        self.filename = filename

    def decode(self):
        print(f'adding audio file {self.filename}')

class SubFile:
    def __init__(self, filename):
        self.filename = filename

    def decode(self):
        print(f'adding sub file {self.filename}')

class VideoPlayer():
    def __init__(self, video: VideoFile, audio: AudioFile, subtitle: SubFile):
        self.video = video
        self.audio = audio
        self.subtitle = subtitle

    def play(self):
        self.video.decode()
        self.audio.decode()
        self.subtitle.decode()

if __name__ == '__main__':
    player = VideoPlayer(VideoFile('movie.mp4'), AudioFile('audio.mp3'), SubFile('subtitle.txt'))
    player.play()