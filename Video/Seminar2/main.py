import sys
sys.path.append("..")
import utils
import MPEG as mv
import download_subs
import extract_histogram

def ex1():
    in_fp   = "../big_buck_bunny.mp4"
    out_fp  = "../bbb_9s.mp4" 
    utils.cut_video_duration(in_fp      = in_fp, 
                             out_fp     = out_fp,
                             start_time = "00:01:10", 
                             end_time   = "00:01:19")
    
    mpeg_class = mv.MPEG()
    mpeg_class.show_macroblocks_and_motion_vectors(in_fp    = out_fp, 
                                                   out_fp   = "../bbb_motion_vectors.mp4")
    
def ex2():
    in_fp   = "../big_buck_bunny.mp4"
    out_fp  = "../bbb_merged_container.mp4"

    mpeg_class = mv.MPEG()
    mpeg_class.create_container(in_fp   = in_fp,
                                out_fp  = out_fp)
    
def ex3():
    in_fp   = "../bbb_merged_container.mp4"
    mpeg_class = mv.MPEG()
    mpeg_class.read_tracks(in_fp)

def ex4_5():
    # Using a new open source video that actually contains subtitles 
    sintel_fp   = "../sintel.mp4"
    yt_url      = "https://www.youtube.com/watch?v=eRsGyueVLvQ&t=235s"
    subs_fp     = "sintel.srt" 
    
    '''5) Now inheritate the new script into the old one, and call that function to execute'''
    download_subs.download_subtitles(yt_url, file_name = subs_fp.split(".")[0])
    
    download_subs.convert_vtt_to_srt(vtt_file = subs_fp.split(".")[0] + ".en.vtt", 
                                     srt_file = subs_fp)
    
    download_subs.integrate_subtitles(in_fp     = sintel_fp,
                                      subs_fp   = subs_fp)
    
     
def ex6():
    video_fp = "../sintel.mp4"
    extract_histogram.extract_yuv_hist(video_fp)



def main():  
    #ex1()
    #ex2()
    #ex3()
    #ex4_5()
    ex6()


if __name__ == "__main__":
    main()