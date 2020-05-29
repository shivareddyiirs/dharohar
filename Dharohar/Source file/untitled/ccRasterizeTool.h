//##########################################################################
//#                                                                        #
//#                              CLOUDCOMPARE                              #
//#                                                                        #
//#  This program is free software; you can redistribute it and/or modify  #
//#  it under the terms of the GNU General Public License as published by  #
//#  the Free Software Foundation; version 2 or later of the License.      #
//#                                                                        #
//#  This program is distributed in the hope that it will be useful,       #
//#  but WITHOUT ANY WARRANTY; without even the implied warranty of        #
//#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the          #
//#  GNU General Public License for more details.                          #
//#                                                                        #
//#          COPYRIGHT: EDF R&D / TELECOM ParisTech (ENST-TSI)             #
//#                                                                        #
//##########################################################################

#ifndef CC_RASTERIZE_TOOL_HEADER
#define CC_RASTERIZE_TOOL_HEADER

#include <ui_rasterizeDlg.h>

//Local
#include "cc2.5DimEditor.h"

//Qt
#include <QString>

#include <QThread>
#include <QMessageBox>
#include <ccGenericPointCloud.h>
#include <ccPointCloud.h>
#include <ccScalarField.h>
#include <fstream>
#include <string>
#include <cmath>
using namespace std;

class ccGenericPointCloud;
class ccPointCloud;
class ccPolyline;

//! Rasterize tool (dialog)
class ccRasterizeTool : public QDialog, public cc2Point5DimEditor, public Ui::RasterizeToolDialog
{
    friend class saveThread;
	Q_OBJECT

public:
	//! Default constructor
	ccRasterizeTool(ccGenericPointCloud* cloud, QWidget* parent = 0);

	//! Destructor
	~ccRasterizeTool();

public: //raster export

	//! Bands to be exported
	struct ExportBands
	{
		bool height = true;
		bool rgb = false;
		bool density = false;
		bool visibleSF = false;
		bool allSFs = false;
	};

	//! Exports a raster grid as a geotiff file
	static bool ExportGeoTiff(	QString outputFilename,
								const ExportBands& exportBands,
								ccRasterGrid::EmptyCellFillOption fillEmptyCellsStrategy,
								const ccRasterGrid& grid,
								const ccBBox& gridBBox,
								unsigned char Z,
								double customHeightForEmptyCells = std::numeric_limits<double>::quiet_NaN(),
								ccGenericPointCloud* originCloud = 0,
								int visibleSfIndex = -1);

protected slots:

	//! Exports the grid as a cloud
	ccPointCloud* generateCloud(bool autoExport = true) const;

	//! Exports the grid as a raster
	void generateRaster() const;

	//! Exports the grid as a mesh
	void generateMesh() const;

	//! Exports the (already generated) contour lines
	void exportContourLines();

	//! Generates a contour plot
	void generateContours();

	//! Generates hillshade
	void generateHillshade();

	//! Removes all displayed contour lines
	void removeContourLines();

	//! Accepts the dialog (if some conditions are met) and save settings
	void testAndAccept();
	//! Rejects the dialog (if some conditions are met)
	void testAndReject();

	//! Save persistent settings and 'accept' dialog
	void saveSettings();

	//! Called when the active layer changes
	void activeLayerChanged(int, bool autoRedraw = true);

	//! Called when the projection direction changes
	void projectionDirChanged(int);

	//! Called when the projection type changes
	void projectionTypeChanged(int);

	//! Called when the 'resampled' option changes
	void resampleOptionToggled(bool);

	//! Called when the SF projection type changes
	void sfProjectionTypeChanged(int);

	//Inherited from cc2Point5DimEditor
	virtual bool showGridBoxEditor() override;

	//! Called when the empty cell filling strategy changes
	void fillEmptyCellStrategyChanged(int);

	//! Called when the an option of the grid generation has changed
	void gridOptionChanged();

	//! Updates the gid info
	void updateGridInfo();

	//! Update the grid and the 2D display
	void updateGridAndDisplay();

