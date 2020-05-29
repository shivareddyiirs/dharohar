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

#ifndef CC_MESH_GROUP_HEADER
#define CC_MESH_GROUP_HEADER

//Local
#include "ccGenericMesh.h"

//! [DEPRECATED] A group of meshes sharing vertices (and associated properties) in a unique cloud
/** This is an empty shell for backward compatibility.
	Shouldn't be used anymore. 
**/
class QCC_DB_LIB_API ccMeshGroup : public ccGenericMesh
{
public:

	//! Default constructor
	ccMeshGroup() : ccGenericMesh("[Deprecated] Mesh Group") {}

	//! Returns class ID
	virtual CC_CLASS_ENUM getClassID() const override { return CC_TYPES::MESH_GROUP; }

	//inherited methods (ccGenericMesh)
	virtual ccGenericPointCloud* getAssociatedCloud() const override { return 0; }
	virtual void refreshBB() override {}
    virtual bool interpolateNormals(unsigned , const CCVector3& , CCVector3& ) override { return false; }
    virtual bool interpolateColors(unsigned , const CCVector3& , ccColor::Rgb& ) override { return false; }
    virtual bool getColorFromMaterial(unsigned , const CCVector3& , ccColor::Rgb& , bool ) override { return false; }
    virtual bool getVertexColorFromMaterial(unsigned , unsigned char , ccColor::Rgb& , bool ) override { return false; }
	virtual bool hasMaterials() const override { return false; }
	virtual const ccMaterialSet* getMaterialSet() const override { return 0; }
    virtual int getTriangleMtlIndex(unsigned ) const override { return -1; }
	virtual bool hasTextures() const override { return false; }
	virtual TextureCoordsContainer* getTexCoordinatesTable() const override { return 0; }
    virtual void getTriangleTexCoordinates(unsigned , float* &tx1, float* &tx2, float* &tx3) const override { tx1 = tx2 = tx3 = 0; }
	virtual bool hasPerTriangleTexCoordIndexes() const override { return false; }
    virtual void getTriangleTexCoordinatesIndexes(unsigned , int& i1, int& i2, int& i3) const override { i1 = i2 = i3 = -1; }
	virtual bool hasTriNormals() const override { return false; }
    virtual void getTriangleNormalIndexes(unsigned , int& i1, int& i2, int& i3) const override { i1 = i2 = i3 = -1; }
    virtual bool getTriangleNormals(unsigned , CCVector3& , CCVector3& , CCVector3& ) const override { return false; }
	virtual NormsIndexesTableType* getTriNormsTable() const override { return 0; }
	virtual unsigned capacity() const override { return 0; }
    virtual bool trianglePicking(const CCVector2d& , const ccGLCameraParameters& , int& , double& , CCVector3d& ) override { return false; }

	//inherited methods (ccHObject)
	virtual bool isSerializable() const override { return true; }
	virtual bool toFile_MeOnly(QFile& out) const override;
	virtual bool fromFile_MeOnly(QFile& in, short dataVersion, int flags) override;

	//inherited methods (GenericIndexedMesh)
	virtual unsigned size() const override { return 0; }
    virtual void forEach(genericTriangleAction& ) override {}
	virtual void placeIteratorAtBegining() override {}
	virtual CCLib::GenericTriangle* _getNextTriangle() override { return 0; }
    virtual CCLib::GenericTriangle* _getTriangle(unsigned ) override { return 0; }
	virtual CCLib::VerticesIndexes* getNextTriangleVertIndexes() override { return 0; }
    virtual CCLib::VerticesIndexes* getTriangleVertIndexes(unsigned ) override { return 0; }
    virtual void getTriangleVertices(unsigned , CCVector3& , CCVector3& , CCVector3& ) override {}
    virtual void getBoundingBox(CCVector3& , CCVector3& ) override {}

protected:

	//inherited from ccHObject
	virtual void drawMeOnly(CC_DRAW_CONTEXT& context) override;
};

#endif //CC_MESH_GROUP_HEADER
