import requests
import json
import re
import os
from bs4 import BeautifulSoup


def main():
    url = getUrl()
    header = getHeader()
    video_url, audio_url, title = getData(url=url, header=header)
    download(video_url=video_url, audio_url=audio_url, title=title, header=header)
    handlefile(title=title)


def getHeader():
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "cookie": "",
        "referer": "https://www.bilibili.com/",
    }
    if not os.path.exists("profile.json"):
        open("profile.json", "w", encoding="utf-8").write(json.dumps(header))

    with open("profile.json", "r", encoding="utf-8") as f:
        profile = json.loads(str(f.read()))
        header = profile
    return header


def getData(url, header):
    response = requests.get(url, headers=header)
    html_text = response.text
    soup = BeautifulSoup(html_text, "html.parser")
    title_text = soup.find_all("div", class_="video-info-title-inner")
    title = re.findall('title="(.*?)"', str(title_text[0]))
    json_str = re.findall("window.__playinfo__=(.*?)</script>", html_text)[0]
    json_data = json.loads(json_str)
    video_url = json_data["data"]["dash"]["video"][0]["baseUrl"]
    audio_url = json_data["data"]["dash"]["audio"][0]["baseUrl"]
    return video_url, audio_url, title


def getUrl():
    url = input("bilibili Url:")
    return url


def download(video_url, audio_url, title, header):
    video = requests.get(video_url, headers=header)
    audio = requests.get(audio_url, headers=header)

    if not os.path.exists("./data"):
        os.mkdir("./data")

    with open("./data/" + title[0] + "_video.mp4", "wb") as f:
        f.write(video.content)

    with open("./data/" + title[0] + "_audio.mp4", "wb") as f:
        f.write(audio.content)


def handlefile(title):
    if not os.path.exists("./out"):
        os.mkdir("./out")

    cmd = (
        'ffmpeg -i "./data/%s_video.mp4" -i "./data/%s_audio.mp4" -c copy "./out/%s.mp4"'
        % (title[0], title[0], title[0])
    )
    os.popen(cmd=cmd)


if __name__ == "__main__":
    main()
