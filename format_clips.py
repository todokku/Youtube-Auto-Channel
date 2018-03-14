#from PIL import Image
#import numpy as np
#import moviepy
from moviepy.video import fx
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import time as t

# return VideoClip resized, bordered and with text
def format_clip(clip, text=None, text_pos='bottom', fontsize = 60 , ideal_size = (1920,1080)):

    if type(clip) == str:
        clip = VideoFileClip(clip)

    text_height = 0
    if text != None:
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
    a = format_clip("input file path goes here",text=None,ideal_size=(1920,1080))
    a.write_videofile("output file path goes here", verbose=False, progress_bar=False, preset='ultrafast')
 