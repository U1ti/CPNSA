
from PyQt4.QtCore import QAbstractTableModel,Qt,QString,QModelIndex,SIGNAL
from PyQt4.QtGui import QBrush

class tableModel(QAbstractTableModel):
    
    def __init__(self, result = None, headers = None, parent=None):
        super(tableModel, self).__init__(parent)
        self.result = result or []
        self.headers = headers or []
       

    def rowCount(self, index=QModelIndex()):
        return len(self.result)
    
    def resetModel(self):
        self.result = []
        self.emit(SIGNAL('layoutChanged()'))
    
    def columnCount(self, index=QModelIndex()):
        return len(self.headers)

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def data(self, index, role):
        if index.isValid():
          
            if role == Qt.BackgroundColorRole:
                if self.result[index.row()][3] == 'TCP':
                    return QBrush(Qt.darkGreen)
                elif self.result[index.row()][3] == 'UDP':
                    return QBrush(Qt.cyan)
                
                elif self.result[index.row()][3] == 'IGMP':
                    return QBrush(Qt.gray)
                else:
                    return QBrush(Qt.darkYellow)
            if role == Qt.DisplayRole:
                row = index.row()
                column = index.column()
                value = self.result[row][column]
                return value
            if role == Qt.TextAlignmentRole:
                return Qt.AlignCenter
           
    def headerData(self, section, orientation, role):
       
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                
                if section < len(self.headers):
                    return self.headers[section]
                else:
                    return "not implemented"
            else:
                return QString("test %1").arg(section)
    
    def insertRows(self, position, rows, data, parent = QModelIndex()):
        
        self.beginInsertRows(parent, position, rows)
        
        while len(data) < len(self.headers):
            data.append('N/A')
        
        self.result.insert(position, data)
        self.endInsertRows()
        
        return True


    def insertColumns(self, position, columns, parent = QModelIndex()):
        
        rowCount = len(self.results)
        
        for i in range(columns):
            for j in range(rowCount):
                self.results[j].insert(position, '')
        
        self.endInsertColumns()
        
        return True