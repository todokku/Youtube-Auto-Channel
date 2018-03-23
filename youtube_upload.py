from selenium import webdriver
import time


with open("youtube_account_info") as f: #stored in seperate file so I don't accidently post to github
    USER, PASS = f.read().split('\n')


def upload(video_path, desc = '', tags = []):
    desc = ''.join(c for c in desc if ord(c) <= 127) #eliminates unicode characters that selenium can't type
    browser = webdriver.Chrome()
    
    def find(s):
        s = s.replace('"', "'")
        return browser.execute_script("return document.querySelector(\"" + s + "\")")

    def try_until_success(func): #sleeps until func doesn't throw an error
        while 1:
            try:
                func()
                return
            except:
                time.sleep(0.1)
               
    def login():
        browser.get('https://www.youtube.com/account')
        find('#identifierId').send_keys(USER)
        find('#identifierNext').click()
        @try_until_success
        def do_password():
            find('input[type="password"]').send_keys(PASS)
            find('#passwordNext').click()

    def actual_upload():
        @try_until_success
        def select_file():
            find("a[href='//www.youtube.com/upload']").click()
            find("input[type='file']").send_keys(video_path)
        desc_input = find('.video-settings-description')
        desc_input.send_keys(desc)
        tag_input = find('input.video-settings-add-tag')
        for tag in tags:
            tag_input.send_keys(str(tag) + ',')
        save_button = find("button.save-changes-button")
        save_button.click()
        if tags != []: #the done button only comes up if you have tags
            while 'Done' not in save_button.get_attribute("innerText"):
                time.sleep(0.1)
        save_button.click()
        processing_bar = find('.progress-bar-processing')
        while '0%' in processing_bar.get_attribute("innerText"):
            time.sleep(0.1)
                
    login()
    actual_upload()
    browser.close()


   
if __name__ == "__main__":
    import random; upload('C:\\Users\\Wakydawgster\\Documents\\Programmable Memes\\python JUNK\\autocancer youtube channel\\videos\\IF YOU LAUGH YOU MUST LIKE THIS VIDEO #2.mp4', 'asdf\xc5', [str(random.random()) for i in range(10)])
    
