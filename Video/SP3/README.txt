This README file is addressed to the person correcting and grading SP3 from the Audio and Video Coding Course.

FFMPEG Scripts:
    - Most of the FFMPEG Scripts are contained within a .py file called "FFMPEG_Functions" within the FFMPEG_Converter_Python directory.
    A description of what the FFMPEG_Context class does and how to use it can be found in the SP3_Scripts.py file within the SP3 directory.


GUI App: General
    - The GUI application is an audio and video converter. As of the date of this deliverable, the GUI App is not finished yet. 
    The idea was for the GUI application to not only convert audio and video files, but to also include a youtube downloader. 
    The youtube video downloader is not implemented yet. However, I plan to continue to develop this application, at least until 
    I have fully tested and debugged all of the features.


GUI App: How to Run    

    DEPENDENCIES:
        - The GUI Application is based on the PyQt6 library. I have linked a requirements.txt from my venv which can be used to install all 
        of the dependencies of the project, in case the person reading this is interested in running the app. Should you want to run the app, 
        I strongly advise you to clone the github repository, as most of the module paths depend on the structure laid out in the repo.

    PATH ISSUES:
        - Speaking of paths, the assets that are used in the project are referenced using hard-coded paths in the application. For some reason,
        PyQt had trouble reading relative paths and I haven't had time to fix the issue, so please excuse this workaround for the time being.  
    
        - In any case, the paths are listed in the Paths.py file and the application should render the assets if you simply copy and paste the absolute
        paths from your machine.

    I CAN'T BE BOTHERED TO RUN YOUR APP, MATE:
        - Should you not want to run the app, A video showing the basic functionality of the app can be found in the Zip file in aula global, 
        as well as screenshots of the app.


Docker:

    - My initial idea was to have the docker container run the FFMPEG Converter app that was created in the context of this lab, in order for
    the user or reader of this document to not have to install the dependencies and just be able to run the script. However, there
    were some issues installing the dependencies, in particular PyQt. That's also something I'll look into in the future.

    - Right now, if you build the docker file (from the github repository), it will run exercise 1 from this lab and create the different video
    files. I know this is not the most creative thing in the world, but I need to study for my exams!

    - I haven't published the docker image and I don't plan on doing so (at least until I figure out how to run a PyQt app in a container!). So,
    if you are going to run the docker, you'll have to do so from the repository, for the same reason as before.


If you made it this far, congrats and thank you for reading :)
