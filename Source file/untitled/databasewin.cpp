

#include "databasewin.h"
#include <QtGui>
#include <QMessageBox>
#include <QDir>
#include <QCoreApplication>
#include <QDebug>
#include <QProcess>




Databasewin::Databasewin(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::Databasewin)
{
    ui->setupUi(this);
    connect ( ui->store, SIGNAL( clicked() ), this, SLOT( store_clicked() ) );
}

Databasewin::~Databasewin()
{
    delete ui;
}


void Databasewin::store_clicked()
{       //QProcess process;
        // QString scriptFile = QDir::currentPath() + "cmd.exe C:/Python27/python p3.py";
       //bool const str= process.startDetached("\""+QDir::currentPath()+ "/C:/Python27 /python edge.py\"");
        //process.waitForFinished();
       // QString str = process.readAllStandardOutput();
        //qDebug()<<str;

//    QProcess process;
  // QString scriptFile = QDir::currentPath() + "C:/Python27/p3.py";

 // QStringList pythonCommandArguments = QStringList() << scriptFile;

  // printf("PyCommand: %s\n", qStringToStdString(pythonCommandArguments.join(' ')).c_str());

    //process.start("c:/Python27/python.exe"+scriptFile);

    QProcess *myProcess = new QProcess(this);

    myProcess->startDetached("C:/Python27/python C:/Python27/chck1.py ");


    //std::string command= "c:/";

    //system(" cd \Python27\python ie.py");


     //QString filename1="C:/Python27/p2.py";
    //QString cmd_qt = QString("python %1script.py").arg(filename1);
      // QProcess::execute (cmd_qt);
     //const char* cmd1 = cmd_qt.toLocal8Bit().constData();
      // system(cmd1);
      //system("pause>nul");
      //QMessageBox::information( this, "Information", "RASTER STORED INTO DATABASE" );

}
