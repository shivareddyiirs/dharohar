#include <QThread>
#include <QMessageBox>
#include <ccGenericPointCloud.h>
#include <ccPointCloud.h>
#include <ccScalarField.h>
#include <fstream>
#include <string>
using namespace std;

class saveThread: public QThread
{
protected:
    ccGenericPointCloud* m_cloud;
    QString sql, project, imagefilename;

public:
    saveThread(ccGenericPointCloud *cloud, QString s, QString pro, QString img):m_cloud(cloud)
    , sql(s)
    , project(pro)
    , imagefilename(img){}

private:
    Q_OBJECT

    void run(){
        QString sqlfilename, createtablesql, imagetablename, pointstablename;

        sqlfilename = imagefilename + ".sql";
        createtablesql = "create" + sqlfilename;

        imagetablename = project + "_image";
        pointstablename = project + "_xyz";

        std::ofstream createtable, sqlfile;
        createtable.open(createtablesql.toStdString().c_str());

        createtable << "BEGIN;\n"
                    << "CREATE TABLE IF NOT EXISTS \"" << imagetablename.toStdString() << "\" (\"rid\" serial PRIMARY KEY,"
                    << "\"rast\" raster,\"filename\" text);\n"
                    << "END;\n"
                    << "BEGIN;\n"
                    << "CREATE TABLE IF NOT EXISTS " << pointstablename.toStdString() << "\n"
                    << "(\n"
                    << "\"rid\" integer REFERENCES " << imagetablename.toStdString() << "(rid) ON UPDATE CASCADE ON DELETE CASCADE,\n"
                    << "\"x\" double precision,\n"
                    << "\"y\" double precision,\n"
                    << "\"z\" double precision\n"
                    << ");\n"
                    << "END;\n";
        createtable.close();
        system((sql + createtablesql).toStdString().c_str());
        remove(createtablesql.toStdString().c_str());

        std::string command = " raster2pgsql -a -C -I -M -F ";
        command = command + imagefilename.toStdString() + " " + imagetablename.toStdString() + " > " + ("temp" + sqlfilename).toStdString();
        system(command.c_str());

        std::ifstream rasterOutput;
        rasterOutput.open(("temp" + sqlfilename).toStdString().c_str());

        sqlfile.open(sqlfilename.toStdString().c_str());
        getline(rasterOutput, command);
        sqlfile << command << endl;
        getline(rasterOutput, command);
        command = command.substr(0, command.size() - 1) + " RETURNING rid;";
        sqlfile << command << endl;
        sqlfile << "END;\n";
        sqlfile.close();
        system((sql + sqlfilename + " > output" + sqlfilename).toStdString().c_str());
        sqlfile.open(sqlfilename.toStdString().c_str());
        sqlfile << "BEGIN;\n";
        getline(rasterOutput, command);
        sqlfile << command << endl;
        getline(rasterOutput, command);
        sqlfile << command << endl;
        getline(rasterOutput, command);
        sqlfile << command << endl;
        getline(rasterOutput, command);
        sqlfile << command << endl;
        getline(rasterOutput, command);
        sqlfile << command << endl;
        sqlfile << "\n";
        rasterOutput.close();
        remove(("temp" + sqlfilename).toStdString().c_str());
        remove(imagefilename.toStdString().c_str());

        int i = m_cloud->getIndex(), rid;
        rasterOutput.open(("output" + sqlfilename).toStdString().c_str());
        getline(rasterOutput, command);
        getline(rasterOutput, command);
        getline(rasterOutput, command);
        rasterOutput >> rid;
        rasterOutput.close();
        remove(("output" + sqlfilename).toStdString().c_str());
        sqlfile << "\n\n";
        sqlfile << "COPY " << pointstablename.toStdString() << " (rid, x, y, z) FROM stdin;\n";
        for(; i < m_cloud->size(); i++){
            sqlfile << rid << "\t" << m_cloud->getPoint(i)->x << "\t" << m_cloud->getPoint(i)->y << "\t" << m_cloud->getPoint(i)->z << "\n";
        }
        sqlfile << "\\.\n";
        sqlfile << "VACUUM ANALYZE \"" << pointstablename.toStdString() << "\";\n";
        sqlfile.close();
        system((sql + sqlfilename).toStdString().c_str());
        remove(("output" + sqlfilename).toStdString().c_str());
        remove(sqlfilename.toStdString().c_str());
        emit savingDone();
    }

signals:
    void savingDone();
};
