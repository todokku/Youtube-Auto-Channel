from moviepy.video import fx
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip


#adds newlines to text so that it is never wider than max_len
#if possible, it adds newlines in such a way so that words aren't broken in half
def _add_newlines(text, max_len):
        new_text = ''
        spot = 0
        while spot < len(text):
            substr = text[spot: spot + max_len]
            last_space = substr.rfind(' ')
            if len(substr) == max_len:
                if last_space != -1:
                    new_text += substr[:last_space] + '\n'
                    spot += last_space + 1 #+1 to go 1 past the space
                else:
                    new_text += substr + '\n'
                    spot += max_len
            else:
                new_text += substr
                break
        if new_text[-1] == '\n':
            new_text = new_text[:-1]
        return new_text
    

# return VideoClip resized, bordered and with text
def format_clip(clip, text=None, text_pos='bottom', fontsize = 60 , ideal_size = (1920,1080), max_text_len = 45):
    
    if type(clip) == str:
        clip = VideoFileClip(clip)

    text_height = 0
    if text != None and text_pos != None:
        text = _add_newlines(text, max_text_len)
        t = TextClip(
                        txt=text,fontsize=fontsize,color='white'
                     ).set_pos(('center',text_pos)).set_duration(clip.duration).set_fps(clip.fps)
        text_height = t.size[1]
    if text_pos == 'top':
        bot_text_margin = 0
        top_text_margin = text_height
    elif text_pos == 'bottom':
        bot_text_margin = text_height
        top_text_margin = 0
    else:
        raise ValueError('invalid text position')
        
    clip_ratio = float(clip.size[0])/float(clip.size[1])
    ideal_ratio = float(ideal_size[0])/float(ideal_size[1]-text_height)

    if clip_ratio < ideal_ratio: #scale so height fits
        scaled_clip = fx.all.resize(clip,height = ideal_size[1]-text_height)
        margin_width = (ideal_size[0] - scaled_clip.size[0])//2
        bordered_clip = fx.all.margin(scaled_clip,
                                        bottom = bot_text_margin,
                                        left = margin_width,
                                        right = ideal_size[0] - margin_width - scaled_clip.size[0], # right is ~= margin_width, set to size needed to make resolution exactly desired
                                        top = top_text_margin)
        
    elif clip_ratio > ideal_ratio: #scale so width fits
        scaled_clip = fx.all.resize(clip,width = ideal_size[0])
        margin_height = (ideal_size[1] - text_height - scaled_clip.size[1])//2
        bordered_clip = fx.all.margin(scaled_clip,
                                        top = top_text_margin + margin_height,
                                        bottom = bot_text_margin + ideal_size[1] - text_height - margin_height - scaled_clip.size[1]) # bottom is ~= margin_height, set to size needed to make resolution exactly desired

    else: #perfect ratio - scale so height & width fit
        scaled_clip = fx.all.resize(clip,newsize=ideal_size)
        bordered_clip = fx.all.margin(scaled_clip,
                                       top = top_text_margin,
                                       bottom = bot_text_margin) # bottom is ~= margin_height, set to size needed to make resolution exactly desired
    if text_height != 0:
        return CompositeVideoClip([bordered_clip,t]).set_duration(t.duration).set_fps(t.fps)
    else:
        return bordered_clip
    
if __name__ == "__main__":
    a = format_clip("C:\\Users\\Monchy\Dropbox\\MEMES\ehren yt\\ewe.gif",text='texting texting 123 HAHAHA')
    a.write_videofile("C:\\Users\\Monchy\Dropbox\\MEMES\ehren yt\\wew.mp4")
    
