import uiautomator2 as u2
import time
import os, random
from dotenv import load_dotenv
import requests

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("OPENAI_API_KEY is not set in environment variables or .env file")

def get_random_comment_from_file(filename="comments.txt"):
    try:
        with open(filename, "r") as file:
            comments = file.readlines()
        return random.choice(comments).strip()
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return "Nice post!"

def get_gpt_response(prompt, api_key):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 50
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        response_json = response.json()
        return response_json['choices'][0]['message']['content'].strip()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return get_random_comment_from_file()

def generate_caption_comment(hashtag):
    prompt = f"Generate a small, less than 15 words engaging random comment for a hashtag: {hashtag}"
    return get_gpt_response(prompt, api_key)

def generate_generic_comment():
    prompt = "Generate a small, less than 15 words engaging random comment for an Instagram post."
    return get_gpt_response(prompt, api_key)

def like_post(device):
    like_button = device(resourceId='com.instagram.android:id/row_feed_button_like')
    if like_button.exists:
        if like_button.info['contentDescription'] == 'Liked':
            print("[+] Already liked the post")
        else:
            like_button.click()
            print("[+] Post Liked")
            return True
    else:
        return False

def comment_on_post(device, comment_text):
    try:
        comment_button = device(resourceId="com.instagram.android:id/row_feed_button_comment")
        if comment_button.exists:
            comment_button.click()
            time.sleep(2)
            comment_field = device(resourceId="com.instagram.android:id/layout_comment_thread_edittext")
            comment_field.set_text(comment_text)
            time.sleep(2)
            post_button = device(resourceId="com.instagram.android:id/layout_comment_thread_post_button_icon")
            post_button.click()
            print("[+] Commented on the post")
            device.press('back')
            device.press('back')
            return True
    except Exception as e:
        print(f"[-] Error commenting on the post: {e}")
    return False

def search_hashtag(device, hashtag):
    device.session("com.instagram.android")
    device.sleep(4)

    search_button = device.xpath('//*[@resource-id="com.instagram.android:id/search_tab"]')
    search_button.click()
    device.sleep(2)
    
    search_bar = device.xpath('//*[@resource-id="com.instagram.android:id/action_bar_search_hints_text_layout"]')
    search_bar.set_text(f"#{hashtag}")
    time.sleep(2)
    
    try:
        hashtag_result = device(resourceId="com.instagram.android:id/row_search_keyword_title", text=f"#{hashtag}").click()
        time.sleep(2)
    except:
        print("Hashtag not found. Please try another one.")
        return False
    return True

def comment_on_hashtag_posts(device, hashtag):
    if not search_hashtag(device, hashtag):
        return
    
    post = device(resourceId="com.instagram.android:id/image_button", index=0)
    post.click()
    time.sleep(2)

    while True:
        time.sleep(2)
        like_successful = like_post(device)
        
        if like_successful:
            comment_text = generate_caption_comment(hashtag)
            print(comment_text)
            time.sleep(4)
            comment_successful = comment_on_post(device, comment_text)
            if not comment_successful:
                print("[-] Error during commenting, swiping to next post.")
        else:
            print("[-] Swiping next post")
        
        device.swipe(500, 1500, 500, 500)  # Swipe to next post
        time.sleep(2)

def comment_on_profile_followers(device, profile_username):
    profile_url = f"instagram://user?username={profile_username}"
    device.open_url(profile_url)
    time.sleep(4)  

    followers_count = device(resourceId="com.instagram.android:id/row_profile_header_textview_followers_count")
    followers_count.click()
    time.sleep(2)

    follower_index = 2

    while True:
        follower_profile = device.xpath(f'//*[@resource-id="android:id/list"]/android.widget.LinearLayout[{follower_index}]')
        if not follower_profile.exists:
            break

        follower_profile.click()
        time.sleep(4)

        post = device(resourceId="com.instagram.android:id/media_set_row_content_identifier").child(index=0)
        if post.exists:
            post.click()
            device.swipe(500, 700, 500, 500) 
            time.sleep(1)
            like_post(device)
            comment_text = generate_generic_comment()
            print(comment_text)
            time.sleep(5)
            comment_on_post(device, comment_text)

        device.press('back')
        device.press('back')
        device.press('back')
        time.sleep(2)
        
        see_more = device.xpath('//*[contains(text(), "see more")]')
        if see_more.exists:
            see_more.click()

        follower_index += 1
        if follower_index == 10:
            follower_index = 2
            device.swipe(500, 1500, 500, 500, steps=10)
            time.sleep(2)

def comment_on_home_feed(device):
    device.session("com.instagram.android")
    time.sleep(2)

    while True:
        like_successful = like_post(device)
        
        if like_successful:
            comment_text = generate_generic_comment()
            print(comment_text)
            time.sleep(4)
            comment_successful = comment_on_post(device, comment_text)
            if not comment_successful:
                print("[-] Error during commenting, swiping to next post.")
        else:
            print("[-] Like button not found, swiping to next post")
        
        device.swipe(500, 1500, 500, 500)  # Swipe to next post
        time.sleep(2)

def comment_on_stories(device):
    device.session("com.instagram.android")
    time.sleep(2)

    stories = device.xpath('//*[@content-desc="reels_tray_container"]/android.widget.LinearLayout[2]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.view.View[1]')
    while stories.exists:
        stories.click()
        time.sleep(2)

        while not device(resourceId="com.instagram.android:id/toolbar_like_container").exists:
            time.sleep(5)
        
        like_button = device(resourceId="com.instagram.android:id/toolbar_like_container")
        like_button.click()
        time.sleep(2)
        device.swipe(500, 1500, 500, 500)  # Swipe to next story
        time.sleep(2)

def main():
    device = u2.connect()

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
