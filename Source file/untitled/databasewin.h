#ifndef DATABASEWIN_H
#define DATABASEWIN_H

#include <QMainWindow>
//#include <QPushButton>
#include "ui_databasewin.h"

namespace Ui {
class Databasewin;
}

class Databasewin : public QMainWindow
{
    Q_OBJECT

public:
    explicit Databasewin(QWidget *parent = 0);
    ~Databasewin();
 // QPushButton *store;

private slots:


   // void store_clicked();

    void store_clicked();

private:
    Ui::Databasewin *ui;

};

#endif // DATABASEWIN_H
