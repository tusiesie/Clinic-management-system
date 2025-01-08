import datetime
from clinic.note import Note

class PatientRecord():
    ''' class that represents a patient's medical record '''

    def __init__(self):
        ''' construct a patient record '''
        self.counter = 0
        self.notes = []

    def __repr__(self):
        return "%r, %r" % (self.counter, self.notes)

    def __str__(self):
        return "There are %r notes for this patient" % self.counter

    def search_note(self, code):
        ''' search a note in the patient's record '''
        for note in self.notes:
            if note.code == code:
                return note
        # note not found
        return None

    def create_note(self, text):
        ''' create a note in the patient's record '''
        self.counter += 1
        current_time = datetime.datetime.now() # time note is created
        new_note = Note(self.counter, text, current_time)
        self.notes.append(new_note)
        return new_note

    def retrieve_notes(self, search_string):
        ''' retrieve notes in the patient's record that satisfy a search string '''
        # retrieve existing notes
        retrieved_notes = []
        for note in self.notes:
            if search_string in note.text:
                retrieved_notes.append(note)
        return retrieved_notes

    def update_note(self, code, new_text):
        ''' update a note from the patient's record '''
        updated_note = None

        # search the note by code
        for note in self.notes:
            if note.code == code:
                updated_note = note
                break

        # note does not exist
        if not updated_note:
            return False

        # note exists, update fields
        updated_note.text = new_text
        updated_note.timestamp = datetime.datetime.now()
        return True

    def delete_note(self, code):
        ''' delete a note from the patient's record '''
        note_to_delete_index = -1

        # first, search the note by code
        for i in range(len(self.notes)):
            if self.notes[i].code == code:
                note_to_delete_index = i
                break

        # note does not exist
        if note_to_delete_index == -1:
            return False

        # note exists, delete note
        self.notes.pop(note_to_delete_index)
        return True

    def list_notes(self):
        ''' list all notes from the patient's record from the 
            more recently added to the least recently added'''

        # list existing notes
        notes_list = []
        for i in range(-1, -len(self.notes)-1, -1):
            notes_list.append(self.notes[i])
        return notes_list
