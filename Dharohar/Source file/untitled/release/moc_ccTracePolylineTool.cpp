/****************************************************************************
** Meta object code from reading C++ file 'ccTracePolylineTool.h'
**
** Created by: The Qt Meta Object Compiler version 67 (Qt 5.6.1)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include "../ccTracePolylineTool.h"
#include <QtCore/qbytearray.h>
#include <QtCore/qmetatype.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'ccTracePolylineTool.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 67
#error "This file was generated using the moc from 5.6.1. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
struct qt_meta_stringdata_ccTracePolylineTool_t {
    QByteArrayData data[17];
    char stringdata0[182];
};
#define QT_MOC_LITERAL(idx, ofs, len) \
    Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, \
    qptrdiff(offsetof(qt_meta_stringdata_ccTracePolylineTool_t, stringdata0) + ofs \
        - idx * sizeof(QByteArrayData)) \
    )
static const qt_meta_stringdata_ccTracePolylineTool_t qt_meta_stringdata_ccTracePolylineTool = {
    {
QT_MOC_LITERAL(0, 0, 19), // "ccTracePolylineTool"
QT_MOC_LITERAL(1, 20, 5), // "apply"
QT_MOC_LITERAL(2, 26, 0), // ""
QT_MOC_LITERAL(3, 27, 6), // "cancel"
QT_MOC_LITERAL(4, 34, 9), // "resetLine"
QT_MOC_LITERAL(5, 44, 10), // "exportLine"
QT_MOC_LITERAL(6, 55, 13), // "closePolyLine"
QT_MOC_LITERAL(7, 69, 1), // "x"
QT_MOC_LITERAL(8, 71, 1), // "y"
QT_MOC_LITERAL(9, 73, 17), // "updatePolyLineTip"
QT_MOC_LITERAL(10, 91, 16), // "Qt::MouseButtons"
QT_MOC_LITERAL(11, 108, 7), // "buttons"
QT_MOC_LITERAL(12, 116, 18), // "onWidthSizeChanged"
QT_MOC_LITERAL(13, 135, 19), // "onShortcutTriggered"
QT_MOC_LITERAL(14, 155, 12), // "onItemPicked"
QT_MOC_LITERAL(15, 168, 10), // "PickedItem"
QT_MOC_LITERAL(16, 179, 2) // "pi"

    },
    "ccTracePolylineTool\0apply\0\0cancel\0"
    "resetLine\0exportLine\0closePolyLine\0x\0"
    "y\0updatePolyLineTip\0Qt::MouseButtons\0"
    "buttons\0onWidthSizeChanged\0"
    "onShortcutTriggered\0onItemPicked\0"
    "PickedItem\0pi"
};
#undef QT_MOC_LITERAL

static const uint qt_meta_data_ccTracePolylineTool[] = {

 // content:
       7,       // revision
       0,       // classname
       0,    0, // classinfo
      11,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       0,       // signalCount

 // slots: name, argc, parameters, tag, flags
       1,    0,   69,    2, 0x09 /* Protected */,
       3,    0,   70,    2, 0x09 /* Protected */,
       4,    0,   71,    2, 0x09 /* Protected */,
       5,    0,   72,    2, 0x09 /* Protected */,
       6,    2,   73,    2, 0x09 /* Protected */,
       6,    1,   78,    2, 0x29 /* Protected | MethodCloned */,
       6,    0,   81,    2, 0x29 /* Protected | MethodCloned */,
       9,    3,   82,    2, 0x09 /* Protected */,
      12,    1,   89,    2, 0x09 /* Protected */,
      13,    1,   92,    2, 0x09 /* Protected */,
      14,    1,   95,    2, 0x09 /* Protected */,

 // slots: parameters
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void, QMetaType::Int, QMetaType::Int,    7,    8,
    QMetaType::Void, QMetaType::Int,    7,
    QMetaType::Void,
    QMetaType::Void, QMetaType::Int, QMetaType::Int, 0x80000000 | 10,    7,    8,   11,
    QMetaType::Void, QMetaType::Int,    2,
    QMetaType::Void, QMetaType::Int,    2,
    QMetaType::Void, 0x80000000 | 15,   16,

       0        // eod
};

void ccTracePolylineTool::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        ccTracePolylineTool *_t = static_cast<ccTracePolylineTool *>(_o);
        Q_UNUSED(_t)
        switch (_id) {
        case 0: _t->apply(); break;
        case 1: _t->cancel(); break;
        case 2: _t->resetLine(); break;
        case 3: _t->exportLine(); break;
        case 4: _t->closePolyLine((*reinterpret_cast< int(*)>(_a[1])),(*reinterpret_cast< int(*)>(_a[2]))); break;
        case 5: _t->closePolyLine((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 6: _t->closePolyLine(); break;
        case 7: _t->updatePolyLineTip((*reinterpret_cast< int(*)>(_a[1])),(*reinterpret_cast< int(*)>(_a[2])),(*reinterpret_cast< Qt::MouseButtons(*)>(_a[3]))); break;
        case 8: _t->onWidthSizeChanged((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 9: _t->onShortcutTriggered((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 10: _t->onItemPicked((*reinterpret_cast< const PickedItem(*)>(_a[1]))); break;
        default: ;
        }
    }
}

const QMetaObject ccTracePolylineTool::staticMetaObject = {
    { &ccOverlayDialog::staticMetaObject, qt_meta_stringdata_ccTracePolylineTool.data,
      qt_meta_data_ccTracePolylineTool,  qt_static_metacall, Q_NULLPTR, Q_NULLPTR}
};


const QMetaObject *ccTracePolylineTool::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *ccTracePolylineTool::qt_metacast(const char *_clname)
{
    if (!_clname) return Q_NULLPTR;
    if (!strcmp(_clname, qt_meta_stringdata_ccTracePolylineTool.stringdata0))
        return static_cast<void*>(const_cast< ccTracePolylineTool*>(this));
    if (!strcmp(_clname, "ccPickingListener"))
        return static_cast< ccPickingListener*>(const_cast< ccTracePolylineTool*>(this));
    if (!strcmp(_clname, "Ui::TracePolyLineDlg"))
        return static_cast< Ui::TracePolyLineDlg*>(const_cast< ccTracePolylineTool*>(this));
    return ccOverlayDialog::qt_metacast(_clname);
}

int ccTracePolylineTool::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = ccOverlayDialog::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 11)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 11;
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 11)
            *reinterpret_cast<int*>(_a[0]) = -1;
        _id -= 11;
    }
    return _id;
}
QT_END_MOC_NAMESPACE
