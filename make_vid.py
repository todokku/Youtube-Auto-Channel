from moviepy import editor as ed
from PIL import Image
from os.path import abspath

#!YOU CAN PASS ImageSequenceClip A FOLDER!


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
    vid.write_videofile(vid_path)
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




if __name__ == "__main__":
    #add_border('images\\wide.jpg')
    #add_border('images\\fCcmquaDiv04b_ZoINPPe4CcC_VgXohw7QWzT9wqWFQa.png')
    import meme; vid_from_imgs(meme.allFiles('test_images'), 0.1)
    
