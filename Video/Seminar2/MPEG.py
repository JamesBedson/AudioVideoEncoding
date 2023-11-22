import subprocess
import utils
from Lab2.MP2_Converter import get_info_from_video
import re

class MPEG:

    '''1) Start a Python script that, with the help from FFMpeg, it will have a method inside a Class, 
    which will output a video that will show the macroblocks and the motion vectors'''
    def show_macroblocks_and_motion_vectors(self, in_fp: str, out_fp: str, ) -> None:
        
        cmd = ["ffmpeg", "-flags2", "+export_mvs", "-i", in_fp, "-vf", "codecview=mv=pf+bf", out_fp]
        subprocess.run(cmd)


    '''2) You're going to create another method in order to create a new BBB container.'''
    def create_container(self, in_fp: str, out_fp: str) -> None:
        
        fp_50s = "../bbb_50s.mp4"
        
        # Cut BBB into 50 seconds only video.
        utils.cut_video_duration(in_fp      = in_fp,
                                 out_fp     = fp_50s,
                                 start_time = "00:01:20",
                                 end_time   = "00:02:10")
        
        fp_mp3_mono = "../bbb_mp3_mono.mp3"
        # Export BBB(50s) audio as MP3 mono track.
        cmd_mp3_mono    = ["ffmpeg", "-i", fp_50s, "-vn", "-ac", "1", fp_mp3_mono] 
        subprocess.run(cmd_mp3_mono)

        #Export BBB(50s) audio in MP3 stereo w/ lower bitrate
        # lower --> we must first find the original bitrate of the audio

        info = get_info_from_video(video_path = fp_50s)
        info = str(info)
        bit_rate_match  = re.search(r"Stream #\d:\d\[\S+\]: Audio: .+, (\d+) kb/s", info)
        bit_rate_mp3    = int(bit_rate_match.group(1)) if bit_rate_match else None

        if bit_rate_mp3 == None or bit_rate_mp3 not in [128, 192, 256, 320]:  
            bit_rate_mp3 = 128

        # Now we can lower the bitrate and export
        fp_mp3_stereo   = f"../bbb_mp3_stereo_{bit_rate_mp3}k.mp3"
        cmd_mp3_stereo  = ["ffmpeg", "-i", fp_50s, "-vn", "-ac", "2", "-b:a", f"{bit_rate_mp3}k", fp_mp3_stereo]
        subprocess.run(cmd_mp3_stereo)

        # Export BBB(50s) audio in AAC codec
        fp_aac  = "../bbb_aac.aac"
        cmd_aac = ["ffmpeg", "-i", fp_50s, "-vn", "-ac", "2", fp_aac]
        subprocess.run(cmd_aac)

        # Finally, create containers 
        cmd_container       = ["ffmpeg", 
                               "-i", fp_mp3_mono, 
                               "-i", fp_mp3_stereo, 
                               "-i", fp_aac,
                               "-map", "0:a",
                               "-map", "1:a",
                               "-map", "2:a", 
                               "-c", "copy", 
                               out_fp]
        
        subprocess.run(cmd_container)


    '''3) Create another method which reads the tracks from an MP4 container, and it's 
    able to say how many tracks does the container contains'''
    
    def read_tracks(self, in_fp: str) -> None: 
        
        cmd     = ["ffmpeg", "-i", in_fp]
        info    = subprocess.run(cmd, capture_output = True, text = True)
        output_lines = info.stderr.split("\n")
        streams = []

        for line in output_lines:
            if "Stream" in line:
                streams.append(line)
        
        print(f"The number of tracks is: {len(streams)}")
        print(stream for stream in streams)    





