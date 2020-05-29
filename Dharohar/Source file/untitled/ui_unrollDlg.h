/********************************************************************************
** Form generated from reading UI file 'unrollDlg.ui'
**
** Created by: Qt User Interface Compiler version 5.6.1
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_UNROLLDLG_H
#define UI_UNROLLDLG_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QButtonGroup>
#include <QtWidgets/QCheckBox>
#include <QtWidgets/QComboBox>
#include <QtWidgets/QDialog>
#include <QtWidgets/QDialogButtonBox>
#include <QtWidgets/QDoubleSpinBox>
#include <QtWidgets/QFrame>
#include <QtWidgets/QGroupBox>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QLabel>
#include <QtWidgets/QSpacerItem>
#include <QtWidgets/QVBoxLayout>

QT_BEGIN_NAMESPACE

class Ui_UnrollDialog
{
public:
    QVBoxLayout *vboxLayout;
    QHBoxLayout *hboxLayout;
    QLabel *label_3;
    QComboBox *comboBoxUnrollShapeType;
    QSpacerItem *spacerItem;
    QHBoxLayout *hboxLayout1;
    QLabel *label;
    QComboBox *comboBoxAxisDimension;
    QFrame *angleFrame;
    QHBoxLayout *horizontalLayout;
    QSpacerItem *horizontalSpacer;
    QLabel *labelAngle;
    QDoubleSpinBox *angleDoubleSpinBox;
    QFrame *radiusFrame;
    QHBoxLayout *horizontalLayout_2;
    QSpacerItem *horizontalSpacer_2;
    QLabel *radiusLabel;
    QDoubleSpinBox *radiusDoubleSpinBox;
    QGroupBox *groupBoxAxisPosition;
    QVBoxLayout *vboxLayout1;
    QFrame *axisFrame;
    QHBoxLayout *hboxLayout2;
    QLabel *label1;
    QDoubleSpinBox *doubleSpinBoxAxisX;
    QSpacerItem *spacerItem1;
    QLabel *label2;
    QDoubleSpinBox *doubleSpinBoxAxisY;
    QSpacerItem *spacerItem2;
    QLabel *label3;
    QDoubleSpinBox *doubleSpinBoxAxisZ;
    QFrame *autoCenterFrame;
    QHBoxLayout *hboxLayout3;
    QCheckBox *checkBoxAuto;
    QSpacerItem *spacerItem3;
    QCheckBox *exportDeviationSFCheckBox;
    QSpacerItem *verticalSpacer;
    QDialogButtonBox *buttonBox;

    void setupUi(QDialog *UnrollDialog)
    {
        if (UnrollDialog->objectName().isEmpty())
            UnrollDialog->setObjectName(QStringLiteral("UnrollDialog"));
        UnrollDialog->resize(500, 220);
        vboxLayout = new QVBoxLayout(UnrollDialog);
        vboxLayout->setObjectName(QStringLiteral("vboxLayout"));
        hboxLayout = new QHBoxLayout();
        hboxLayout->setObjectName(QStringLiteral("hboxLayout"));
        label_3 = new QLabel(UnrollDialog);
        label_3->setObjectName(QStringLiteral("label_3"));

        hboxLayout->addWidget(label_3);

        comboBoxUnrollShapeType = new QComboBox(UnrollDialog);
        comboBoxUnrollShapeType->setObjectName(QStringLiteral("comboBoxUnrollShapeType"));

        hboxLayout->addWidget(comboBoxUnrollShapeType);

        spacerItem = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        hboxLayout->addItem(spacerItem);


        vboxLayout->addLayout(hboxLayout);

        hboxLayout1 = new QHBoxLayout();
        hboxLayout1->setObjectName(QStringLiteral("hboxLayout1"));
        label = new QLabel(UnrollDialog);
        label->setObjectName(QStringLiteral("label"));
        label->setScaledContents(false);
        label->setAlignment(Qt::AlignLeading|Qt::AlignLeft|Qt::AlignVCenter);

        hboxLayout1->addWidget(label);

        comboBoxAxisDimension = new QComboBox(UnrollDialog);
        comboBoxAxisDimension->setObjectName(QStringLiteral("comboBoxAxisDimension"));

        hboxLayout1->addWidget(comboBoxAxisDimension);

        angleFrame = new QFrame(UnrollDialog);
        angleFrame->setObjectName(QStringLiteral("angleFrame"));
        angleFrame->setFrameShape(QFrame::StyledPanel);
        angleFrame->setFrameShadow(QFrame::Raised);
        horizontalLayout = new QHBoxLayout(angleFrame);
        horizontalLayout->setContentsMargins(0, 0, 0, 0);
        horizontalLayout->setObjectName(QStringLiteral("horizontalLayout"));
        horizontalSpacer = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout->addItem(horizontalSpacer);

        labelAngle = new QLabel(angleFrame);
        labelAngle->setObjectName(QStringLiteral("labelAngle"));

        horizontalLayout->addWidget(labelAngle);

        angleDoubleSpinBox = new QDoubleSpinBox(angleFrame);
        angleDoubleSpinBox->setObjectName(QStringLiteral("angleDoubleSpinBox"));
        angleDoubleSpinBox->setDecimals(2);
        angleDoubleSpinBox->setMaximum(180);
        angleDoubleSpinBox->setValue(15);

        horizontalLayout->addWidget(angleDoubleSpinBox);


        hboxLayout1->addWidget(angleFrame);

        radiusFrame = new QFrame(UnrollDialog);
        radiusFrame->setObjectName(QStringLiteral("radiusFrame"));
        horizontalLayout_2 = new QHBoxLayout(radiusFrame);
        horizontalLayout_2->setContentsMargins(0, 0, 0, 0);
        horizontalLayout_2->setObjectName(QStringLiteral("horizontalLayout_2"));
        horizontalSpacer_2 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_2->addItem(horizontalSpacer_2);

        radiusLabel = new QLabel(radiusFrame);
        radiusLabel->setObjectName(QStringLiteral("radiusLabel"));
        radiusLabel->setAlignment(Qt::AlignLeading|Qt::AlignLeft|Qt::AlignVCenter);

        horizontalLayout_2->addWidget(radiusLabel);

        radiusDoubleSpinBox = new QDoubleSpinBox(radiusFrame);
        radiusDoubleSpinBox->setObjectName(QStringLiteral("radiusDoubleSpinBox"));
        radiusDoubleSpinBox->setDecimals(6);
        radiusDoubleSpinBox->setMaximum(1e+09);
        radiusDoubleSpinBox->setValue(100);

        horizontalLayout_2->addWidget(radiusDoubleSpinBox);


        hboxLayout1->addWidget(radiusFrame);


        vboxLayout->addLayout(hboxLayout1);

        groupBoxAxisPosition = new QGroupBox(UnrollDialog);
        groupBoxAxisPosition->setObjectName(QStringLiteral("groupBoxAxisPosition"));
        vboxLayout1 = new QVBoxLayout(groupBoxAxisPosition);
        vboxLayout1->setObjectName(QStringLiteral("vboxLayout1"));
        axisFrame = new QFrame(groupBoxAxisPosition);
        axisFrame->setObjectName(QStringLiteral("axisFrame"));
        hboxLayout2 = new QHBoxLayout(axisFrame);
        hboxLayout2->setContentsMargins(0, 0, 0, 0);
        hboxLayout2->setObjectName(QStringLiteral("hboxLayout2"));
        label1 = new QLabel(axisFrame);
        label1->setObjectName(QStringLiteral("label1"));
        label1->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);

        hboxLayout2->addWidget(label1);

        doubleSpinBoxAxisX = new QDoubleSpinBox(axisFrame);
        doubleSpinBoxAxisX->setObjectName(QStringLiteral("doubleSpinBoxAxisX"));
        doubleSpinBoxAxisX->setEnabled(true);
        doubleSpinBoxAxisX->setDecimals(6);
        doubleSpinBoxAxisX->setMinimum(-1e+09);
        doubleSpinBoxAxisX->setMaximum(1e+09);

        hboxLayout2->addWidget(doubleSpinBoxAxisX);

        spacerItem1 = new QSpacerItem(10, 20, QSizePolicy::Fixed, QSizePolicy::Minimum);

        hboxLayout2->addItem(spacerItem1);

        label2 = new QLabel(axisFrame);
        label2->setObjectName(QStringLiteral("label2"));
        label2->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);

        hboxLayout2->addWidget(label2);

        doubleSpinBoxAxisY = new QDoubleSpinBox(axisFrame);
        doubleSpinBoxAxisY->setObjectName(QStringLiteral("doubleSpinBoxAxisY"));
        doubleSpinBoxAxisY->setEnabled(true);
        doubleSpinBoxAxisY->setDecimals(6);
        doubleSpinBoxAxisY->setMinimum(-1e+09);
        doubleSpinBoxAxisY->setMaximum(1e+09);

        hboxLayout2->addWidget(doubleSpinBoxAxisY);

        spacerItem2 = new QSpacerItem(10, 20, QSizePolicy::Fixed, QSizePolicy::Minimum);

        hboxLayout2->addItem(spacerItem2);

        label3 = new QLabel(axisFrame);
        label3->setObjectName(QStringLiteral("label3"));
        label3->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);

        hboxLayout2->addWidget(label3);

        doubleSpinBoxAxisZ = new QDoubleSpinBox(axisFrame);
        doubleSpinBoxAxisZ->setObjectName(QStringLiteral("doubleSpinBoxAxisZ"));
        doubleSpinBoxAxisZ->setEnabled(true);
        doubleSpinBoxAxisZ->setDecimals(6);
        doubleSpinBoxAxisZ->setMinimum(-1e+09);
        doubleSpinBoxAxisZ->setMaximum(1e+09);

        hboxLayout2->addWidget(doubleSpinBoxAxisZ);


        vboxLayout1->addWidget(axisFrame);

        autoCenterFrame = new QFrame(groupBoxAxisPosition);
        autoCenterFrame->setObjectName(QStringLiteral("autoCenterFrame"));
        hboxLayout3 = new QHBoxLayout(autoCenterFrame);
        hboxLayout3->setContentsMargins(0, 0, 0, 0);
        hboxLayout3->setObjectName(QStringLiteral("hboxLayout3"));
        checkBoxAuto = new QCheckBox(autoCenterFrame);
        checkBoxAuto->setObjectName(QStringLiteral("checkBoxAuto"));
        checkBoxAuto->setEnabled(true);
        checkBoxAuto->setChecked(false);

        hboxLayout3->addWidget(checkBoxAuto);

        spacerItem3 = new QSpacerItem(71, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        hboxLayout3->addItem(spacerItem3);


        vboxLayout1->addWidget(autoCenterFrame);


        vboxLayout->addWidget(groupBoxAxisPosition);

        exportDeviationSFCheckBox = new QCheckBox(UnrollDialog);
        exportDeviationSFCheckBox->setObjectName(QStringLiteral("exportDeviationSFCheckBox"));

        vboxLayout->addWidget(exportDeviationSFCheckBox);

        verticalSpacer = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);

        vboxLayout->addItem(verticalSpacer);

        buttonBox = new QDialogButtonBox(UnrollDialog);
        buttonBox->setObjectName(QStringLiteral("buttonBox"));
        buttonBox->setOrientation(Qt::Horizontal);
        buttonBox->setStandardButtons(QDialogButtonBox::Cancel|QDialogButtonBox::Ok);

        vboxLayout->addWidget(buttonBox);


        retranslateUi(UnrollDialog);
        QObject::connect(buttonBox, SIGNAL(accepted()), UnrollDialog, SLOT(accept()));
        QObject::connect(buttonBox, SIGNAL(rejected()), UnrollDialog, SLOT(reject()));

        comboBoxAxisDimension->setCurrentIndex(2);


        QMetaObject::connectSlotsByName(UnrollDialog);
    } // setupUi

    void retranslateUi(QDialog *UnrollDialog)
    {
        UnrollDialog->setWindowTitle(QApplication::translate("UnrollDialog", "Unroll", 0));
        label_3->setText(QApplication::translate("UnrollDialog", "Type", 0));
        comboBoxUnrollShapeType->clear();
        comboBoxUnrollShapeType->insertItems(0, QStringList()
         << QApplication::translate("UnrollDialog", "Cylinder", 0)
         << QApplication::translate("UnrollDialog", "Cone", 0)
         << QApplication::translate("UnrollDialog", "Straightened cone", 0)
        );
        label->setText(QApplication::translate("UnrollDialog", "Axis", 0));
        comboBoxAxisDimension->clear();
        comboBoxAxisDimension->insertItems(0, QStringList()
         << QApplication::translate("UnrollDialog", "X", 0)
         << QApplication::translate("UnrollDialog", "Y", 0)
         << QApplication::translate("UnrollDialog", "Z", 0)
        );
#ifndef QT_NO_TOOLTIP
        labelAngle->setToolTip(QApplication::translate("UnrollDialog", "Cone angle (0-180\302\260)", 0));
#endif // QT_NO_TOOLTIP
        labelAngle->setText(QApplication::translate("UnrollDialog", "Half angle (degrees)", 0));
#ifndef QT_NO_TOOLTIP
        angleDoubleSpinBox->setToolTip(QApplication::translate("UnrollDialog", "Cone angle (0-180\302\260)", 0));
#endif // QT_NO_TOOLTIP
#ifndef QT_NO_STATUSTIP
        angleDoubleSpinBox->setStatusTip(QString());
#endif // QT_NO_STATUSTIP
#ifndef QT_NO_TOOLTIP
        radiusLabel->setToolTip(QApplication::translate("UnrollDialog", "Cylinder (or cone base) radius", 0));
#endif // QT_NO_TOOLTIP
        radiusLabel->setText(QApplication::translate("UnrollDialog", "Radius", 0));
#ifndef QT_NO_TOOLTIP
        radiusDoubleSpinBox->setToolTip(QApplication::translate("UnrollDialog", "Cylinder (or cone base) radius", 0));
#endif // QT_NO_TOOLTIP
        groupBoxAxisPosition->setTitle(QApplication::translate("UnrollDialog", "Axis position", 0));
        label1->setText(QApplication::translate("UnrollDialog", "X", 0));
        label2->setText(QApplication::translate("UnrollDialog", "Y", 0));
        label3->setText(QApplication::translate("UnrollDialog", "Z", 0));
        checkBoxAuto->setText(QApplication::translate("UnrollDialog", "Auto (gravity center)", 0));
#ifndef QT_NO_TOOLTIP
        exportDeviationSFCheckBox->setToolTip(QApplication::translate("UnrollDialog", "Deviation from the theoretical shape (i.e. cone or cylinder)", 0));
#endif // QT_NO_TOOLTIP
        exportDeviationSFCheckBox->setText(QApplication::translate("UnrollDialog", "Export deviation scalar field", 0));
    } // retranslateUi

};

namespace Ui {
    class UnrollDialog: public Ui_UnrollDialog {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_UNROLLDLG_H
