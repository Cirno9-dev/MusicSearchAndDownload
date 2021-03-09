from selenium.webdriver.firefox.options import Options

# 设置options
firefox_options = Options()
firefox_options.add_argument("--headless")
firefox_options.add_argument("--disable-gpu")

import requests
import re
from selenium import webdriver
from time import sleep
from prettytable import PrettyTable

# 搜索音乐
def SearchMusic(name):
	url_search = "https://music.163.com/#/search/m/?s="+name+"&type=1"
	# 初始化
	browser = webdriver.Firefox(executable_path="geckodriver.exe", options=firefox_options)
	# 歌曲搜索
	browser.get(url=url_search)
	# 切换iframe
	browser.switch_to.frame("g_iframe")
	sleep(0.5)
	# 页面信息
	page_text = browser.execute_script("return document.documentElement.outerHTML")
	# 退出
	browser.quit()
	# 正则表达式
	re1 = '<a.*?id="([0-9]*?)"'
	re2 = '<b title="(.*?)">.*?<span class="s-fc7">'
	re3 = 'class="td w1"><div class="text"><a href=".*?">(.*?)</div></div>'

	id_list = re.findall(re1, page_text, re.M)[::2]
	song_list = re.findall(re2, page_text, re.M)
	singer_list = re.findall(re3, page_text, re.M)

	total_list = list(zip(song_list, singer_list, id_list))

	# 命令行表格
	table = PrettyTable(["序号", "音乐名", "歌手", "音乐ID"])

	for i in range(len(total_list)):
		# 处理多个歌手
		# 处理不完全，可能有BUG
		if "<a href=" in total_list[i][1]:
			re4 = '(.*?)</a>'
			temp = re.findall(re4, total_list[i][1], re.M)
			re5 = '<a href=".*?">(.*?)</a>'
			singer = ""
			for s in temp:
				t = re.findall(re5, s+"</a>", re.M)
				if t == []:
					singer += s + "/"
				else:
					singer += t[0] + "/"
			total_list[i] = (total_list[i][0], singer[:-1], total_list[i][2])
		else:
			if total_list[i][1][-1] != ">":
				temp = total_list[i][1].replace("</a>","")
			else:
				temp = total_list[i][1][:-4]
			total_list[i] = (total_list[i][0], temp, total_list[i][2])
		# 将数据加入到表格
		table.add_row([str(i+1), total_list[i][0], total_list[i][1], total_list[i][2]])
	# 输出表格
	print(table,"\n")
	return total_list

# 下载音乐
def GetMusic(music_id):
	head = {"User-Agent":'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
			"Referer": "https://music.163.com/"}
	url_music = "http://music.163.com/song/media/outer/url?id="+music_id+".mp3"
	html = requests.get(url_music, headers=head)
	with open(music_id+".mp3", "wb") as f:
		f.write(html.content)

# 输出菜单
def menu():
	print("网易云音乐搜索下载")
	print("1.音乐搜索")
	print("2.音乐下载(需要音乐ID)")
	print("3.退出")
	print("注: 音乐搜索可以获得音乐ID\n")

# 主函数
def main():
	while 1:
		menu()
		num = input("请输入序号(1-3):")
		try:
			num = int(num)
		except:
			print("错误序号!\n")
			continue
		if num not in [1,2,3]:
			print("错误序号!\n")

		if num == 1:
			name = input("\n输入歌名(输入q返回):")
			if name == "q":
				continue
			total_list = SearchMusic(name)
		elif num == 2:
			music_id = input("\n请输入歌曲id(输入q返回):")
			if music_id == "q":
				continue
			print("下载中")
			GetMusic(music_id)
			print("下载完成\n")
		elif num == 3:
			break

if __name__ == '__main__':
	main()