'''
@name 自动修仙
@author myh
@version 3.0
@description 使用插件自动修仙
'''

import requests,json,os,time,filecmp

# 更新 update
try:
	version = requests.get('https://Misaka10049.github.io/xiulian/version.json').json()
	latest_url = version['latest']
	raw = requests.get(latest_url)
	if raw.ok:
		with open("download", "wb") as f:
			f.write(raw.content)
			f.close()
		itself = os.path.basename(__file__)
		if not filecmp.cmp(itself,"download"):
			os.system('echo y|copy download "{}"'.format(itself))
			os.system("del /q download")
			print("脚本自动更新完成，即将重新启动！\n")
			time.sleep(3)
			os.system("python "+itself)
			exit()
		else:
			print("您的脚本已是最新版！\n")
	else:
		print('更新检查失败，将使用当前版本继续！\n')
except Exception as e:
	print('发生错误：{}\n请报告给开发者\n'.format(e))
	print('更新检查失败，将使用当前版本继续！\n')

try:
	res = requests.get("http://127.0.0.1:3000/")
	if res.status_code == 200:
		print("检测到机器人框架已启动\n")
except:
	print("下次记得先启动机器人框架哦~\n")
	print("按任意键结束\n")
	os.system("pause 1>nul 2>nul")
	exit()

xiulian = 0
group = 0
try:
	with open('settings.json','r',encoding='utf-8') as file:
		content = json.load(file)
		group = content['group']
		xiulian = content['times']
	print("你的小群群号是 {} 对吧，你已经自动修炼了 {} 次了！".format(group,xiulian))
	print("\n如果要修改小群群号，请删除文件 settings.json 并重新启动本程序")
except FileNotFoundError:
	group=int(input("请输入你小群的群号(需要有小小在里面): "))
except PermissionError:
	print('无权限访问文件！') 
except Exception as e:
	print('发生未知错误：{}\n请报告给开发者\n'.format(e))
	print("请按任意键结束")
	os.system("pause 1>nul 2>nul")
	exit()

if group == 764310096:
	print("\n这个群是“柴郡王国”吧，你确定要这么做？(这算是一个彩蛋哦)\n")
	print("请按任意键结束")
	os.system("pause 1>nul 2>nul")
	exit()

print("\n请确认上次修炼已经结束，然后按任意键启动(固定每67.5s发送一次修炼)\n")
os.system("pause 1>nul 2>nul")
now=time.time()

def auto():
	global xiulian,group
	msg = '[CQ:at,qq=3889001741]%20修炼'
	url = "http://127.0.0.1:3000/send_group_msg?group_id={}&message={}".format(group,msg)
	response = requests.get(url).json()
	status = response['status']
	if status != 'ok' and status != 'async':
		print('可能发生了错误，请咨询开发者：')
		print(response)
	return None

while True:
	try:
		print("第 {} 次修炼\n".format(xiulian+1))
		auto()
		now = time.time()
		xiulian += 1
		with open('settings.json','w') as file:
			file.write("{"+'"group":{},"times":{}'.format(group,xiulian)+"}")
	except Exception as e:
		print('发生未知错误：{}\n\n请报告给开发者哦\n'.format(e))
		print("将在3s后尝试重连\n")
		time.sleep(3)
		continue
	delay = 67.5 - (time.time() - now)
	time.sleep(delay)