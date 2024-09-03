'''
@name 自动修仙
@author myh
@version 1.0.1
@description 使用QQ机器人框架自动修仙
'''

import requests,json,os,time

xiulian = 0

def send_msg(data):# 发送消息
	msg_type = data['msg_type']  # 发送类型（群聊/私聊）
	number = data['number']  # 发送账号（群号/好友号）
	msg = data['msg']  # 要发送的消息

	# 对特殊字符进行url编码
	msg = msg.replace(" ", "%20")
	msg = msg.replace("\n", "%0a")

	url=""
	if msg_type == 'group':
		url = "http://127.0.0.1:5700/send_group_msg?group_id=" + str(number) + "&message=" + msg
	elif msg_type == 'private':
		url = "http://127.0.0.1:5700/send_private_msg?user_id=" + str(number) + "&message=" + msg
	global xiulian,group
	xiulian += 1
	with open('settings.json','w') as file:
		file.write("{"+'"group":{},"times":{}'.format(group,xiulian)+"}")
	print("第 {} 次修炼\n".format(xiulian))
	response = requests.get(url).json()
	status = response['status']
	if status == 'ok' or status == 'async' :
		return status
	else:
		print(status+' '+response['msg']+' '+response['wording'])
		return None

try:
	res = requests.get("http://127.0.0.1:5700/")
	if res.status_code == 200:
		print("机器人框架已启动\n")
except:
	print("下次记得先启动机器人框架哦~\n")
	print("按任意键结束\n")
	os.system("pause 1>nul 2>nul")
	exit()

bot=3889001741
group=0
try:
	with open('settings.json','r',encoding='utf-8') as file:
		content = json.load(file)
		group = content['group']
		xiulian = content['times']
	print("你的小群群号是 {} 对吧，你已经自动修炼了 {} 次了！".format(group,xiulian))
	print("\n如果遇到问题，或是要修改小群群号，请删除文件 settings.json 并重新启动本程序")
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

print("\n请确认上次修炼已经结束，然后按任意键启动(固定每68s发送一次修炼)\n")
os.system("pause 1>nul 2>nul")
now=time.time()

while True:
	send_msg({'msg_type':'group','number':group,'msg':'[CQ:at,qq=3889001741]修炼'})
	while True:
		if time.time() - now > 68 :
			now = time.time()
			break