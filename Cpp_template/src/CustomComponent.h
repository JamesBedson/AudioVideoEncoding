#ifndef CUSTOMCOMPONENT_H
#define CUSTOMCOMPONENT_H

#include <QWidget>
#include <QPainter>
#include <QLabel>
#include <QVBoxLayout>

class CustomComponent : public QWidget {
    Q_OBJECT

public:
    CustomComponent(QWidget *parent = nullptr);
    

protected:
    void paintEvent(QPaintEvent *event) override;

private:
    QLabel* converterLabel;
    QLabel* youtubeLabel;
};

#endif // CUSTOMCOMPONENT_H
