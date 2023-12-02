from PyQt6.QtMultimedia import QMediaPlayer #, QMediaContent
from PyQt6.QtMultimediaWidgets import QVideoWidget
from enum import Enum
import os

class FileCategory(Enum):
    AUDIO_FILE  = "audio-file"
    VIDEO_FILE  = "video-file"
    UNKNOWN     = "unknown"

class FileManager:
    def __init__(self):
        self.resetFile()
        
    def setNewFilePath(self, filePath: str) -> None:
        self.currentFilePath = filePath
        return
    
    def getCurrentFilePath(self) -> str | None:
        return self.currentFilePath
    
    def getCurrentFileInformation(self):
        return self.fileInfo
    
    def resetFile(self) -> None:
        self.currentFilePath = None
        self.fileInfo = self.fileInfo = {
                'name': "",
                'extension': "",
                'size': "",
                'category': "",
                'rate': "",
                'resolution': "",
                'codecs': "",
                'channels': ""
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
        if self.currentFilePath:
            fileSize = os.path.getsize(self.currentFilePath)  # Size in bytes
            formattedSize = self.formatFileSize(fileSize)

            fileName, fileExtension = os.path.splitext(os.path.basename(self.currentFilePath))
            
            category            = self.getCategoryFromExtension(fileExtension)
            readyForProcessing  = False
            
            if category == FileCategory.AUDIO_FILE or category == FileCategory.VIDEO_FILE:
                readyForProcessing = True
            
            self.fileInfo["name"]       = fileName
            self.fileInfo["extension"]  = fileExtension
            self.fileInfo["size"]       = formattedSize
            self.fileInfo["category"]   = category.value
             

        
    def getValidExtensions(self) -> dict[str, list]:
        
        audioExtensions = [".mp3", ".aac", ".wav", ".flac", ".ogg", ".m4a", ".ac3", ".aiff", ".amr", ".mp2"]
        videoExtensions = [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm", ".mpeg", ".ogv", ".3gp"]

        return {
            "audioExtensions": audioExtensions,
            "videoExtensions": videoExtensions
        }