import uiautomator2 as u2
import google.generativeai as genai
import time,os
from dotenv import load_dotenv

load_dotenv()

# Configure the API key
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in environment variables or .env file")

genai.configure(api_key=api_key)

def caption_comment(hashtag):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Generate a small, less than 15 words engaging random comment for a hashtag: {hashtag}"
        response = model.generate_content(prompt)
        
        comment = response.text
        return comment
    except Exception as e:
        print(f"Error generating comment: {e}")
        return "Nice post!"

def generate_comment():
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Generate a small, les than 15 words engaging random comment for a Instagram post: "
        response = model.generate_content(prompt)
        
        comment = response.text
        return comment
    except Exception as e:
        print(f"Error generating comment: {e}")
        return "Nice post!"

    
def comment_on_hashtag_posts(device, hashtag):
    device.session("com.instagram.android")
    device.sleep(4)

    searchButton = device.xpath('//*[@resource-id="com.instagram.android:id/search_tab"]')
    searchButton.click()
    device.sleep(2)
    
    searchBar = device.xpath('//*[@resource-id="com.instagram.android:id/action_bar_search_hints_text_layout"]')
    searchBar.set_text(f"#{hashtag}")
    time.sleep(2)
    try:
        hashtag_ = device(resourceId="com.instagram.android:id/row_search_keyword_title", text=f"#{hashtag}").click()
        time.sleep(2)
    except:
        if not hashtag_.exists:
            print(" Hashtag not found Please try another one")

    post = device(resourceId="com.instagram.android:id/image_button", index=0)
    post.click()
    time.sleep(2)

    while True:
            
            like_button_visible = False
            for _ in range(3):  # Try swiping a few times to bring the like button into view
                like_button = device(resourceId='com.instagram.android:id/row_feed_button_like')
                if like_button.exists:
                    like_button_visible = True
                    break
                else:
                    device.swipe(500, 1000, 500, 500) 
                    time.sleep(1)

            if like_button_visible:
                try:
                    if like_button.info['contentDescription'] == 'Liked':
                        print("[+] Already liked the post")
                        # device.swipe(500, 1500, 500, 500) 
                        device.swipe(500, 1500, 500, 500) 
                    else:
                        like_button.click()
                        print("[+] Post Liked")
                        comment_text = caption_comment(hashtag)
                        print(comment_text)
                        time.sleep(4)

                        
                        try:
                            comment_button = device(resourceId="com.instagram.android:id/row_feed_button_comment")
                            if comment_button.exists:
                                comment_button.click()
                                time.sleep(2)
                                comment = device(resourceId="com.instagram.android:id/layout_comment_thread_edittext")
                                comment.set_text(comment_text)
                                time.sleep(2)
                                comment_post = device(resourceId="com.instagram.android:id/layout_comment_thread_post_button_icon")
                                comment_post.click()
                                print("[+] Commented on the post")
                                device.press('back')
                                device.press('back')
                        except Exception as e:
                            print(f"[-] Error commenting on the post: {e}")
                            pass
                except Exception as e:
                    print(f"[-] Error liking the post: {e}")
                    pass
            else:
                print("[-] Like button not found, swiping to next post")

            time.sleep(2)

