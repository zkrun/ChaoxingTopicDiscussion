import requests
import re
import json
from urllib.parse import unquote
import hashlib
import time
url_find='https://sharewh1.xuexi365.com/share/'
url="https://passport2.chaoxing.com/fanyalogin"
url_reply='https://groupweb.chaoxing.com/course/topicDiscuss/23dd9ff499b24338a58c465ff8b46ff4_topicDiscuss/getTopic'
course_url='https://mooc2-ans.chaoxing.com/mooc2-ans/visit/courselistdata'
url_activity='https://mobilelearn.chaoxing.com/v2/apis/active/student/activelist?'
url_activity_info='https://mobilelearn.chaoxing.com/v2/apis/discuss/getTopicDiscussInfo?'
course_params={
    'courseType':'1',
    'courseFolderId':'0',
    'query':'',
    'superstarClass':'0'
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 13; M2012K11AC Build/TKQ1.220829.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/116.0.0.0 Mobile Safari/537.36 XWEB/1160065 MMWEBSDK/20230805 MMWEBID/5630 MicroMessenger/8.0.42.2424(0x28002A43) WeChat/arm64 Weixin GPVersion/1 NetType/4G Language/zh_CN ABI/arm64 MiniProgramEnv/android',
    'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
    'Cookie':'lang=zh-CN',


}

headers_new={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0'
}

headers_android ={
    'User-Agent':'Dalvik/2.1.0 (Linux; U; Android 13; M2012K11AC Build/TKQ1.220829.002) (schild:c6d53cc67e7d563d0d71a9f26972a5be) (device:M2012K11AC) Language/zh_CN com.chaoxing.mobile/ChaoXingStudy_3_6.1.5_android_phone_911_103 (@Kalimdor)_18d77c7addc743ada77d444496c49f06'

}


# 创建一个会话对象
session = requests.Session()
uname=input("输入账号:")
password=input("输入密码")
# 构造登录请求的参数
login_data = {
    'fid': '-1',
    'uname': uname,
    'password': password,
    'refer': 'https://i.chaoxing.com',
    't': 'true',
    'doubleFactorLogin': '0',
    'forbidotherlogin': '0',
    'independentId': '0',
    'independentNameId': '0'
}
course_list_data = {
    'courseType': '1',
    'courseFolderId': '0',
    'baseEducation': '0',
    'superstarClass': '',
    'courseFolderSize': '0'
}
# 发送登录请求
response = session.post(url=url, data=login_data,headers=headers)

# 检查登录是否成功
if response.status_code == 200:
    print(response.text)
    # 保存响应的 cookie
    cookies = session.cookies.get_dict()
    session.cookies.update(cookies)

else:
    print('登录失败')


response=session.get('https://mooc1-api.chaoxing.com/mycourse/backclazzdata?view=json&mcode=',headers=headers_android)
#print(response.text) #打印课程信息


parsed_data = json.loads(response.text)

# Extract course names, classIds, and courseIds
courses = parsed_data['channelList']

# Create a dictionary to store course names as keys and their corresponding courseId and classId as values
course_mapping = {}

for course in courses:
    content = course['content']

    if 'course' in content:
        course_data = content['course']['data']

        if course_data:
            course_name = course_data[0]['name']
            class_id = content['id']
            course_id = course_data[0]['id']

            # Store the course name, courseId, and classId in the dictionary
            course_mapping[course_name] = {'courseId': course_id, 'classId': class_id}

# Prompt the user to enter a course name
user_input = input("Enter a course name: ")

# Check if the entered course name exists in the course_mapping dictionary
if user_input in course_mapping:
    # Retrieve the courseId and classId for the entered course name
    course_info = course_mapping[user_input]
    course_id = course_info['courseId']
    class_id = course_info['classId']

   # print("Course Name:", user_input)
    #print("Class ID:", class_id)
    #print("Course ID:", course_id)
else:
    print("Course not found.")

fid = cookies.get("fid")
timestamp = str(int(time.time() * 1000))  # 获取当前毫秒级时间戳并转换为字符串
url_activity=url_activity+'fid=%s&courseId=%s&classId=%s&showNotStartedActive=0&_=%s' % (fid,course_id,class_id,timestamp)
#print(url_activity)
activity_response=session.get(url_activity,headers=headers_new)
#print(activity_response.text)
parsed_data = json.loads(activity_response.text)

# Extract the activeList array
active_list = parsed_data['data']['activeList']

# Print the id and nameOne for each item in activeList
for item in active_list:
    id = item['id']
    name = item['nameOne']
    #print("ID:", id)
    #print("Name:", name)
    #print()

# Prompt the user to enter the discussion number
discussion_number = input("Enter the discussion number: (用中文数字输入)")

# Find the corresponding item based on the discussion number entered by the user
discussion_item = None
for item in active_list:
    if item['nameOne'].startswith(f"第{discussion_number}次讨论"):
        discussion_item = item
        break

# Check if the discussion item was found
if discussion_item:
    discussion_id = discussion_item['id']
    #print("Discussion ID:",  discussion_id)
else:
    print("Discussion not found.")
url_activity_info=url_activity_info +  'activeId='+ str(discussion_id)
url_activity_info_response=session.get(url=url_activity_info,headers=headers)
#print(url_activity_info_response.text)
parsed_data = json.loads(url_activity_info_response.text)

# Extract the uuid and bbsid
uuid = parsed_data['data']['uuid']
bbsid = parsed_data['data']['bbsid']
#最终输出结果
url_final=url_find + str(uuid) + '?c=' + str(bbsid) + '&t=2'
print(url_final)

