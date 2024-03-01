from fields import  NoteID, NoteTags, NoteText
from output import NotesOutputInfo

class Note:
    def __init__(self, note_id:str, note_text: str, *tags: str):
        self.note_text = NoteText(note_text)
        self.note_id = NoteID(note_id)
        if tags:
            self.tags = [NoteTags(tag) for tag in tags]
        else:
            self.tags = []
    
    def add_tag(self, *tags):
        for tag in tags:
            if not any(obj.value == tag for obj in self.tags):
                tag_obj = NoteTags(tag)
                self.tags.append(tag_obj)
    
    def find_in_tag(self, string):
        for t in self.tags:
            if string in t.value:
                return ', '.join(t.value for t in self.tags)
    
    def find_in_text(self, string:str):
        if string in self.note_text.value:
            return self.note_text.value
    
    def remove_tag(self,  tag):
        for t in self.tags:
            if tag == t.value:
                self.tags.remove(t)
            # else:
            #     print(ValueError('Tag not found'))

    def edit_tag(self, tag, new_tag):   # add new tag even when editable tag not exist
        self.remove_tag(tag)
        self.add_tag(new_tag)

    def __str__(self):
        return NotesOutputInfo().make_output(self)

    