import json
from clinic.patient import Patient
from clinic.dao.patient_dao import PatientDAO
from clinic.dao.patient_encoder import PatientEncoder
from clinic.dao.patient_decoder import PatientDecoder

class PatientDAOJSON(PatientDAO):

    def __init__(self, autosave):
        self.autosave = autosave
        self.filename = "clinic/patients.json"
        self._load_data()

    def _load_data(self):
        '''get data from a file'''
        # load save file
        try:
            with open(self.filename, 'r') as file:
                list_patients = json.load(file, cls=PatientDecoder)

            self.patients = {}

            # turn list of patients into dictionary of patients
            for person in list_patients:
                self.patients[person.phn] = person

        # file does not exist, create empty dictionary
        except:
            self.patients = {}

    def _autosave(self):
        '''autosaves data into file'''
        # get patients from dictionary
        list_patients = list(self.patients.values())

        # save list of patients to file
        with open(self.filename, 'w') as file:
            json.dump(list_patients, file, cls=PatientEncoder, indent=4)

    def search_patient(self, key):
        '''user searches a patient'''
        # get patient, returns None if not found
        return self.patients.get(key)

    def create_patient(self, patient):
        '''user creates a patient'''
        # create new entry in paitent dictionary
        self.patients[patient.phn] = patient

        # if autosave on, save data to file
        if self.autosave:
            self._autosave()

    def retrieve_patients(self, search_string):
        '''user retrieves patients that satisfy a search criterion'''
        retrieved_patients = []

        # add patients to list if their name is searched
        for patient in self.patients.values():
            if search_string in patient.name:
                retrieved_patients.append(patient)

        # return list of searched patients
        return retrieved_patients

    def update_patient(self, key, patient):
        '''user updates a patient'''
        # delete previous entry of patient if phn changes
        if key != patient.phn and key in self.patients:
            del self.patients[key]

        # update patient details
        self.patients[patient.phn] = patient

        # if autosave on, save data to file
        if self.autosave:
            self._autosave()

    def delete_patient(self, key):
        '''user deletes a patient'''
        # delete patient
        del self.patients[key]

        # if autosave on, save data to file
        if self.autosave:
            self._autosave()

    def list_patients(self):
        '''user lists all patients'''
        # return a list of all patients
        return list(self.patients.values())
