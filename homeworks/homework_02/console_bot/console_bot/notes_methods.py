import copy
import pickle
from collections import UserDict
from pathlib import Path
from .note import Note
from .iterators import Iterator
from .output import NotesFindOutputInfo
from .format import HEADER_NOTE

                
class Notes(UserDict):
    def __init__(self):
        super().__init__()
        p = Path(__file__)
        Path(p.parent / 'Data').mkdir(parents=True, exist_ok=True)
        self.filename = p.parent / 'Data' / 'notes.pkl'
        #self.filename = "Data\\notes.pkl"


    def serialize(self):
        with open(self.filename, "wb") as file:
            pickle.dump(self, file)

    def deserialize(self):
        try:
            with open(self.filename, "rb") as file:
                notes = pickle.load(file)
            return notes
        except FileNotFoundError:
            return self
    
    def add_note(self, *args):
        if len(args) != 0:                          # incorrect validation, must be changed!
            note_text  = ' '.join(args)
            id = len(self.data)+1
            self.data[id] = Note(str(id), note_text)
            self.serialize()

    def delete_note(self, id: int):
        self.data.pop(int(id))
        new_data = {}
        for note in self.data.values():
            note.note_id.value = len(new_data)+1    # change id of note
            new_data[len(new_data)+1] = note        # change id in self.data.key
        self.data = copy.deepcopy(new_data)
       
    def edit_note(self, id, *args):
        note_text  = ' '.join(args)
        self.data[int(id)] = Note(id, note_text)
    
    def edit_note_tag(self, id, tag, *new_tag):
        self.data[int(id)].edit_tag(tag, *new_tag)

    def add_note_tag(self, id, *new_tag):
        self.data[int(id)].add_tag(*new_tag)
            
    def find_notes(self, text:str):
        print(HEADER_NOTE)
        return NotesFindOutputInfo().make_output(self, text)

    def show_all_notes(self):
        print(HEADER_NOTE)
        for item in Iterator(self):
            print(item)