	//! Exports the grid as an image
	virtual void generateImage() const;

    //! Save project to DB
    void saveDone();
    void saveFailed();

    //! Save to DB in separate thread
    virtual void saveToDB();

	//! Exports the grid as an ASCII matrix
	virtual void generateASCIIMatrix() const;

protected: //standard methods

	//Inherited from cc2Point5DimEditor
	virtual double getGridStep() const override;
	virtual unsigned char getProjectionDimension() const override;
	virtual ccRasterGrid::ProjectionType getTypeOfProjection() const override;

	//! Returns user defined height for empty cells
	double getCustomHeightForEmptyCells() const;

	//! Returns strategy for empty cell filling (extended version)
	ccRasterGrid::EmptyCellFillOption getFillEmptyCellsStrategyExt(	double& emptyCellsHeight,
																	double& minHeight,
																	double& maxHeight) const;

	//! Returns whether a given field count should be exported as SF (only if a cloud is generated!)
	bool exportAsSF(ccRasterGrid::ExportableFields field) const;

	//! Returns whether the output cloud should use the original cloud or the grid as 'support'
	bool resampleOriginalCloud() const;

	//! Returns type of SF interpolation
	ccRasterGrid::ProjectionType getTypeOfSFInterpolation() const;

	//Inherited from cc2Point5DimEditor
	virtual void gridIsUpToDate(bool state) override;

	//! Load persistent settings
	void loadSettings();

	//! Updates the grid
	bool updateGrid(bool interpolateSF = false);

	//! Tests if the dialog can be safely closed
	bool canClose();

protected: //raster grid related stuff

	//! Converts the grid to a cloud with scalar field(s)
	ccPointCloud* convertGridToCloud(	const std::vector<ccRasterGrid::ExportableFields>& exportedFields,
										bool interpolateSF,
										bool interpolateColors,
										bool copyHillshadeSF,
										QString activeSFName,
										bool exportToOriginalCS) const;

protected: //members

	//! Layer types
	enum LayerType {	LAYER_HEIGHT = 0,
						LAYER_RGB = 1,
						LAYER_SF = 2
	};

	//! Associated cloud
	ccGenericPointCloud* m_cloud;

	//! Contour lines
    std::vector<ccPolyline*> m_contourLines;

};

class saveThread: public QThread
{
protected:
    ccGenericPointCloud* m_cloud;
    QString sql, project, imagefilename, db;

public:
    saveThread(ccGenericPointCloud *cloud, QString s, QString pro, QString img, QString d):m_cloud(cloud)
    , sql(s)
    , project(pro)
    , imagefilename(img)
    , db(d){}

private:
    Q_OBJECT

