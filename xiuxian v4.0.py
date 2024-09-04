'''
@name 自动修仙
@author myh
@version 4.0
@description 基于LiteLoaderQQNT和NapCatQQ/LLOneBot实现的自动修仙
'''

import requests,json,os,time,filecmp

verid = 4

# 更新 update
try:
	version = requests.get('https://Misaka10049.github.io/xiulian/version.json').json()
	if verid < version['latest']['ver']:
		if "xid" in version['latest']:
			filename = "xiuxian v{}.{}.py".format(version['latest']['xid'],version['latest']['yid'])
		else:
			filename = "xiuxian v{}.0.py".format(version['latest']['id'])
		latest_url = version['latest']['url']
		raw = requests.get(latest_url)
		if raw.ok:
			with open("download", "wb") as f:
				f.write(raw.content)
				f.close()
			itself = os.path.basename(__file__)
			os.system('del /q "{}"'.format(itself))
			os.system('rename download "{}"'.format(filename))
			print("脚本自动更新完成，请重新启动！\n")
			print("按任意键退出...")
			os.system("pause 1>nul 2>nul")
			exit()
		else:
			print('连接更新服务器失败，将使用当前版本继续！\n')
	else:
		print("您的脚本已是最新版！\n")
except Exception as e:
	print('发生错误：{}\n\n请报告给开发者\n'.format(e))
	print('更新检查失败，将使用当前版本继续！\n')

# 检测机器人框架
try:
	res = requests.get("http://127.0.0.1:3000/")
	if res.status_code == 200:
		print("检测到机器人框架已启动\n")
except:
	print("下次记得先启动机器人框架哦~\n")
	print("按任意键退出...\n")
	os.system("pause 1>nul 2>nul")
	exit()

# 初始化数据
xiulian = 0
group = 0
try:
	with open('settings.json','r',encoding='utf-8') as file:
		content = json.load(file)
		group = content['group']
		xiulian = content['times']
	print("你的小群群号是 {} 对吧，你已经自动修炼了 {} 次了！".format(group,xiulian))
	print('\n如果要修改小群群号的话，请修改文件 settings.json 中 "group" 字段后的内容，\n然后重新启动本程序')
except FileNotFoundError:
	group=int(input("请输入你小群的群号(需要有小小在里面): "))
except Exception as e:
	print('读取文件失败：{}\n\n请报告给开发者\n'.format(e))
	group=int(input("请输入你小群的群号(需要有小小在里面): "))

# 特殊判断
if group == 764310096:
	print("\n这个群是“柴郡王国”吧，你确定要这么做？(这算是一个彩蛋哦)\n")
	print("请按任意键结束")
	os.system("pause 1>nul 2>nul")
	exit()

# 发送修炼函数
def auto(qun):
	url = "http://127.0.0.1:3000/send_group_msg?group_id={}&message=[CQ:at,qq=3889001741]%20修炼".format(qun)
	response = requests.get(url).json()
	status = response['status']
	if status != 'ok' and status != 'async':
		print('可能发生了错误，请咨询开发者：')
		print(response)
	return None

# 手动启动修炼
print("\n请确认上次修炼已经结束，然后按任意键启动(固定每67s发送一次修炼)\n")
os.system("pause 1>nul 2>nul")
now=time.time()

while True:
	try:
		# 尝试发送修炼
		print("[{}] 第 {} 次修炼\n".format(time.strftime('%X', time.localtime()),xiulian+1))
		auto(group)
		now = time.time()
		xiulian += 1
		with open('settings.json','w') as file:
			file.write("{"+'"group":{},"times":{}'.format(group,xiulian)+"}")
	except Exception as e:
		# 错误处理 重试
		print('发生未知错误：{}\n\n这种情况可能是你的 QQ 关闭了，如果不是请报告给开发者哦\n'.format(e))
		print("将在3s后尝试重新发送\n")
		time.sleep(3)
		continue
	# 等待
	delay = 67 - (time.time() - now)
	time.sleep(delay)
