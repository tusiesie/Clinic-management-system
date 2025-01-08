import pickle
from clinic.note import Note
from clinic.dao.note_dao import NoteDAO

class NoteDAOPICKLE(NoteDAO):

    def __init__(self, autosave, phn):
        self.autosave = autosave
        # set filename to {phn_number}.dat
        self.filename = "clinic/records/%s.dat" % phn
        self._load_data()

    def _load_data(self):
        '''load data from a file'''
        # load save file
        try:
            with open(self.filename, 'rb') as file:
                self.notes = pickle.load(file)

        # file does note exist, create empty list
        except:
            self.notes = []

    def _autosave(self):
        '''autosaves data into a file'''
        # save list of notes to file
        with open(self.filename, 'wb') as file:
            pickle.dump(self.notes, file)

    def search_note(self, key):
        '''user searches a note from the current patient's record'''
        # key out of index
        if len(self.notes) < key:
            return None

        # return found note
        return self.notes[key-1]

    def create_note(self, text):
        '''user creates a note in the current patient's record'''
        # get the next empty index
        index = len(self.notes) + 1

        # create new note
        note = Note(index, text)

        # append note
        self.notes.append(note)

        # if autosave on, save data to file
        if self.autosave:
            self._autosave()

        return note

    def retrieve_notes(self, search_string):
        '''user retrieves the notes from the current patient's record
           that satisfy a search string'''
        retrieved_notes = []

        # if keyword in note text, append note to retrieved notes
        for note in self.notes:
            if note:
                if search_string in note.text:
                    retrieved_notes.append(note)

        # return list of retrieved notes that contain keyword
        return retrieved_notes

    def update_note(self, key, text):
        '''user updates a note from the current patient's record'''
        # key not in note list
        if len(self.notes) < key:
            return False

        # note has been deleted
        if self.notes[key-1] is None:
            return False

        # create new note
        note = Note(key, text)

        # save note
        self.notes[key-1] = note

        # if autosave on, save data to file
        if self.autosave:
            self._autosave()

        # update note successful
        return True

    def delete_note(self, key):
        '''user deletes a ntoe from the current patient's record'''
        # if key not in note list
        if len(self.notes) < key:
            return False

        # note has already been deleted
        if self.notes[key-1] is None:
            return False

        # delete note
        self.notes[key-1] = None

        # if autosave on, save data to file
        if self.autosave:
            self._autosave()

        # delete note successful
        return True

    def list_notes(self):
        '''user lists all notes from the current patient's record'''
        list_notes = []

        # append notes in reverse order
        for note in reversed(self.notes):
            # note exists, has not been deleted
            if note:
                list_notes.append(note)

        # return a list of all viable notes
        return list_notes
