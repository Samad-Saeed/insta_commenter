import uiautomator2 as u2
import time, os

def action():
    device = u2.connect()
    device.session("com.instagram.android")
    device.sleep(4)
    
   
    # more = device.xpath('//*[@content-desc="more"]')
    

    caption = device(resourceId="com.instagram.android:id/row_feed_comment_textview_layout")
    # caption.click()py 

    # if caption.exists():
    #     caption_text = caption.get_text()
    #     print("Caption:", caption_text)


    commentButton = device(resourceId="com.instagram.android:id/row_feed_button_comment")
    commentButton.click()

    try:
        comment = device(resourceId="com.instagram.android:id/layout_comment_thread_edittext")
        comment.set_text("I want to win the giveaway")

        commentPost = device(resourceId="com.instagram.android:id/layout_comment_thread_post_button_icon")
        commentPost.click()
    except:
        pass
             


def main():
    
    # check_keywords(device_ip)
    action()

if __name__ == "__main__":
    # os.system('adb connect localhost:51561')
    main()
