from moviepy.editor import ImageClip, VideoFileClip, concatenate_videoclips, AudioFileClip, concatenate_audioclips
from moviepy.config import get_setting
from os.path import abspath
import subprocess
from format_clips import format_clip
from media_getter import is_img


def vid_from_media(vid_path, media, song_path, titles, img_duration = 8):
    clips = []
    print "sequencing media..."
    for m in media:
        print m.path
        if good_file(m.path):
            try:
                if is_img(m.path):
                    new_clip = ImageClip(m.path)
                    new_clip.fps = 1.0/img_duration
                    new_clip.duration = img_duration
                else:
                    new_clip = VideoFileClip(m.path)
                text = m.title if titles else None
                new_clip = format_clip(new_clip, text)
                clips.append(new_clip)
            except Exception as err:
                "COULDN'T CREAT CLIP BECAUSE: " + str(err)
        else:
            print 'CORRUPT FILE FOUND: ' + m.path + ', skipping.'
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
    vid.write_videofile(vid_path, progress_bar = False, preset = 'ultrafast')
    return abspath(vid_path)


#true if file is not corrupt
#have to do this check because VideoFileClip() hangs when getting data back from an ffmpeg call if it's given a corrupt gif
#this should be checked for every path so that more test cases can easily be added later
def good_file(path):
    if path.endswith('.gif'):
        proc = subprocess.Popen([get_setting("FFMPEG_BINARY"), '-i', path, '-f', 'null', '/dev/null'], stderr=subprocess.PIPE, shell = True)
        data = proc.communicate()[1]
        proc.terminate()
        if 'null @' in data:
            return False
    return True



if __name__ == "__main__":
    #add_border('images\\wide.jpg')
    #add_border('images\\fCcmquaDiv04b_ZoINPPe4CcC_VgXohw7QWzT9wqWFQa.png')
    #from meme import allFiles
    #vid_from_media('test.mp4', allFiles('test_media'), 'music\\0.452108414789.mp3')
    print good_file('fuckedgif.gif')
    print good_file('finegif.gif')








'''
def vid_from_imgs(vid_path, imgs, song_path, fps = 0.1):
    for i in imgs:
        add_border(i)
    print "sequencing images..."
    vid = ed.ImageSequenceClip(imgs, fps)
    print "getting song..."
    print song_path
    audio = ed.AudioFileClip(song_path)
    audio_loops = int(vid.duration/audio.duration) + 1 #times to loop audio
    audio = ed.concatenate_audioclips([audio] * audio_loops)
    print audio.duration
    print vid.duration
    audio = audio.set_duration(vid.duration)
    vid = vid.set_audio(audio)
    print "writing video..."
    vid.write_videofile(vid_path, progress_bar = False)
    return abspath(vid_path)


#adds a black border to the image at image_path so that the image has the specified aspect ratio
def add_border(img_path, aspect_ratio = (16,9)):
    print "adding border to " + img_path + "..."
    img = Image.open(img_path)
    img_ratio = float(img.height)/float(img.width)
    ideal_ratio = float(aspect_ratio[1])/float(aspect_ratio[0])
    ideal_size = tuple(v * 200 for v in aspect_ratio)
    if (img.width, img.height) != ideal_size:
        if img_ratio > ideal_ratio: #if we need to fix width
            print 'fixing width'
            black_border = Image.new("RGB", (int(img.height / ideal_ratio), img.height))
        elif img_ratio < ideal_ratio: #if we need to fix height
            print 'fixing height'
            black_border = Image.new("RGB", (img.width, int(img.width * ideal_ratio)))
        else: #if ratio is right and we just need to chage the size of the image
            black_border = Image.new("RGB", (img.width, img.height))
        black_border.paste(img, ((black_border.width - img.width)/2,
                            (black_border.height - img.height)/2)) #to put img in the center of black_border
        black_border = black_border.resize(ideal_size) #make sure everything is the exact right size
        black_border.save(img_path)
    return img_path
'''
    
