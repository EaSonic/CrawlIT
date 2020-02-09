import os
from os.path import join, getsize
import requests
from moviepy.editor import *

host = 'https://w.5huase.com'

def getVideoId():
    videoId = int(1142432)
    # videoUrl = host + str("video-") + str(videoId)
    return str(videoId)

def getXHR():
    videoId = getVideoId()
    # https://w.5huase.com/video/view/1142432
    headers = {
        # "cookie": "__cfduid=df35aedc536fb7f864db3592c14758acb1581099613; _ga=GA1.2.1465073728.1581099615; _gid=GA1.2.537211386.1581099615; xn=00b9c562-3efa-4e62-a22b-7108b1fdd463; v=eyJhbGciOiJIUzI1NiJ9.eyJJZCI6MzQ5MTUzLCJVaWQiOjM0OTE1MywiZXhwIjoxNTg4OTAzMDA5LjA0NDYwNTUsImlkIjozNDkxNTMsInVpZCI6MzQ5MTUzfQ.COS64h2QHECNzZZczwEuS9WOPGCdEK85vGBAlYjdky8",
        "referer": str(host) + "/video/view/" + str(videoId),
        # "sec-fetch-mode": "cors",
        # "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
        "x-requested-with": "XMLHttpRequest",
    }
    # https://w.5huase.com/api/video/player_domain?id=1142432
    videoUrl = str(host) + "/api/video/player_domain?id=" + videoId
    response = requests.get(videoUrl,headers=headers)
    res_status = response.status_code
    if res_status == 200:
        response = response.json()
        # print(response)
        return response
    else:
        return None

def parseXHR():
    XHR = getXHR()
    code = XHR.get("code")
    if code == 1:
        return XHR.get("data")
    else:
        print('Error! \n')
        return None

# data: "https://hot22.yyhdyl.com/20191230/6f814eaa13dd20a38ef4a6101db323bf/hls/hls.m3u8?t=1581129115&sign=537c263a805dccb35a88179b35b36e13"
def m3u8(data):
    # Get master m3u8
    response = requests.get(data)
    res_status = response.status_code
    if res_status == 200:
        response = response.text.splitlines()
        
        for i, line in enumerate(response):
            if '720p' in line:
                break
            
        print(line+'\t'+str(i)+'\n')

        # Get largest quality m3u8
        uri = data.rpartition('/')
        m3u8_720p_url = uri[0] + '/' + response[i+1]
        response = requests.get(m3u8_720p_url)

        path_urls = filter(lambda line: '#' not in line, response.text.splitlines())
        # file_urls = filter(lambda path: path.rpartition('/')[2], path_urls)
        file_urls = ["https://hot22.yyhdyl.com" + path for path in path_urls]

        return file_urls
    else:
        return None

if __name__ == '__main__':
    # file_urls = []
    # XHR = parseXHR()
    # if XHR == None:
    #     print('Error!\n')
    # else:
    #     file_urls = m3u8(XHR)
    #     # print(*file_urls, sep = '\t')
    
    # if file_urls is not None:
    #     dl_path = os.getcwd() + "/哈尔滨约炮大神JOKER付费群福利/"
    #     for i, file in enumerate(file_urls):
    #         dir = dl_path
    #         if not os.path.exists(dir):
    #             print("创建目录:.%s" % dir)
    #             os.makedirs(dir)
    #         # Write into disk
    #         with open(r'{}{}.ts'.format(dir, i), 'ab')as f:
    #             r = requests.get(file)
    #             print("正在下载:{}...".format(file), end="")
    #             f.write(r.content)
    #             print("\t下载完成！")

    videos = []

    for root, dirs, files in os.walk("./哈尔滨约炮大神JOKER付费群福利"):
        files = [f for f in files if not f[0] == '.']
        # files.sort(key=lambda f: int(re.sub('\D', '', f)))
        fl = sorted(files, key=lambda x: int(os.path.splitext(x)[0]))
        files.sort(key = lambda f: int(os.path.splitext(f)[0]))
        print(*files, sep = '\n')

        for file in files:
            if os.path.splitext(file)[1] == ".ts":
                fpath = os.path.join(root, file)
                print("Now join " + fpath)
                video = VideoFileClip(fpath)
                videos.append(video)

    final_clip = concatenate_videoclips(videos)
    final_clip.write_videofile("./哈尔滨约炮大神JOKER付费群福利.mp4")

'''
    for root, dirs, files in os.walk("./哈尔滨约炮大神JOKER付费群福利"):
        # files = files.replace('mp2t', 'ts')
        files.sort()
        print(files)
        for file in files:
            old = os.getcwd() + "/哈尔滨约炮大神JOKER付费群福利/" + file
            new = os.getcwd() + "/哈尔滨约炮大神JOKER付费群福利/" + file.replace('mp2t', 'ts')
            print(new)
            os.rename(old, new)

    dl_path = os.path.join(os.getcwd() + "/哈尔滨约炮大神JOKER付费群福利/")
    videos = []
    file0 = dl_path + "0.ts"
    file1 = dl_path + "1.ts"
    file2 = dl_path + "2.ts"
    video0 = VideoFileClip(file0)
    video1 = VideoFileClip(file1)
    video2 = VideoFileClip(file2)
    videos.append(video0)
    videos.append(video1)
    videos.append(video2)

    final = concatenate_videoclips(videos)
    final.write_videofile("./target.mp4")
'''