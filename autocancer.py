print "importing make_vid..."
from make_vid import vid_from_media
print "importing media_getter..."
from media_getter import save_media
print "importing youtube_upload..."
from youtube_upload import upload
print "importing get_song..."
from get_song import get_song
print "importing reddit..."
from reddit import subreddit
print "importing get..."
from get import get
from sources import full_day_sources, update_titles
from time import sleep


#AUDIO'S GETTING CUT OFF AT THE END OF THE VIDEO

#SOMETIMES I NEED TO ENTER MY RECOVERY EMAIL WHEN LOGGING INTO YOUTUBE

#STANDARD GARBAGE MEME CHANNELS HAVE A BACKGROUND THATS NOT JUST BLACK, MAKE A BETTER ONE
    #IDK IF THIS IS POSSIBLE NOW THAT I'M DOING GIFS AND STUFF THOUGH

#THE FRAMERATE OF ONE OF THE VIDEOS WAS 50 FPS, FIND A WAY TO MAKE EVERY VIDEO ONLY 25 FPS
    #yeah I don't really care about this one 

for source in full_day_sources():
    sub = subreddit(source.subreddit)
    "getting top of the day links..."
    posts = [post for post in sub.top('day') if not post.is_sticky][:3]
    print 'downloading {0} links'.format(len(posts))
    all_media = save_media(posts, 'media')
    print "got {0} pieces of media".format(len(all_media))
    print "getting song..."
    song = get_song('dubstep')
    print song
    print "making video..."
    vid = vid_from_media("videos\\" + source.title + '.mp4', all_media, song.file_path(), source.text, 8)
    print "uploading video..."
    upload(vid, "Song: " + str(song), source.tags)
    update_titles(source.title)
    print "sleeping for like 20 mins..."
    sleep(60*20)
