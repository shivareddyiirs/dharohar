/********************************************************************************
** Form generated from reading UI file 'databasewin.ui'
**
** Created by: Qt User Interface Compiler version 5.6.1
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_DATABASEWIN_H
#define UI_DATABASEWIN_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QButtonGroup>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_Databasewin
{
public:
    QWidget *centralwidget;
    QPushButton *store;
    QMenuBar *menubar;
    QStatusBar *statusbar;

    void setupUi(QMainWindow *Databasewin)
    {
        if (Databasewin->objectName().isEmpty())
            Databasewin->setObjectName(QStringLiteral("Databasewin"));
        Databasewin->resize(800, 600);
        centralwidget = new QWidget(Databasewin);
        centralwidget->setObjectName(QStringLiteral("centralwidget"));
        store = new QPushButton(centralwidget);
        store->setObjectName(QStringLiteral("store"));
        store->setGeometry(QRect(30, 60, 75, 23));
        Databasewin->setCentralWidget(centralwidget);
        menubar = new QMenuBar(Databasewin);
        menubar->setObjectName(QStringLiteral("menubar"));
        menubar->setGeometry(QRect(0, 0, 800, 21));
        Databasewin->setMenuBar(menubar);
        statusbar = new QStatusBar(Databasewin);
        statusbar->setObjectName(QStringLiteral("statusbar"));
        Databasewin->setStatusBar(statusbar);

        retranslateUi(Databasewin);

        QMetaObject::connectSlotsByName(Databasewin);
    } // setupUi

    void retranslateUi(QMainWindow *Databasewin)
    {
        Databasewin->setWindowTitle(QApplication::translate("Databasewin", "DATABASE", 0));
        store->setText(QApplication::translate("Databasewin", "store", 0));
    } // retranslateUi

};

namespace Ui {
    class Databasewin: public Ui_Databasewin {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_DATABASEWIN_H
