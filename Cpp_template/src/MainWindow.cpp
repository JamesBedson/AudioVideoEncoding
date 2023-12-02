#include "MainWindow.h"

MainWindow::MainWindow(QWidget *parent) : QMainWindow(parent)
{
    // Create centralWidget and set it as the central widget
    QWidget* centralWidget = new QWidget(this);
    setCentralWidget(centralWidget);

    // Create a layout for centralWidget
    QHBoxLayout *layout = new QHBoxLayout(centralWidget);

    // Create the tab widget
    QTabWidget* tabWidget = new QTabWidget(centralWidget);

    // Create the tabs
    QWidget *converter = new QWidget();
    QWidget *youtubeDownload = new QWidget();
    tabWidget->addTab(converter, "Convert File");
    tabWidget->addTab(youtubeDownload, "Download From Youtube");

    // Add the tab widget to the layout
    layout->addWidget(tabWidget);
}

MainWindow::~MainWindow()
{
}

void MainWindow::paintEvent(QPaintEvent *event) {
}
