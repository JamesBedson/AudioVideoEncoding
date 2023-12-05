import os, subprocess, re
from enum import Enum

class ConversionEvent(Enum):
    AUDIO_CONVERSION = 0
    VIDEO_CONVERSION = 1

class AudioOutputFormat(Enum):
    MP3     = "mp3 (LAME)"
    AAC     = "aac (Advanced Audio Codec)"
    WAV     = "wav (Pulse Code Modulation)"
    FLAC    = "flac (Free Lossless Audio Codec)"
    OGG     = "ogg (Vorbis)"
    M4A     = "m4a (Advanced Audio Codec)"
    AIFF    = "aiff (Pulse Code Modulation)"
    MP2     = "mp2 (MPEG Audio Layer II)"

class SampleRate(Enum):
    RATE_22_05_KHZ  = "22.05 kHz"
    RATE_32_KHZ     = "32 kHz"
    RATE_44_1_KHZ   = "44.1 kHz"
    RATE_48_KHZ     = "48 kHz"
    RATE_96_KHZ     = "96 kHz"
    RATE_192_KHZ    = "192 kHz"

class VideoOutputFormat(Enum):
    MP4         = "mp4 (Av1)"
    MKV         = "mkv (H.265)"
    MOV         = "mov (H.264)"
    WMV         = "wmv (Windows Media Video)"
    FLV         = "flv (H.264)"
    WEBM_VP8    = "webm (VP8)"
    WEBM_VP9    = "webm (VP9)"
    MPEG        = "mpeg (MPEG-2)"
    OGV         = "ogv (Theora)"

class VideoResolution(Enum):
    SD_160x120          = "160x120"
    SD_360x240          = "360x240"
    SD_640x480          = "640x480 (SD)"
    SD_720x480          = "720x480 (SD)"
    HD_1280x720         = "1280x720 (HD)"
    FULL_HD_1920x1080   = "1920x1080 (Full HD)"
    _2K_2048x1080       = "2048x1080 (2k)"
    QHD_2560x1440       = "2560x1440 (QHD)"
    _4K_3840x2160       = "3840x2160 (4k)"
    _4K_4096x2160       = "4096x2160 (4k)"

class Channels(Enum):
    MONO    = "Mono"
    STEREO  = "Stereo"

class Quality(Enum):
    LOW     = "Low"
    MEDIUM  = "Medium"
    HIGH    = "High"

qualityToIndex: dict[str, int] = {
                Quality.LOW.value: 2,
                Quality.MEDIUM.value: 1,
                Quality.HIGH.value: 0,
            }

sampleRateToFormat: dict[str, str] = {
    SampleRate.RATE_22_05_KHZ.value: "22050",
    SampleRate.RATE_32_KHZ.value: "32000",
    SampleRate.RATE_44_1_KHZ.value: "44100",
    SampleRate.RATE_48_KHZ.value: "48000",
    SampleRate.RATE_96_KHZ.value: "96000",
    SampleRate.RATE_192_KHZ.value: "192000"
}

videoCodecs: dict[str, str] = {
                VideoOutputFormat.MP4.value:        "libaom-av1",
                VideoOutputFormat.MKV.value:        "libx265",
                VideoOutputFormat.MOV.value:        "libx264",
                VideoOutputFormat.WMV.value:        "wmv2",
                VideoOutputFormat.FLV.value:        "libx264",
                VideoOutputFormat.WEBM_VP8.value:   "libvpx",
                VideoOutputFormat.WEBM_VP9.value:   "libvpx-vp9",
                VideoOutputFormat.MPEG.value:       "mpeg2video",
                VideoOutputFormat.OGV.value:        "libtheora",
            }

audioCodecs: dict[str, str] = {
                AudioOutputFormat.MP3.value: "libmp3lame",
                AudioOutputFormat.AAC.value: "aac",
                AudioOutputFormat.WAV.value: "pcm_s16le",
                AudioOutputFormat.FLAC.value: "flac",
                AudioOutputFormat.OGG.value: "libvorbis",
                AudioOutputFormat.M4A.value: "aac",
                AudioOutputFormat.AIFF.value: "pcm_s16be",
                AudioOutputFormat.MP2.value: "mp2",
                }

videoQualitySettings: dict[str, tuple[str, list[str]]] = {
    "libaom-av1":    ("-crf", ["20", "30", "40"]),
    "libx265":       ("-crf", ["18", "23", "28"]),
    "libx264":       ("-crf", ["18", "23", "28"]),
    "wmv2":          ("-q:v", ["1", "20", "31"]),
    "libvpx":        ("-crf", ["20", "30", "40"]),  
    "libvpx-vp9":    ("-crf", ["20", "30", "40"]),
    "mpeg2video":    ("-b:v", ["8000k", "5000k", "500k"]),
    "libtheora":     ("-q:v", ["-1", "5", "10"]),
}

