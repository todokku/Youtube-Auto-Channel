from moviepy.editor import ImageClip, VideoFileClip, concatenate_videoclips, AudioFileClip, concatenate_audioclips
from os.path import abspath
from format_clips import format_clip
from media_getter import is_img


def vid_from_media(vid_path, media, song_path, titles, img_duration = 8):
    clips = []
    print "sequencing media..."
    for m in media:
        print m.path
        if is_img(m.path):
            new_clip = ImageClip(m.path)
            new_clip.fps = 1.0/img_duration
            new_clip.duration = img_duration
        else:
            new_clip = VideoFileClip(m.path)
        text = m.title if titles else None
        new_clip = format_clip(new_clip, text)
        clips.append(new_clip)
    vid = concatenate_videoclips(clips)
    print song_path
    audio = AudioFileClip(song_path)
    audio_loops = int(vid.duration/audio.duration) + 1 #times to loop audio
    audio = concatenate_audioclips([audio] * audio_loops)
    print audio.duration
    print vid.duration
    audio = audio.set_duration(vid.duration)
    vid = vid.set_audio(audio)
    print "writing video..."
    vid.write_videofile(vid_path, progress_bar = False, preset = 'ultrafast', threads = 2)
    return abspath(vid_path)



if __name__ == "__main__":
    from meme import allFiles
    vid_from_media('test.mp4', allFiles('test_media'), 'music\\0.452108414789.mp3')
    
