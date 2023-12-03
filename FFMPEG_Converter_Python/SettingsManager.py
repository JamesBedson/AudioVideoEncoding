from PyQt6.QtCore import pyqtSignal, QObject
from enum import Enum
import os
from FFMPEG_Functions import *

class SignalManager(QObject):
    fileDropped = pyqtSignal()

class FileCategory(Enum):
    AUDIO_FILE  = "audio-file"
    VIDEO_FILE  = "video-file"
    UNKNOWN     = "unknown"

class SettingsManager:
    def __init__(self):
        self.currentInputFilePath   = ""
        self.currentOutputFilePath  = ""
        self.resetFile()
        self.resetSettings()
        self.context = FFMPEG_Context()
        
    def setNewInputFilePath(self, filePath: str) -> None:
        self.currentInputFilePath = filePath

    def setNewOutputFilePath(self, filePath: str) -> None:
        self.currentOutputFilePath = filePath
    
    def getCurrentInputFilePath(self) -> str | None:
        return self.currentInputFilePath
    
    def getCurrentFileInformation(self):
        return self.fileInfo
    
    def resetFile(self) -> None:
        self.fileInfo = {
                'name': "",
                'extension': "",
                'size': "",
                'category': "",
                'rate': "",
                'resolution': "",
                'codecs': ""
            }
        
    def resetSettings(self) -> None:
        self.currentAudioSettings = {
            AudioOutputFormat: "",
            SampleRate: "",
            Channels: "",
            Quality: "" 
        }

        self.currentVideoSettings = {
            VideoOutputFormat: "",
            VideoResolution: "",
            Channels: "",
            Quality: ""
        }
        
    def getCategoryFromExtension(self, extension: str) -> FileCategory:
        validExtensions = self.getValidExtensions()

        if extension in validExtensions["videoExtensions"]:
            return FileCategory.VIDEO_FILE
        
        elif extension in validExtensions["audioExtensions"]:
            return FileCategory.AUDIO_FILE
        
        else:
            return FileCategory.UNKNOWN
        
    def formatFileSize(self, size: float) -> str:
        
        units = ['B', 'KB', 'MB', 'GB']
        unit_index = 0
        
        while size > 1024 and unit_index < len(units) - 1:
            size = size / 1024.0
            unit_index += 1

        formatted_size = "{:.2f} {}".format(size, units[unit_index])
        return formatted_size

    def updateFileInfo(self) -> None:
        
        if self.currentInputFilePath:
            fileSize        = os.path.getsize(self.currentInputFilePath)  # Size in bytes
            formattedSize   = self.formatFileSize(fileSize)

            fileName, fileExtension = os.path.splitext(os.path.basename(self.currentInputFilePath))
            category    = self.getCategoryFromExtension(fileExtension)
            missingInfo = {"resolution": "-", "rate": "-", "codecs": "-"}

            if category == FileCategory.VIDEO_FILE:
                missingInfo = self.context.getVideoInformation(self.currentInputFilePath)
                missingInfo["rate"] = missingInfo["rate"] + " fps"

            elif category == FileCategory.AUDIO_FILE:
                missingInfo = self.context.getAudioInformation(self.currentInputFilePath)
                missingInfo["rate"] = missingInfo["rate"] + " Hz"

            self.fileInfo["name"]       = fileName
            self.fileInfo["extension"]  = fileExtension
            self.fileInfo["size"]       = formattedSize
            self.fileInfo["category"]   = category.value
            self.fileInfo["rate"]       = missingInfo["rate"]
            self.fileInfo["resolution"] = missingInfo["resolution"]
            self.fileInfo["codecs"]     = missingInfo["codecs"]

     
    def getValidExtensions(self) -> dict[str, list]:
        
        audioExtensions = [".mp3", ".aac", ".wav", ".flac", ".ogg", ".m4a", ".ac3", ".aiff", ".amr", ".mp2"]
        videoExtensions = [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm", ".mpeg", ".ogv", ".3gp"]

        return {
            "audioExtensions": audioExtensions,
            "videoExtensions": videoExtensions
        }
    
    def sendConversionEvent(self, event: ConversionEvent) -> None:
        if event == ConversionEvent.AUDIO_CONVERSION:
            self.context.convert(event, self.currentInputFilePath, self.currentOutputFilePath, self.fileInfo, self.currentAudioSettings)
        else:
            self.context.convert(event, self.currentInputFilePath, self.currentOutputFilePath, self.fileInfo, self.currentVideoSettings)
    
