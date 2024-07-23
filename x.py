import uiautomator2 as u2
d = u2.connect('192.168.1.5:40167')

d(resourceId="com.instagram.android:id/row_profile_header_imageview").click()