audioQualitySettings: dict[str, tuple[str, list[str]]] = {
    "libmp3lame":   ("-q:a", ["320k", "192k", "64k"]),
    "aac":          ("-b:a", ["256k", "128k", "64k"]),
    "flac":         ("-compression_level", ["8", "5", "2"]),
    "libvorbis":    ("-q:a", ["6", "4", "2"]),
    "aac":          ("-b:a", ["256k", "128k", "64k"]),
    "ac3":          ("-b:a", ["640k", "384k", "192k"]),
    "amr_nb":       ("-ab", ["23.85k", "12.2k", "5.9k"]),
    "mp2":          ("-b:a", ["192k", "128k", "64k"]),
}

class FFMPEG_Context:
    def __init__(self) -> None:
        pass


    def getVideoInformation(self, videoPath) -> dict[str, str]:
        cmd     = ["ffmpeg", "-i", videoPath]
        result  = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        resolutionMatch = re.search(r"(\d{3,4}x\d{3,4})", result.stderr)
        frameRateMatch  = re.search(r"(\d+(\.\d+)?) fps", result.stderr)
        codecsMatch     = re.search(r"Video: ([^,]+),", result.stderr)
        codecsString    = str(codecsMatch.group(1)).split(" ")[0] #type: ignore

        videoInfo = {
            "resolution": resolutionMatch.group(1) if resolutionMatch else "N/A",
            "rate": frameRateMatch.group(1) if frameRateMatch else "N/A",
            "codecs": codecsString if codecsMatch else "N/A",
        }
        return videoInfo
    
    
    def getAudioInformation(self, videoPath) -> dict[str, str]:
        cmd = ["ffmpeg", "-i", videoPath]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        audioCodecMatch = re.search(r"Audio: ([^,]+),", result.stderr)
        sampleRateMatch = re.search(r"(\d+) Hz", result.stderr)
        resolutionMatch = re.search(r"(\d+)x(\d+)", result.stderr)

        audioInfo = {
            "codecs": audioCodecMatch.group(1) if audioCodecMatch else "N/A",
            "rate": sampleRateMatch.group(1) if sampleRateMatch else "N/A",
            "resolution": f"{resolutionMatch.group(1)}x{resolutionMatch.group(2)}" if resolutionMatch else "N/A",
        }
        return audioInfo


    def convert(self, 
                event: ConversionEvent, 
                inputFilePath: str, 
                outputFilePath: str, 
                conversionSettings: dict) -> None:

        if event == ConversionEvent.VIDEO_CONVERSION:
            outputFormat    = str(conversionSettings[VideoOutputFormat])
            resolution      = str(conversionSettings[VideoResolution])
            channels        = str(conversionSettings[Channels])
            quality         = str(conversionSettings[Quality])

            chosenCodec     = videoCodecs[outputFormat]
            chosenRes       = resolution.split(" ")[0]

            qualityIdx      = qualityToIndex[quality]
            chosenQuality   = videoQualitySettings[chosenCodec][1][qualityIdx]

            cmd = [
                "ffmpeg",
                "-i", inputFilePath,
                "-c:v", f"{chosenCodec}",
                "-vf", f"scale={chosenRes}",
                "-ac", "1" if channels == Channels.MONO.value else "2",
                videoQualitySettings[chosenCodec][0], chosenQuality,
                outputFilePath
            ]

            subprocess.run(cmd, input="y".encode())

        elif event == ConversionEvent.AUDIO_CONVERSION:
            outputFormat    = str(conversionSettings[AudioOutputFormat])
            sampleRate      = str(conversionSettings[SampleRate])
            channels        = str(conversionSettings[Channels])
            quality         = str(conversionSettings[Quality])
            
            print(conversionSettings)
            chosenCodec         = audioCodecs[outputFormat]
            chosenSampleRate    = sampleRateToFormat[sampleRate]
            qualityIdx          = qualityToIndex[quality]

            cmd = [
                "ffmpeg",
                "-i", inputFilePath,
                "-c:a", f"{chosenCodec}",
                "-ar", f"{chosenSampleRate}",]

            if outputFormat != AudioOutputFormat.AIFF.value and outputFormat != AudioOutputFormat.WAV.value:
            
                chosenQuality = audioQualitySettings[chosenCodec][1][qualityIdx]
                cmd.append(f"{audioQualitySettings[chosenCodec][0]}")
                cmd.append(f"{chosenQuality}")

            cmd.append("-ac")
            cmd.append("1" if channels == Channels.MONO.value else "2")
            cmd.append(outputFilePath)


            result = subprocess.run(cmd, input="y".encode(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(result.stdout)
            print(result.stderr)

        else:
            print("Invalid conversion event")
            return

