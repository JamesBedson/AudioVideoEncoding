import os, sys
sys.path.append("../../")
from FFMPEG_Converter_Python.FFMPEG_Functions import * 
from itertools import product

def exercise1() -> None:

    # The FFMPEG_Context class is a converter class that acts as a context between python and ffmpeg.
    print("Creating Context...")
    context = FFMPEG_Context()

    '''1 ) Remember you have the BBB video converted into these? If not, convert it now!
        720p
        480p
        360x240
        160x120'''

    # In order to convert a video using the context, we must provide some parameters:
    
    cEvent: ConversionEvent     = ConversionEvent.VIDEO_CONVERSION      # The conversion event tells the context what type of conversion it should perform
    
    cSettings: dict    = {                                              # The converter takes in a dictionary of different Enums (kind of like constant classes) that specify the different possible settings for ffmpeg
         
            VideoOutputFormat:  VideoOutputFormat.MP4.value,            # As of now, the converter lets you specify the extension, rather than the codec itself for simplicity (see GUI), 
                                                                        # which is a little cumbersome and will be modified in the future. 
                                                                        # You can find the codecs used for each extension in the FFMPEG_Functions file.
            VideoResolution:    "",                
            Channels:           Channels.STEREO.value,
            Quality:            Quality.HIGH.value                      # The quality lets you choose the output quality, i.e. the compression settings of the codec. 
                                                                        # To find out the "meaning" behind the "low", "medium" and "high" options, refer to the FFMPEG_Functions file
    }

    # Create MP4s with the target resolutions
    targetResolutions = [
        VideoResolution.HD_1280x720.value, 
        VideoResolution.SD_640x480.value, 
        VideoResolution.SD_360x240.value, 
        VideoResolution.SD_160x120.value
        ]
    
    targetOutputFormats = [
        #VideoOutputFormat.MP4.value,        # Uses the AV1 Codec
        VideoOutputFormat.WEBM_VP8.value,   # Uses the VP8 Codec
        VideoOutputFormat.WEBM_VP9.value,   # Uses the VP9 Codec
        VideoOutputFormat.MKV.value         # Uses the h265 Codec
    ]

    videoPathIn = "bbb_9seconds.mp4"
    fileNameWithExtension   = os.path.basename(videoPathIn)
    fileNameNoExtension, _  = os.path.splitext(fileNameWithExtension)

    # This mega for loop creates a separate file i.e. applies the different codecs to
    # each of the resolutions we previously exported

    for outFormat, resolution in product(targetOutputFormats, targetResolutions):
        cSettings[VideoOutputFormat]    = outFormat
        cSettings[VideoResolution]      = resolution

        print(f"Encoding {outFormat} and {resolution}")

        newFileNameWithExtension    = os.path.basename(fileNameNoExtension) 
        newFileNameNoExtension, _   = os.path.splitext(newFileNameWithExtension)
        videoPathOut                = os.path.join("..", f"{newFileNameNoExtension}_{outFormat}_{resolution.split(' ')[0]}.{outFormat.split(' ')[0]}")
        
        context.convert(event               = cEvent, 
                        inputFilePath       = videoPathIn,
                        outputFilePath      = videoPathOut,
                        conversionSettings  = cSettings)

def exercise2() -> None:

    '''2) Create a script that will export 2 video comparision.
        For example: VP8 vs VP9 (both in same screen).'''
    
    videoFilePath_VP8 = "../bbb_9seconds_webm (VP8)_1280x720.webm"
    videoFilePath_VP9 = "../bbb_9seconds_webm (VP9)_1280x720.webm"

    cmd = ["ffmpeg",
            "-i", videoFilePath_VP8,
            "-i", videoFilePath_VP9,
            "-filter_complex", "[0:v]drawtext=text='VP8':x=(w-text_w)/2:y=H-th-10:fontsize=30:fontcolor=white[vp8]; [1:v]drawtext=text='VP9':x=(w-text_w)/2:y=H-th-10:fontsize=30:fontcolor=white[vp9]; [vp8][vp9]hstack",
            "VP8_vs_VP9.mp4"
            ]
    
    subprocess.run(cmd)

    '''Comment on the differences you find there'''
    # The quality settings for both videos were set to the same value (high) 
    # and the same resolution when they were exported. Nevertheless, the VP8
    # codec seems to compress the video a lot more and the output looks more 
    # pixelated. It seems as though it is loosing out on more resolution, i.e.
    # it looks like the video has been downsampled (even though it still main-
    # tains the same resolution (1280x720)). Looking at the file size, we see
    # that the VP9 video is much larger than the VP9 video.

def exercise4() -> None:
    pass