def comment_on_profile_followers(device, profile_username):
    profile = f"instagram://user?username={profile_username}"
    device.open_url(profile)
    time.sleep(4)  

    # Click on the follower count
    followers_count = device(resourceId="com.instagram.android:id/row_profile_header_textview_followers_count")
    followers_count.click()
    time.sleep(2)

    follower_index = 2  # Start with the first profile in the list

    while True:
        first_profile = device.xpath(f'//*[@resource-id="android:id/list"]/android.widget.LinearLayout[{follower_index}]')
        if not first_profile.exists:
            break  # Exit if no more profiles are found

        first_profile.click()
        time.sleep(4)

        post = device(resourceId="com.instagram.android:id/media_set_row_content_identifier").child(index=0)
        # Check if the user has posts
        if post.exists:
            
            # time.sleep(4)

            post.click()
            device.swipe(500, 700, 500, 500) 
           
            time.sleep(1)
            try:
                like_button = device(resourceId='com.instagram.android:id/row_feed_button_like')
                if like_button.exists and like_button.info['contentDescription'] == 'Liked':
                    print(f"[+] Already liked the post")
                else:
                    like_button.click()
                    print(f"[+] Post Liked")
            except:
                pass

            commentButton = device(resourceId="com.instagram.android:id/row_feed_button_comment")
            commentButton.click()
            comment_text = generate_comment()
            print(comment_text)
            time.sleep(5)

            try:
                pass
                comment = device(resourceId="com.instagram.android:id/layout_comment_thread_edittext")
                comment.set_text(comment_text)
                time.sleep(2)
                commentPost = device(resourceId="com.instagram.android:id/layout_comment_thread_post_button_icon")
                commentPost.click()
            except:
                pass

            time.sleep(2)
            device.press('back')
            time.sleep(2)
            device.press('back')
            time.sleep(1)
            device.press('back')
            time.sleep(1)
            device.press('back')
        else:
            device.press('back')
            time.sleep(2)

        see_more = device.xpath('//*text="see more"')
        if see_more.exists:
            see_more.click()

        follower_index += 1  # Move to the next profile in the list
        if follower_index == 10:
            follower_index = 2
            device.swipe(500, 1500, 500, 500, steps=10)  # Adjust the swipe coordinates and steps as necessary
            time.sleep(2)

        time.sleep(2)


def comment_on_home_feed(device):
    device.session("com.instagram.android")
    time.sleep(2)

    while True:
        
        like_button_visible = False
        for _ in range(3):  # Try swiping a few times to bring the like button into view
            like_button = device(resourceId='com.instagram.android:id/row_feed_button_like')
            if like_button.exists:
                like_button_visible = True
                break
            else:
                device.swipe(500, 1000, 500, 500) 
                time.sleep(1)

        if like_button_visible:
            try:
                if like_button.info['contentDescription'] == 'Liked':
                    # print("[+] Already liked the post")
                    # device.swipe(500, 1500, 500, 500) 
                    device.swipe(500, 1500, 500, 500) 
                else:
                    like_button.click()
                    print("[+] Post Liked")
                    comment_text = generate_comment()
                    print(comment_text)
                    time.sleep(4)

                    
                    try:
                        comment_button = device(resourceId="com.instagram.android:id/row_feed_button_comment")
                        if comment_button.exists:
                            comment_button.click()
                            time.sleep(2)
                            comment = device(resourceId="com.instagram.android:id/layout_comment_thread_edittext")
                            comment.set_text(comment_text)
                            time.sleep(2)
                            comment_post = device(resourceId="com.instagram.android:id/layout_comment_thread_post_button_icon")
                            comment_post.click()
                            print("[+] Commented on the post")
                            device.press('back')
                    except Exception as e:
                        print(f"[-] Error commenting on the post: {e}")
                        pass
            except Exception as e:
                print(f"[-] Error liking the post: {e}")
                pass
        else:
            print("[-] Like button not found, swiping to next post")

        time.sleep(2)


def comment_on_stories(device):
    device.session("com.instagram.android")
    time.sleep(2)

    stories = device.xpath('//*[@content-desc="reels_tray_container"]/android.widget.LinearLayout[2]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.view.View[1]')
    while True:
        if stories.exists:
            stories.click()
            time.sleep(2)
            
            # Wait for the like button to appear
            while not device(resourceId="com.instagram.android:id/toolbar_like_container").exists:
                time.sleep(5)  # Check every 1 second
            
            like_button = device(resourceId="com.instagram.android:id/toolbar_like_container")
            like_button.click()
            time.sleep(2)
        else:
            break


def main():
    device = u2.connect('192.168.1.9:43487')

    while True:
        print("\nMenu:")
        print("1. Comment on posts related to hashtags")
        print("2. Comment on selected profile's followers and their followers")
        print("3. Comment on home feed")
        print("4. Comment on stories")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            hashtag = input("Enter the hashtag: ")
            comment_on_hashtag_posts(device, hashtag)
        elif choice == '2':
            profile_username = input("Enter the profile username: ")
            comment_on_profile_followers(device, profile_username)
        elif choice == '3':
            comment_on_home_feed(device)
        elif choice == '4':
            comment_on_stories(device)
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
