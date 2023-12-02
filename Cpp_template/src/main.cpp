#include <QApplication>
#include <QLabel>
#include "MainWindow.h"

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);

    // Create an instance of MainWindow
    MainWindow mainWindow;
    mainWindow.setWindowTitle("FFMPEG Converter");
    mainWindow.setGeometry(100, 100, 800, 600);
    
    // Show the main window
    mainWindow.show();

    // Run the application event loop
    return a.exec();
}