    void run(){
        QString sqlfilename, createtablesql, imagetablename, pointstablename, rdttablename;

        sqlfilename = imagefilename + ".sql";
        createtablesql = "create" + sqlfilename;

        imagetablename = project + "_image";
        pointstablename = project + "_xyz";
        rdttablename = project + "_rdt";

        std::ofstream createtable, sqlfile, rdtfile;
        createtable.open(("temp/" + createtablesql).toStdString().c_str());

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
                    << "END;\n"
                    << "BEGIN;\n"
                    << "CREATE TABLE IF NOT EXISTS " << rdttablename.toStdString() << "\n"
                    << "(\n"
                    << "\"rid\" integer REFERENCES " << imagetablename.toStdString() << "(rid) ON UPDATE CASCADE ON DELETE CASCADE,\n"
                    << "\"r\" double precision,\n"
                    << "\"depth\" double precision,\n"
                    << "\"theta\" double precision\n"
                    << ");\n"
                    << "END;\n"
                    << "BEGIN;\n"
                    << "GRANT ALL PRIVILEGES ON TABLE " + imagetablename.toStdString() + " TO GROUP " + db.toStdString() + "_project_admins WITH GRANT OPTION;\n"
                    << "GRANT ALL PRIVILEGES ON TABLE " + pointstablename.toStdString() + " TO GROUP " + db.toStdString() + "_project_admins WITH GRANT OPTION;\n"
                    << "GRANT ALL PRIVILEGES ON TABLE " + rdttablename.toStdString() + " TO GROUP " + db.toStdString() + "_project_admins WITH GRANT OPTION;\n"
                    << "END;\n";
        createtable.close();

        STARTUPINFO si;
        PROCESS_INFORMATION pi;
        ZeroMemory(&si, sizeof(si));
        si.cb = sizeof(si);
        ZeroMemory(&pi, sizeof(pi));

        QString command;
        command = sql + "temp\\" + createtablesql;
        wchar_t warray[250];
        wcsncpy(warray, command.toStdWString().c_str(), command.toStdWString().size());
        warray[command.toStdWString().size()] = '\0';

        //system((sql + "temp/" + createtablesql).toStdString().c_str());

        if(!CreateProcess(NULL, warray, NULL, NULL, FALSE, CREATE_NO_WINDOW, NULL, NULL, &si, &pi)){
            QMessageBox msgBox;
            msgBox.setText("Could not create process to save project.\n");
            msgBox.setWindowTitle("Save Operation failed.");
            msgBox.setIcon(msgBox.Critical);
            msgBox.exec();
            emit(savingFailed());
            return;
        }
        else{
            WaitForSingleObject(pi.hProcess, INFINITE);
        }

        remove(("temp/" + createtablesql).toStdString().c_str());

        command = "cmd /c raster2pgsql -a -I -M -F temp\\" + imagefilename + " " + imagetablename + " > " + "temp\\temp" + sqlfilename;
        //system((command).c_str());

        wcsncpy(warray, command.toStdWString().c_str(), command.toStdWString().size());
        warray[command.toStdWString().size()] = '\0';

        if(!CreateProcess(NULL, warray, NULL, NULL, FALSE, CREATE_NO_WINDOW, NULL, NULL, &si, &pi)){
            QMessageBox msgBox;
            msgBox.setText("Could not create process to save project.\n");
            msgBox.setWindowTitle("Save Operation failed.");
            msgBox.setIcon(msgBox.Critical);
            msgBox.exec();
            emit(savingFailed());
            return;
        }
        else{
            WaitForSingleObject(pi.hProcess, INFINITE);
        }

        std::ifstream rasterOutput;
        rasterOutput.open(("temp/temp" + sqlfilename).toStdString().c_str());

        string strcommand;

        sqlfile.open(("temp/" + sqlfilename).toStdString().c_str());
        getline(rasterOutput, strcommand);
        sqlfile << strcommand << endl;
        getline(rasterOutput, strcommand);
        strcommand = strcommand.substr(0, strcommand.size() - 1) + " RETURNING rid;";
        sqlfile << strcommand << endl;
        sqlfile << "END;\n";
        sqlfile.close();

        //system((sql + "temp/" + sqlfilename + " > temp/output" + sqlfilename).toStdString().c_str());

        command = sql + "temp\\" + sqlfilename + " > temp\\output" + sqlfilename;

        wcsncpy(warray, command.toStdWString().c_str(), command.toStdWString().size());
        warray[command.toStdWString().size()] = '\0';

        if(!CreateProcess(NULL, warray, NULL, NULL, FALSE, CREATE_NO_WINDOW, NULL, NULL, &si, &pi)){
            QMessageBox msgBox;
            msgBox.setText("Could not create process to save project.\n");
            msgBox.setWindowTitle("Save Operation failed.");
            msgBox.setIcon(msgBox.Critical);
            msgBox.exec();
            emit(savingFailed());
            return;
        }
        else{
            WaitForSingleObject(pi.hProcess, INFINITE);
        }

        sqlfile.open(("temp/" + sqlfilename).toStdString().c_str());
        sqlfile << "BEGIN;\n";
        getline(rasterOutput, strcommand);
        sqlfile << strcommand << endl;
        getline(rasterOutput, strcommand);
        sqlfile << strcommand << endl;
        getline(rasterOutput, strcommand);
        sqlfile << strcommand << endl;
        getline(rasterOutput, strcommand);
        sqlfile << strcommand << endl;
        getline(rasterOutput, strcommand);
        sqlfile << strcommand << endl;
        sqlfile << "\n";
        rasterOutput.close();
        remove(("temp/temp" + sqlfilename).toStdString().c_str());
        remove(("temp/" + imagefilename).toStdString().c_str());

        int i = m_cloud->getIndex(), rid;
        double r, depth, theta, x, y, z;
        rasterOutput.open(("temp/output" + sqlfilename).toStdString().c_str());
        rdtfile.open(("temp/rdt" + sqlfilename).toStdString().c_str());
        getline(rasterOutput, strcommand);
        getline(rasterOutput, strcommand);
        getline(rasterOutput, strcommand);
        rasterOutput >> rid;
        rasterOutput.close();
        remove(("temp/output" + sqlfilename).toStdString().c_str());
        sqlfile << "\n\n";
        sqlfile << "COPY " << pointstablename.toStdString() << " (rid, x, y, z) FROM stdin;\n";
        rdtfile << "COPY " <<   rdttablename.toStdString() << " (rid, r, depth, theta) FROM stdin;\n";
        for(; i < m_cloud->size(); i++){
            x = m_cloud->getPoint(i)->x;
            y = m_cloud->getPoint(i)->y;
            z = m_cloud->getPoint(i)->z;
            sqlfile << rid << "\t" << x << "\t" << y << "\t" << z << "\n";
            r = sqrt(x * x + y * y + z * z);
            theta = atan2(y, x);
            depth = acos(z / r);
            rdtfile << rid << "\t" << r << "\t" << depth << "\t" << theta << "\n";
        }
        sqlfile << "\\.\n";
        rdtfile << "\\.\n";
        sqlfile << "VACUUM ANALYZE \"" << pointstablename.toStdString() << "\";\n";
        rdtfile << "VACUUM ANALYZE \"" << rdttablename.toStdString() << "\";\n";
        sqlfile.close();
        rdtfile.close();

        //system((sql + "temp/" + sqlfilename).toStdString().c_str());
        //system((sql + "temp/rdt" + sqlfilename).toStdString().c_str());

        command = sql + "temp\\" + sqlfilename;
        wcsncpy(warray, command.toStdWString().c_str(), command.toStdWString().size());
        warray[command.toStdWString().size()] = '\0';

        if(!CreateProcess(NULL, warray, NULL, NULL, FALSE, CREATE_NO_WINDOW, NULL, NULL, &si, &pi)){
            QMessageBox msgBox;
            msgBox.setText("Could not create process to save project.\n");
            msgBox.setWindowTitle("Save Operation failed.");
            msgBox.setIcon(msgBox.Critical);
            msgBox.exec();
            emit(savingFailed());
            return;
        }
        else{
            WaitForSingleObject(pi.hProcess, INFINITE);
        }

        command = sql + "temp\\rdt" + sqlfilename;
        wcsncpy(warray, command.toStdWString().c_str(), command.toStdWString().size());
        warray[command.toStdWString().size()] = '\0';

        if(!CreateProcess(NULL, warray, NULL, NULL, FALSE, CREATE_NO_WINDOW, NULL, NULL, &si, &pi)){
            QMessageBox msgBox;
            msgBox.setText("Could not create process to save project.\n");
            msgBox.setWindowTitle("Save Operation failed.");
            msgBox.setIcon(msgBox.Critical);
            msgBox.exec();
            emit(savingFailed());
            return;
        }
        else{
            WaitForSingleObject(pi.hProcess, INFINITE);
        }

        remove(("temp/output" + sqlfilename).toStdString().c_str());
        remove(("temp/" + sqlfilename).toStdString().c_str());
        remove(("temp/rdt" + sqlfilename).toStdString().c_str());
        emit savingDone();
    }

signals:
    void savingDone();
    void savingFailed();
};


#endif //CC_RASTERIZE_TOOL_HEADER
