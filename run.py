from command import FFmpegCmd as fc
import os
import shutil

from utils import *


def media_split_size(size_limit, reencode):
    if reencode=='y' or reencode=='Y' or reencode=='yes' or reencode=='Yes':
        reencode = True
    else:
        reencode = False
    media_list = get_all_media()
    selected_file = media_list[int(input('Select media to split: '))]
    file_name = os.path.splitext(selected_file)[0]
    ext = os.path.splitext(selected_file)[1]

    start_time = 0
    original_duration = fc.get_media_duration(selected_file)
    index = 1
    tmp = [start_time]

    while True:
        output_file = f'{file_name}-{index:02d}{ext}'
        fc.split_media_size(selected_file, output_file, start_time, size_limit, reencode)

        duration = fc.get_media_duration(output_file)
        start_time += duration
        tmp.append(start_time)
        if start_time >= original_duration:
            break
        index += 1

def media_split_time(time_limit):
    media_list = get_all_media()
    selected_file = media_list[int(input('Select media to split: '))]
    file_name = os.path.splitext(selected_file)[0]

    if time_limit[-1] == 's':
        segment_time = int(time_limit[:-1])
    elif time_limit[-1] == 'm':
        segment_time = int(time_limit[:-1]) * 60
    elif time_limit[-1] == 'h':
        segment_time = int(time_limit[:-1]) * 3600

    # bitrate = fc.get_video_bitrate(selected_file) / 1000 # kb/s
    # segment_time = (size * 1024 * 8) / bitrate # s
    
    output_file = f'{file_name}-%02d.mp4'
    fc.split_media_time(selected_file, output_file, segment_time)

def video_convert(mode):
    video_list = get_all_videos()
    selected_files = input('Select videos to convert: e.g. 0,1,2\n')
    try:
        video_selected_list = [video_list[int(i)] for i in selected_files.split(',')]
    except Exception as e:
        print(f'Invalid input: {e}')
        return

    track_list = []
    for video in video_selected_list:
        track = fc.get_audio_tracks(video)
        files_print(track)

        track_index = int(input(f'Select {video} track: '))
        track_list.append(track_index)

    for video, track_index in zip(video_selected_list, track_list):
        if mode == 'to_video':
            output_file = os.path.splitext(video)[0] + '.mp4'
            fc.convert_to_mp4(video, output_file, track_index)
        elif mode == 'to_audio':
            output_file = os.path.splitext(video)[0] + '.mp3'
            fc.extract_audio(video, output_file, track_index)

# def media_concat():
#     media_list = get_all_media()
#     selected_files = input('Select videos to concat: e.g. 0,1,2\n')
#     try:
#         selected_files = [media_list[int(i)] for i in selected_files.split(',')]
#     except Exception as e:
#         print(f'Invalid input: {e}')
#         return
    
#     codecs = fc.get_codecs(selected_files[0])
#     bsf = codec_to_bsf(codecs['video'])
    
#     files_TS = []
#     for index, file in enumerate(selected_files, start=1):
#         output_file = f'intermediate_{index}.ts'
#         fc.to_TS(file, output_file, bsf)
#         files_TS.append(output_file)
    
#     input_TS = 'concat:' + '|'.join(files_TS)
#     output_file = selected_files[0].split('-')[0] + '_concat' + os.path.splitext(selected_files[0])[1]

#     bsf = codec_to_bsf(codecs['audio'])
#     fc.concat_video(input_TS, output_file, bsf)
    
#     for file in files_TS:
#         os.remove(file)

def media_concat():
    media_list = get_all_media()
    selected_files = input('Select media files to concat: e.g. 0,1,2\n')
    try:
        selected_files = [media_list[int(i)] for i in selected_files.split(',')]
    except Exception as e:
        print(f'Invalid input: {e}')
        return
    
    with open('file_list.txt', 'w') as file_list:
        for i, file in enumerate(selected_files):
            shutil.copy(file, f'intermediate_{i}{os.path.splitext(file)[1]}')
            file_list.write(f"file 'intermediate_{i}{os.path.splitext(file)[1]}'\n")
    
    output_file = selected_files[0].split('-')[0] + '_concat' + os.path.splitext(selected_files[0])[1]
    fc.concat_media('file_list.txt', output_file)
    for i, file in enumerate(selected_files):
        os.remove(f'intermediate_{i}{os.path.splitext(file)[1]}')
    os.remove('file_list.txt')

def audio_combination():
    mp3_convert = input('Select video to convert to mp3? (y/n): ')
    if mp3_convert == 'y' or mp3_convert == 'Y' or mp3_convert == 'yes' or mp3_convert == 'Yes':
        video_convert(mode='to_audio')

    video_list = get_all_videos()
    selected_video_file = video_list[int(input('Select video to concat: '))]

    audio_list = get_all_audios()
    selected_audio_file = audio_list[int(input('Select audio to concat: '))]

    output_file = os.path.splitext(selected_video_file)[0] + '_combination.mp4'
    fc.audio_and_video_combination(selected_video_file, selected_audio_file, output_file)

def adjust_media_length(start_adjust, end_adjust):
    media_list = get_all_media()
    selected_video_file = media_list[int(input('Select media to cut: '))]

    file_nm, file_ext = os.path.splitext(selected_video_file)
    duration = fc.get_media_duration(selected_video_file)
    output_file = file_nm + '_adjust' + file_ext

    start_time = max(0, parse_time_string(start_adjust))
    end_time = min(0, parse_time_string(end_adjust))
    end_time = duration + end_time
    if end_time < 0:
        print(f'Invalid media length. The video length is {duration} seconds. \
              But the range is {start_time} to {end_time - start_time}')
        return
    fc.cut_media(selected_video_file, output_file, start_time, end_time)


if __name__ == '__main__':
    
    print(
    """
    \tPlease select run mode:
    \t0: convert to mp4
    \t1: concat media
    \t2: video extract audio
    \t3: media split(size)
    \t4: media split(time)
    \t5: audio and video combination
    \t6: adjust media length
    """
    )

    mode = int(input('Select mode: '))
    if mode == 0:
        video_convert(mode='to_video')
    elif mode == 1:
        media_concat()
    elif mode == 2:
        video_convert(mode='to_audio')
    elif mode == 3:
        input_size = input('Input segment size: ')
        reencode = input('Reencode? (y/n): ')
        media_split_size(input_size, reencode)
    elif mode == 4:
        input_size = input('Input segment time: ')
        media_split_time(input_size)
    elif mode == 5:
        audio_combination()
    elif mode == 6:
        start_adjust = input('Input start adjust time: e.g. 2h1m30s\n')
        end_adjust = input('Input end adjust time: e.g. 2h1m30s\n')
        adjust_media_length('+' + start_adjust, '-' + end_adjust)
    else:
        print('Invalid mode')
