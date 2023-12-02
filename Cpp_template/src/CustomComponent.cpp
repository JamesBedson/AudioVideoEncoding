#include "CustomComponent.h"

CustomComponent::CustomComponent(QWidget *parent) : QWidget(parent) {
    // Initialize and set up your custom component
    // Add widgets, layouts, signals, slots, etc.
    converterLabel  = new QLabel(this);
    youtubeLabel    = new QLabel(this);
    converterLabel->setText("Converter");
    youtubeLabel->setText("Donwload From Youtube");

    QHBoxLayout* layout = new QHBoxLayout(this);
    layout->addWidget(converterLabel);
    layout->addWidget(youtubeLabel);
    
}

void CustomComponent::paintEvent(QPaintEvent *event) {

    // QPainter painter(this);
    // QRect labelRect = converterLabel->geometry();
    // QRect label2Rect = youtubeLabel->geometry(); 
    // painter.drawRect(labelRect);
    // painter.drawRect(label2Rect);

}


