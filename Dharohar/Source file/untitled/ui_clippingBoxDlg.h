/********************************************************************************
** Form generated from reading UI file 'clippingBoxDlg.ui'
**
** Created by: Qt User Interface Compiler version 5.6.1
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_CLIPPINGBOXDLG_H
#define UI_CLIPPINGBOXDLG_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QButtonGroup>
#include <QtWidgets/QDialog>
#include <QtWidgets/QDoubleSpinBox>
#include <QtWidgets/QFormLayout>
#include <QtWidgets/QFrame>
#include <QtWidgets/QGroupBox>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QLabel>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QSpacerItem>
#include <QtWidgets/QToolButton>
#include <QtWidgets/QVBoxLayout>

QT_BEGIN_NAMESPACE

class Ui_ClippingBoxDlg
{
public:
    QVBoxLayout *verticalLayout;
    QHBoxLayout *horizontalLayout_2;
    QToolButton *showBoxToolButton;
    QToolButton *showInteractorsToolButton;
    QSpacerItem *horizontalSpacer_9;
    QToolButton *resetButton;
    QToolButton *closeButton;
    QGroupBox *thicknessGroupBox;
    QFormLayout *formLayout;
    QLabel *label_2;
    QDoubleSpinBox *thickXDoubleSpinBox;
    QLabel *label_3;
    QDoubleSpinBox *thickYDoubleSpinBox;
    QLabel *label_4;
    QDoubleSpinBox *thickZDoubleSpinBox;
    QHBoxLayout *horizontalLayout_6;
    QHBoxLayout *horizontalLayout_3;
    QPushButton *exportButton;
    QFrame *viewButtonsFrame;
    QHBoxLayout *horizontalLayout_8;
    QGroupBox *groupBox;
    QHBoxLayout *horizontalLayout_4;
    QSpacerItem *horizontalSpacer_2;
    QToolButton *minusXShiftToolButton;
    QToolButton *plusXShiftToolButton;
    QToolButton *minusYShiftToolButton;
    QToolButton *plusYShiftToolButton;
    QToolButton *minusZShiftToolButton;
    QToolButton *plusZShiftToolButton;
    QSpacerItem *horizontalSpacer_3;

    void setupUi(QDialog *ClippingBoxDlg)
    {
        if (ClippingBoxDlg->objectName().isEmpty())
            ClippingBoxDlg->setObjectName(QStringLiteral("ClippingBoxDlg"));
        ClippingBoxDlg->resize(220, 322);
        QSizePolicy sizePolicy(QSizePolicy::Maximum, QSizePolicy::Maximum);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(ClippingBoxDlg->sizePolicy().hasHeightForWidth());
        ClippingBoxDlg->setSizePolicy(sizePolicy);
        verticalLayout = new QVBoxLayout(ClippingBoxDlg);
        verticalLayout->setObjectName(QStringLiteral("verticalLayout"));
        horizontalLayout_2 = new QHBoxLayout();
        horizontalLayout_2->setObjectName(QStringLiteral("horizontalLayout_2"));
        showBoxToolButton = new QToolButton(ClippingBoxDlg);
        showBoxToolButton->setObjectName(QStringLiteral("showBoxToolButton"));
        QIcon icon;
        icon.addFile(QStringLiteral(":/CC/images/square.png"), QSize(), QIcon::Normal, QIcon::Off);
        showBoxToolButton->setIcon(icon);
        showBoxToolButton->setCheckable(true);
        showBoxToolButton->setChecked(true);
        showBoxToolButton->setAutoRaise(true);

        horizontalLayout_2->addWidget(showBoxToolButton);

        showInteractorsToolButton = new QToolButton(ClippingBoxDlg);
        showInteractorsToolButton->setObjectName(QStringLiteral("showInteractorsToolButton"));
        QIcon icon1;
        icon1.addFile(QStringLiteral(":/CC/images/interactors.png"), QSize(), QIcon::Normal, QIcon::Off);
        showInteractorsToolButton->setIcon(icon1);
        showInteractorsToolButton->setCheckable(true);
        showInteractorsToolButton->setChecked(true);
        showInteractorsToolButton->setAutoRaise(true);

        horizontalLayout_2->addWidget(showInteractorsToolButton);

        horizontalSpacer_9 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_2->addItem(horizontalSpacer_9);

        resetButton = new QToolButton(ClippingBoxDlg);
        resetButton->setObjectName(QStringLiteral("resetButton"));
        resetButton->setMinimumSize(QSize(25, 25));
        QIcon icon2;
        icon2.addFile(QStringLiteral(":/CC/images/smallReset.png"), QSize(), QIcon::Normal, QIcon::Off);
        resetButton->setIcon(icon2);

        horizontalLayout_2->addWidget(resetButton);

        closeButton = new QToolButton(ClippingBoxDlg);
        closeButton->setObjectName(QStringLiteral("closeButton"));
        closeButton->setMinimumSize(QSize(25, 25));
        QIcon icon3;
        icon3.addFile(QStringLiteral(":/CC/images/smallCancel.png"), QSize(), QIcon::Normal, QIcon::Off);
        closeButton->setIcon(icon3);

        horizontalLayout_2->addWidget(closeButton);


        verticalLayout->addLayout(horizontalLayout_2);

        thicknessGroupBox = new QGroupBox(ClippingBoxDlg);
        thicknessGroupBox->setObjectName(QStringLiteral("thicknessGroupBox"));
        QSizePolicy sizePolicy1(QSizePolicy::Preferred, QSizePolicy::Maximum);
        sizePolicy1.setHorizontalStretch(0);
        sizePolicy1.setVerticalStretch(0);
        sizePolicy1.setHeightForWidth(thicknessGroupBox->sizePolicy().hasHeightForWidth());
        thicknessGroupBox->setSizePolicy(sizePolicy1);
        formLayout = new QFormLayout(thicknessGroupBox);
        formLayout->setObjectName(QStringLiteral("formLayout"));
        label_2 = new QLabel(thicknessGroupBox);
        label_2->setObjectName(QStringLiteral("label_2"));

        formLayout->setWidget(0, QFormLayout::LabelRole, label_2);

        thickXDoubleSpinBox = new QDoubleSpinBox(thicknessGroupBox);
        thickXDoubleSpinBox->setObjectName(QStringLiteral("thickXDoubleSpinBox"));
        thickXDoubleSpinBox->setDecimals(8);
        thickXDoubleSpinBox->setMaximum(1e+09);

        formLayout->setWidget(0, QFormLayout::FieldRole, thickXDoubleSpinBox);

        label_3 = new QLabel(thicknessGroupBox);
        label_3->setObjectName(QStringLiteral("label_3"));

        formLayout->setWidget(1, QFormLayout::LabelRole, label_3);

        thickYDoubleSpinBox = new QDoubleSpinBox(thicknessGroupBox);
        thickYDoubleSpinBox->setObjectName(QStringLiteral("thickYDoubleSpinBox"));
        thickYDoubleSpinBox->setDecimals(8);
        thickYDoubleSpinBox->setMaximum(1e+09);

        formLayout->setWidget(1, QFormLayout::FieldRole, thickYDoubleSpinBox);

        label_4 = new QLabel(thicknessGroupBox);
        label_4->setObjectName(QStringLiteral("label_4"));

        formLayout->setWidget(2, QFormLayout::LabelRole, label_4);

        thickZDoubleSpinBox = new QDoubleSpinBox(thicknessGroupBox);
        thickZDoubleSpinBox->setObjectName(QStringLiteral("thickZDoubleSpinBox"));
        thickZDoubleSpinBox->setDecimals(8);
        thickZDoubleSpinBox->setMaximum(1e+09);

        formLayout->setWidget(2, QFormLayout::FieldRole, thickZDoubleSpinBox);

        horizontalLayout_6 = new QHBoxLayout();
        horizontalLayout_6->setObjectName(QStringLiteral("horizontalLayout_6"));

        formLayout->setLayout(3, QFormLayout::SpanningRole, horizontalLayout_6);


        verticalLayout->addWidget(thicknessGroupBox);

        horizontalLayout_3 = new QHBoxLayout();
        horizontalLayout_3->setObjectName(QStringLiteral("horizontalLayout_3"));
        exportButton = new QPushButton(ClippingBoxDlg);
        exportButton->setObjectName(QStringLiteral("exportButton"));

        horizontalLayout_3->addWidget(exportButton);


        verticalLayout->addLayout(horizontalLayout_3);

        viewButtonsFrame = new QFrame(ClippingBoxDlg);
        viewButtonsFrame->setObjectName(QStringLiteral("viewButtonsFrame"));
        sizePolicy1.setHeightForWidth(viewButtonsFrame->sizePolicy().hasHeightForWidth());
        viewButtonsFrame->setSizePolicy(sizePolicy1);
        viewButtonsFrame->setFrameShape(QFrame::NoFrame);
        horizontalLayout_8 = new QHBoxLayout(viewButtonsFrame);
        horizontalLayout_8->setObjectName(QStringLiteral("horizontalLayout_8"));
        horizontalLayout_8->setContentsMargins(0, 0, 0, 0);

        verticalLayout->addWidget(viewButtonsFrame);

        groupBox = new QGroupBox(ClippingBoxDlg);
        groupBox->setObjectName(QStringLiteral("groupBox"));
        sizePolicy1.setHeightForWidth(groupBox->sizePolicy().hasHeightForWidth());
        groupBox->setSizePolicy(sizePolicy1);
        horizontalLayout_4 = new QHBoxLayout(groupBox);
        horizontalLayout_4->setObjectName(QStringLiteral("horizontalLayout_4"));
        horizontalLayout_4->setContentsMargins(4, 4, 4, 4);
        horizontalSpacer_2 = new QSpacerItem(1, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_4->addItem(horizontalSpacer_2);

        minusXShiftToolButton = new QToolButton(groupBox);
        minusXShiftToolButton->setObjectName(QStringLiteral("minusXShiftToolButton"));
        sizePolicy.setHeightForWidth(minusXShiftToolButton->sizePolicy().hasHeightForWidth());
        minusXShiftToolButton->setSizePolicy(sizePolicy);
        minusXShiftToolButton->setMinimumSize(QSize(25, 25));

        horizontalLayout_4->addWidget(minusXShiftToolButton);

        plusXShiftToolButton = new QToolButton(groupBox);
        plusXShiftToolButton->setObjectName(QStringLiteral("plusXShiftToolButton"));
        sizePolicy.setHeightForWidth(plusXShiftToolButton->sizePolicy().hasHeightForWidth());
        plusXShiftToolButton->setSizePolicy(sizePolicy);
        plusXShiftToolButton->setMinimumSize(QSize(25, 25));

        horizontalLayout_4->addWidget(plusXShiftToolButton);

        minusYShiftToolButton = new QToolButton(groupBox);
        minusYShiftToolButton->setObjectName(QStringLiteral("minusYShiftToolButton"));
        sizePolicy.setHeightForWidth(minusYShiftToolButton->sizePolicy().hasHeightForWidth());
        minusYShiftToolButton->setSizePolicy(sizePolicy);
        minusYShiftToolButton->setMinimumSize(QSize(25, 25));

        horizontalLayout_4->addWidget(minusYShiftToolButton);

        plusYShiftToolButton = new QToolButton(groupBox);
        plusYShiftToolButton->setObjectName(QStringLiteral("plusYShiftToolButton"));
        sizePolicy.setHeightForWidth(plusYShiftToolButton->sizePolicy().hasHeightForWidth());
        plusYShiftToolButton->setSizePolicy(sizePolicy);
        plusYShiftToolButton->setMinimumSize(QSize(25, 25));

        horizontalLayout_4->addWidget(plusYShiftToolButton);

        minusZShiftToolButton = new QToolButton(groupBox);
        minusZShiftToolButton->setObjectName(QStringLiteral("minusZShiftToolButton"));
        sizePolicy.setHeightForWidth(minusZShiftToolButton->sizePolicy().hasHeightForWidth());
        minusZShiftToolButton->setSizePolicy(sizePolicy);
        minusZShiftToolButton->setMinimumSize(QSize(25, 25));

        horizontalLayout_4->addWidget(minusZShiftToolButton);

        plusZShiftToolButton = new QToolButton(groupBox);
        plusZShiftToolButton->setObjectName(QStringLiteral("plusZShiftToolButton"));
        sizePolicy.setHeightForWidth(plusZShiftToolButton->sizePolicy().hasHeightForWidth());
        plusZShiftToolButton->setSizePolicy(sizePolicy);
        plusZShiftToolButton->setMinimumSize(QSize(25, 25));

        horizontalLayout_4->addWidget(plusZShiftToolButton);

        horizontalSpacer_3 = new QSpacerItem(0, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_4->addItem(horizontalSpacer_3);


        verticalLayout->addWidget(groupBox);


        retranslateUi(ClippingBoxDlg);

        QMetaObject::connectSlotsByName(ClippingBoxDlg);
    } // setupUi

    void retranslateUi(QDialog *ClippingBoxDlg)
    {
        ClippingBoxDlg->setWindowTitle(QApplication::translate("ClippingBoxDlg", "Clipping Box", 0));
#ifndef QT_NO_TOOLTIP
        showBoxToolButton->setToolTip(QApplication::translate("ClippingBoxDlg", "Show/hide bounding box", 0));
#endif // QT_NO_TOOLTIP
#ifndef QT_NO_TOOLTIP
        showInteractorsToolButton->setToolTip(QApplication::translate("ClippingBoxDlg", "Show/hide interactors", 0));
#endif // QT_NO_TOOLTIP
#ifndef QT_NO_TOOLTIP
        resetButton->setToolTip(QApplication::translate("ClippingBoxDlg", "Reset", 0));
#endif // QT_NO_TOOLTIP
#ifndef QT_NO_STATUSTIP
        resetButton->setStatusTip(QApplication::translate("ClippingBoxDlg", "Reset", 0));
#endif // QT_NO_STATUSTIP
#ifndef QT_NO_TOOLTIP
        closeButton->setToolTip(QApplication::translate("ClippingBoxDlg", "Close", 0));
#endif // QT_NO_TOOLTIP
#ifndef QT_NO_STATUSTIP
        closeButton->setStatusTip(QApplication::translate("ClippingBoxDlg", "Close", 0));
#endif // QT_NO_STATUSTIP
        thicknessGroupBox->setTitle(QApplication::translate("ClippingBoxDlg", "Box thickness", 0));
        label_2->setText(QApplication::translate("ClippingBoxDlg", "X", 0));
        label_3->setText(QApplication::translate("ClippingBoxDlg", "Y", 0));
        label_4->setText(QApplication::translate("ClippingBoxDlg", "Z", 0));
        exportButton->setText(QApplication::translate("ClippingBoxDlg", "Export Cropped Cloud", 0));
        groupBox->setTitle(QApplication::translate("ClippingBoxDlg", "Shift box", 0));
#ifndef QT_NO_TOOLTIP
        minusXShiftToolButton->setToolTip(QApplication::translate("ClippingBoxDlg", "Shift box along its X dimension", 0));
#endif // QT_NO_TOOLTIP
        minusXShiftToolButton->setText(QApplication::translate("ClippingBoxDlg", "-X", 0));
#ifndef QT_NO_TOOLTIP
        plusXShiftToolButton->setToolTip(QApplication::translate("ClippingBoxDlg", "Shift box along its X dimension", 0));
#endif // QT_NO_TOOLTIP
        plusXShiftToolButton->setText(QApplication::translate("ClippingBoxDlg", "+X", 0));
#ifndef QT_NO_TOOLTIP
        minusYShiftToolButton->setToolTip(QApplication::translate("ClippingBoxDlg", "Shift box along its Y dimension", 0));
#endif // QT_NO_TOOLTIP
        minusYShiftToolButton->setText(QApplication::translate("ClippingBoxDlg", "-Y", 0));
#ifndef QT_NO_TOOLTIP
        plusYShiftToolButton->setToolTip(QApplication::translate("ClippingBoxDlg", "Shift box along its Y dimension", 0));
#endif // QT_NO_TOOLTIP
        plusYShiftToolButton->setText(QApplication::translate("ClippingBoxDlg", "+Y", 0));
#ifndef QT_NO_TOOLTIP
        minusZShiftToolButton->setToolTip(QApplication::translate("ClippingBoxDlg", "Shift box along its Z dimension", 0));
#endif // QT_NO_TOOLTIP
        minusZShiftToolButton->setText(QApplication::translate("ClippingBoxDlg", "-Z", 0));
#ifndef QT_NO_TOOLTIP
        plusZShiftToolButton->setToolTip(QApplication::translate("ClippingBoxDlg", "Shift box along its Z dimension", 0));
#endif // QT_NO_TOOLTIP
        plusZShiftToolButton->setText(QApplication::translate("ClippingBoxDlg", "+Z", 0));
    } // retranslateUi

};

namespace Ui {
    class ClippingBoxDlg: public Ui_ClippingBoxDlg {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_CLIPPINGBOXDLG_H
