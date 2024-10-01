import subprocess


class FFmpegCmd():
    @staticmethod
    def get_audio_tracks(input_file):
        """
        args:
            input_file: str, input file path
        return:
            list of str, audio tracks
        """
        command = [
            'ffprobe',
            '-v', 'error',
            '-select_streams', 'a',
            '-show_entries', 'stream=index,codec_name',
            '-of', 'csv=p=0',
            input_file
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        return result.stdout.strip().split('\n')
    
    def get_codecs(input_file):
        video_codec_command = [
            'ffprobe',
            '-v', 'error',
            '-select_streams', 'v:0',
            '-show_entries', 'stream=codec_name',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            input_file
        ]
        audio_codec_command = [
            'ffprobe',
            '-v', 'error',
            '-select_streams', 'a:0',
            '-show_entries', 'stream=codec_name',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            input_file
        ]
        
        video_result = subprocess.run(video_codec_command, capture_output=True, text=True)
        audio_result = subprocess.run(audio_codec_command, capture_output=True, text=True)
        
        codecs = {
            'video': video_result.stdout.strip(),
            'audio': audio_result.stdout.strip()
        }
        
        return codecs
    
    @staticmethod
    def convert_to_mp4(input_file, output_file, audio_track):
        """
        args:
            input_file: str, input file path
            output_file: str, output file path
            audio_track: int, audio track index
        """
        command = [
            'ffmpeg',
            '-i', input_file,
            '-map', '0:v:0',  # 添加這行來包含視頻流
            '-map', f'0:a:{audio_track}',
            '-c:v', 'copy',
            '-c:a', 'copy',
            output_file
        ]
        subprocess.run(command)

    @staticmethod
    def to_TS(input_file, output_file, bsf):
        """
        args:
            input_file: str, input file path
            output_file: str, output file path
        """
        command = [
            'ffmpeg',
            '-i', input_file,
            '-c', 'copy',
            '-f', 'mpegts'
        ]
        if bsf:
            command += ['-bsf:v', bsf]
        command.append(output_file)
        subprocess.run(command)

    @staticmethod
    def concat_video(input_TS, output_file, codec):
        """
        args:
            input_files: str, input file paths
            output_file: str, output file path
        """
        command = [
            'ffmpeg',
            '-i', input_TS,
            '-c', 'copy'
        ]
        if codec:
            command += ['-bsf:a', 'aac_adtstoasc']
        command.append(output_file)
        subprocess.run(command)

    @staticmethod
    def concat_media(file_list, output_file):
        """
        args:
            file_list: str, path to the file list
            output_file: str, output file path
        """
        command = [
            'ffmpeg',
            '-f', 'concat',
            '-safe', '0',
            '-i', file_list,
            '-c', 'copy',
            output_file
        ]
        subprocess.run(command)

    @staticmethod
    def extract_audio(input_file, output_file, audio_track):
        """
        args:
            input_file: str, input file path
            output_file: str, output file path
            audio_track: int, audio track index
        """
        command = [
            'ffmpeg',
            '-i', input_file,
            '-map', f'0:a:{audio_track}',
            output_file
        ]
        subprocess.run(command)

    @staticmethod
    def get_video_bitrate(input_file):
        """
        args:
            input_file: str, input file path
        return:
            int, bitrate
        """
        command = [
            'ffprobe',
            '-v', 'error',
            '-show_entries', 'format=bit_rate',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            input_file
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        return int(result.stdout.strip())
    
    @staticmethod
    def get_media_duration(input_file):
        """
        args:
            input_file: str, input file path
        return:
            float, duration
        """
        command = [
            'ffprobe',
            '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            input_file
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        return float(result.stdout)
    
    @staticmethod
    def split_media_size(input_file, output_file, start_time, size_limit, reencode=False):
        """
        args:
            input_file: str, input file path
            output_file: str, output file path
            start_time: int, start time in seconds
            size_limit: int, size limit in bytes
        """
        command = [
            'ffmpeg',
            '-ss', str(start_time),
            '-i', input_file,
            '-fs', str(size_limit)
        ]
        if reencode:
            command += ['-c:v', 'libx264', '-c:a', 'aac']
        else:
            command += ['-c', 'copy']
        command.append(output_file)
        subprocess.run(command)

    @staticmethod
    def split_media_time(input_file, output_file, segment_time):
        """
        args:
            input_file: str, input file path
            output_file: str, output file path
            segment_time: int, segment time in seconds
        """
        command = [
            'ffmpeg',
            '-i', input_file,
            '-c', 'copy',
            '-map', '0',
            '-segment_time', str(segment_time),
            '-f', 'segment',
            '-reset_timestamps', '1',
            '-segment_start_number', '1',
            output_file
        ]
        subprocess.run(command)

    @staticmethod
    def audio_and_video_combination(input_file, audio_file, output_file):
        """
        args:
            input_file: str, input file path
            audio_file: str, audio file path
            output_file: str, output file path
        """
        command = [
            'ffmpeg',
            '-i', input_file,
            '-i', audio_file,
            '-c:v', 'copy',
            '-c:a', 'copy',
            '-map', '0:v:0',
            '-map', '1:a:0',
            output_file
        ]
        subprocess.run(command)

    @staticmethod
    def cut_media(input_file, output_file, start_time, end_time):
        """
        args:
            input_file: str, input file path
            output_file: str, output file path
            start_time: int, start time in seconds
            end_time: int, end time in seconds
        """
        command = [
            'ffmpeg',
            '-ss', str(start_time),
            '-i', input_file,
            '-t', str(end_time - start_time),
            '-c', 'copy',
            output_file
        ]
        subprocess.run(command)

