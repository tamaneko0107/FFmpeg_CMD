import re
import os

from const import *


# 剪切影片長度字串判斷
def parse_time_string(time_str):
    if not time_str:
        return 0

    # 匹配時間格式，例如 2h30m10s
    pattern = r'([+-])?(\d+h)?(\d+m)?(\d+s)?'
    match = re.match(pattern, time_str)
    if not match:
        raise ValueError("Invalid time format")

    sign, hours, minutes, seconds = match.groups()
    total_seconds = 0

    if hours:
        total_seconds += int(hours[:-1]) * 3600
    if minutes:
        total_seconds += int(minutes[:-1]) * 60
    if seconds:
        total_seconds += int(seconds[:-1])

    if sign == '-':
        total_seconds = -total_seconds

    return total_seconds

# codec 轉 bsf
def codec_to_bsf(codec):
    if codec == 'h264':
        return 'h264_mp4toannexb'
    elif codec == 'hevc':
        return 'hevc_mp4toannexb'
    elif codec == 'aac':
        return 'aac_adtstoasc'
    else:
        return None

# 取得所有影片檔案
def get_all_videos():
    video_list = [file for file in os.listdir() if file.endswith(SUPPORTED_VIDEO_FORMATS)]
    files_print(video_list)
    return video_list

# 取得所有音訊檔案
def get_all_audios():
    audio_list = [file for file in os.listdir() if file.endswith(SUPPORTED_AUDIO_FORMATS)]
    files_print(audio_list)
    return audio_list

# 取得所有媒體檔案
def get_all_media():
    media_list = [file for file in os.listdir() if file.endswith(SUPPORTED_AUDIO_FORMATS + SUPPORTED_VIDEO_FORMATS)]
    files_print(media_list)
    return media_list

# 列印檔案清單
def files_print(mdeia_list):
    str = "\n"
    for i, file in enumerate(mdeia_list):
        str += f'\t{i}: {file}\n'
    print(str)