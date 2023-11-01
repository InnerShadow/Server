from moviepy.editor import VideoFileClip

class VideoPreprocer:
    def __init__(self):
        pass


    def get_video_duration(self, video_path : str):
        try:
            clip = VideoFileClip(video_path)
            duration = clip.duration
            clip.reader.close()
            return duration
        except Exception as e:
            return None
        
