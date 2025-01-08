import hashlib
from clinic.patient import Patient
from clinic.note import Note
from clinic.dao.patient_dao_json import PatientDAOJSON
from clinic.dao.note_dao_pickle import NoteDAOPICKLE
from clinic.exception.invalid_login_exception import InvalidLoginException
from clinic.exception.duplicate_login_exception import DuplicateLoginException
from clinic.exception.invalid_logout_exception import InvalidLogoutException
from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.exception.illegal_operation_exception import IllegalOperationException
from clinic.exception.no_current_patient_exception import NoCurrentPatientException

class Controller():
    ''' controller class that receives the system's operations '''

    def __init__(self, autosave):
        ''' construct a controller class '''
        self.users = self.get_users()

        self.username = None
        self.password = None
        self.logged = False

        self.patient_dao = PatientDAOJSON(autosave)
        self.note_dao = None
        self.current_patient = None

        self.autosave = autosave
        
    def __str__(self):
        if self.logged_in:
            return "Username: %r, Password: %r, Number of patients: %r" % \
            (self.username, self.password, len(self.patients))
        else:
            return "not logged in"

    def get_users(self):
        filename = "clinic/users.txt"
        users = {}

        # save users from txt file to dictionary
        with open(filename, "r") as file:
            for line in file:
                data = line.strip().split(",")
                users[data[0]] = data[1]

        # return dictionary of users and their passwords
        return users

    def login(self, username, password):
        ''' user logs in the system '''
        # cannot log in if already logged in
        if self.logged:
            raise DuplicateLoginException("cannot login again while still logged in")

        if username in self.users:
            encoded_pass = hashlib.sha256(password.encode()).hexdigest()
            if encoded_pass == self.users[username]:
                self.username = username
                self.password = password
                self.logged = True
                return True # logged in successfully
            else:
                # given password incorrect
                raise InvalidLoginException("login with incorrect password")
        else:
            # given username incorrect
            raise InvalidLoginException("login with incorrect username")

    def logout(self):
        ''' user logs out from the system '''
        # cannot log out if not logged in
        if not self.logged:
            raise InvalidLogoutException("log out only after being logged in")
        else:
            self.username = None
            self.password = None
            self.logged = False
            self.current_patient = None
            return True # succuessfully logged out

    def search_patient(self, phn):
        ''' user searches a patient '''
        # must be logged in to do operation
        if not self.logged:
            raise IllegalAccessException("cannot search patient without logging in")

        # return searched patient
        return self.patient_dao.search_patient(phn)

    def create_patient(self, phn, name, birth_date, phone, email, address):
        ''' user creates a patient '''
        # must be logged in to do operation
        if not self.logged:
            raise IllegalAccessException("cannot create patient without logging in")

        # create patient
        patient = Patient(phn, name, birth_date, phone, email, address)

        # patient already exists, do not create
        if self.patient_dao.search_patient(phn):
            raise IllegalOperationException("cannot add a patient with a phn that is already registered")

        # create patient
        self.patient_dao.create_patient(patient)

        # return created patient
        return patient

    def retrieve_patients(self, name):
        ''' user retrieves the patients that satisfy a search criterion '''
        # must be logged in to do operation
        if not self.logged:
            raise IllegalAccessException("cannot retrieve patients without logging in")

        # return list of patients with searched name
        return self.patient_dao.retrieve_patients(name)

    def update_patient(self, original_phn, phn, name, birth_date, phone, email, address):
        ''' user updates a patient '''
        # must be logged in to do operation
        if not self.logged:
            raise IllegalAccessException("cannot update patient without logging in")

        # patient does not exist, cannot update
        if self.patient_dao.search_patient(original_phn) is None:
            raise IllegalOperationException("cannot update patient with a phn that is not registered")

        # create patient
        patient = Patient(phn, name, birth_date, phone, email, address)

        # patient is current patient, cannot update
        if self.current_patient:
            if patient.phn == self.current_patient.phn:
                raise IllegalOperationException("cannot update the current patient")

        # conflicting phn
        if original_phn != phn and self.patient_dao.search_patient(phn):
            raise IllegalOperationException("cannot update patient and give them a registered phn")

        # update patient
        self.patient_dao.update_patient(original_phn, patient)

        # update patient successful
        return True

    def delete_patient(self, phn):
        ''' user deletes a patient '''
        # must be logged in to do operation
        if not self.logged:
            raise IllegalAccessException("cannot delete patient without logging in")

        # patient does not exist, cannot delete
        if not self.patient_dao.search_patient(phn):
            raise IllegalOperationException("cannot delete patient with a phn that is not registered")

        # get patient
        patient = self.patient_dao.search_patient(phn)

        # patient is current patient, cannot delete
        if self.current_patient:
            if patient == self.current_patient:
                raise IllegalOperationException("cannot delete the current patient")

        # patient exists, delete patient
        self.patient_dao.delete_patient(phn)

        # delete patient successful
        return True

    def list_patients(self):
        ''' user lists all patients '''
        # must be logged in to do operation
        if not self.logged:
            raise IllegalAccessException("cannot list paitents without logging in")

        # get list of patients
        return self.patient_dao.list_patients()

    def set_current_patient(self, phn):
        ''' user sets the current patient '''

        # must be logged in to do operation
        if not self.logged:
            raise IllegalAccessException("cannot set current patient without logging in")

        # first, search the patient by key
        patient = self.patient_dao.search_patient(phn)

        # patient does not exist
        if not patient:
            raise IllegalOperationException("cannot set non-existent patient as the current patient")

        # update patient note
        if self.current_patient is None or patient.phn != self.current_patient.phn:
            self.note_dao = NoteDAOPICKLE(self.autosave, phn)

        # patient exists, set them to be the current patient
        self.current_patient = patient

        # set curent patient successful
        return True


    def get_current_patient(self):
        ''' get the current patient '''
        # must be logged in to do operation
        if not self.logged:
            raise IllegalAccessException("cannot get current patient without logging in")

        # return current patient
        return self.current_patient

    def unset_current_patient(self):
        ''' unset the current patient '''

        # must be logged in to do operation
        if not self.logged:
            raise IllegalAccessException("cannot unset current patient without logging in")

        # unset current patient
        self.current_patient = None
        self.note_dao = None


    def search_note(self, code):
        ''' user searches a note from the current patient's record '''
        # must be logged in to do operation
        if not self.logged:
            raise IllegalAccessException("cannot search note for a patient without logging in")

        # there must be a valid current patient
        if not self.current_patient:
            raise NoCurrentPatientException("cannot search note without a valid current patient")

        # search a new note with the given code and return it
        return self.note_dao.search_note(code)

    def create_note(self, text):
        ''' user creates a note in the current patient's record '''
        # must be logged in to do operation
        if not self.logged:
            raise IllegalAccessException("cannot add note for a patient without logging in")

        # there must be a valid current patient
        if not self.current_patient:
            raise NoCurrentPatientException("cannot add note without a valid current patient")

        # create a new note
        note = self.note_dao.create_note(text)

        # return created note
        return note

    def retrieve_notes(self, search_string):
        ''' user retrieves the notes from the current patient's record
            that satisfy a search string '''
        # must be logged in to do operation
        if not self.logged:
            raise IllegalAccessException("cannot retireve notes for a patient without logging in")

        # there must be a valid current patient
        if not self.current_patient:
            raise NoCurrentPatientException("cannot retrieve notes without a valid current patient")

        # return the found notes
        return self.note_dao.retrieve_notes(search_string)

    def update_note(self, code, new_text):
        ''' user updates a note from the current patient's record '''
        # must be logged in to do operation
        if not self.logged:
            raise IllegalAccessException("cannot update note for a patient without logging in")

        # there must be a valid current patient
        if not self.current_patient:
            raise NoCurrentPatientException("cannot update not without a valid current patient")

        # update note
        result =  self.note_dao.update_note(code, new_text)

        # return bool of update note successful
        return result


    def delete_note(self, code):
        ''' user deletes a note from the current patient's record '''
        # must be logged in to do operation
        if not self.logged:
            raise IllegalAccessException("cannot delete note for a patient without logging in")

        # there must be a valid current patient
        if not self.current_patient:
            raise NoCurrentPatientException("cannot delete note without a valid current patient")

        # delete note
        result = self.note_dao.delete_note(code)

        # return bool of delete note successful
        return result

    def list_notes(self):
        ''' user lists all notes from the current patient's record '''
        # must be logged in to do operation
        if not self.logged:
            raise IllegalAccessException("cannot list notes for a patient without logging in")

        # there must be a valid current patient
        if not self.current_patient:
            raise NoCurrentPatientException("cannot list notes without a valid current patient")

        # return list of all viable notes
        return self.note_dao.list_notes()
