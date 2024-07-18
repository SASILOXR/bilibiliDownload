import requests
import json
import re
import os
from bs4 import BeautifulSoup


def main():
    url = getUrl()
    header = getHeader(url=url)
    video_url, audio_url, title = getData(url=url, header=header)
    download(video_url=video_url, audio_url=audio_url, title=title, header=header)


def getHeader(url):
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "cookie": "buvid3=18D2110A-F1CF-6FCE-F0B0-AF9FF4FDB7A340856infoc; b_nut=1721199440; CURRENT_FNVAL=4048; bsource=search_google; _uuid=6AB5972E-10CCA-BDFF-C2D4-C1791BE10185738579infoc; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjE0NTg2NDEsImlhdCI6MTcyMTE5OTM4MSwicGx0IjotMX0.PNsqpilG9sy5pJ4_mgMY0NQOAC5CzyOgdgqEpyO4lnU; bili_ticket_expires=1721458581; rpdid=|(kmJ))YJ|kJ0J'u~kuummRRk; SESSDATA=9f7898d9%2C1736751523%2Cb2561%2A71CjDG-s0gcl0M8nN0G4yx6wR7FLHBnaheid0T6TZujayjS89MG4NmmOt0ElOA1GrtapESVkJZTk1CNXk2Y01jRlNRQlpTSldEZUJpMGRmbDgxV2YyNnVRZm1td2lWRTRjaWNnbFdZYnVES3RMUVlGLWZBckNqOHVmMUNzTkdxNUN3WWdzeURqZ2pnIIEC; bili_jct=0ef0853e5e28b21b777362df6255238c; DedeUserID=363210839; DedeUserID__ckMd5=2b22cf0cf3c2e569; sid=63r4oah0; hit-dyn-v2=1; buvid4=731D40A3-2C52-0D41-0366-7671A76FE6FA35074-023090723-bevVgi1zYcBrN6qICkw4eA%3D%3D; fingerprint=8df36ecd52b746a8b5b1ace7c5dc1794; buvid_fp_plain=undefined; buvid_fp=8df36ecd52b746a8b5b1ace7c5dc1794; b_lsid=5D4F7A9F_190C0525B5E; bp_t_offset_363210839=955099150653849600",
        "referer": url,
    }

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


if __name__ == "__main__":
    main()
