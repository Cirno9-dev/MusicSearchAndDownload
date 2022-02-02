import requests
import sys
import base64

music_name = "無間嫉妬劇場"
music_id = "1306498257"
music_path = "./"

unUse = ["*", "/", "\\", "<", ">", "|", ":", "?", "\""]
for char in unUse:
	music_name = music_name.replace(char, "")

head = {"User-Agent":'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
			"Referer": "https://music.163.com/"}
url_music = "http://music.163.com/song/media/outer/url?id="+music_id+".mp3"
try:
	html = requests.get(url_music, headers=head)
	with open(music_path+music_name+".mp3", "wb") as f:
		f.write(html.content)
	print(music_name, "successfully")
except Exception as e:
	print(e)
	print(music_name, "error")