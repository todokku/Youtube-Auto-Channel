from selenium import webdriver
import time


with open("youtube_account_info") as f: #stored in seperate file so I don't accidently post to github
    USER, PASS = f.read().split('\n')


def upload(video_path, desc = '', tags = []):
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
        find("button.save-changes-button").click()
                
    login()
    actual_upload()


   
if __name__ == "__main__":
    upload('C:\\Users\\Wakydawgster\\Documents\\Programmable Memes\\python JUNK\\autocancer youtube channel\\cancer.mp4')
    
