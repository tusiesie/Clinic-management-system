import sys
from PyQt6.QtCore import Qt, QAbstractTableModel
from clinic.controller import Controller
from clinic.patient import Patient

class PatientTableModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._data = []

    def search_patient(self, patient_list):
        '''Updates the tabled model with a list of patients'''
        self._data = []
        for patient in patient_list:
            temp = []
            temp.append(patient.phn)
            temp.append(patient.name)
            temp.append(patient.birth_date)
            temp.append(patient.phone)
            temp.append(patient.email)
            temp.append(patient.address)
            self._data.append(temp)
        # emitting the layoutChanged signal to aler the QTable View of model changes
        self.layoutChanged.emit()

    def reset(self):
        '''Resets the data to an empty state and emits the layoutChange signal'''
        self._data = []
        # emitting the layoutChanged signal to alert the QTableView of model changes
        self.layoutChanged.emit()

    def data(self, index, role):
        '''Returns the data to be displayed in the table cell'''
        value = self._data[index.row()][index.column()]

        if role == Qt.ItemDataRole.DisplayRole:
            # Perform per-type checks and render accordingly.
            if isinstance(value, int):
                # Render float to 2 dp
                return "%d" % value
            if isinstance(value, str):
                # Render strings with quotes
                return '%s' % value
            # Default (anything not captured above: e.g. int)
            return value

        if role == Qt.ItemDataRole.TextAlignmentRole:
            if isinstance(value, int) or isinstance(value, float):
                # Align right, vertical middle.
                return Qt.AlignmentFlag.AlignVCenter + Qt.AlignmentFlag.AlignRight

    def rowCount(self, index):
        '''Retruend the number of rows in the model'''
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        '''Returns the number of columns'''
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        if self._data:
            return len(self._data[0])
        else:
            return 0

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        '''Return the header data for each column'''
        headers = ["PHN", "Name", "Birth Date", "Phone", "Email", "Address"]
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return '%s' % headers[section]
        return super().headerData(section, orientation, role)
