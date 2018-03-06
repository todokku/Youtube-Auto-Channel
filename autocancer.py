print "importing make_vid..."
from make_vid import vid_from_imgs
print "importing image_getter..."
from image_getter import save_imgs
print "importing youtube_upload..."
from youtube_upload import upload
print "importing get_song..."
from get_song import get_song
print "importing reddit..."
from reddit import subreddit
print "importing get..."
from get import get


#I THINK THE LONG EXPORT MAY HAVE JUST BEEN CAUSED BY IT TAKING A WHILE TO PRINT TBH
    #SCROLLING THOUGH THE PRINTED TEXT WAS REALLY REALLY LAGGY

#ALSO, AUDIO'S GETTING CUT OFF AT THE END OF THE VIDEO

#AND I NEED A WAY OF CHECKING IF A REDDIT LINK IS NSFW/STICKIED

folder = 'images'
sub = subreddit('dankmemes')
"getting top of the day links..."
links = sub.top('day')
print 'downloading {0} links'.format(len(links))
all_imgs = save_imgs(links, 'images')
print "getting song..."
song = get_song()
print "making video..."
vid = vid_from_imgs("test.mp4",
                    all_imgs, song.file_path(), 0.125)
print "uploading video..."
upload(vid, "Song: " + str(song))
