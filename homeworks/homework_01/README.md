# Console Bot / Personal Assistant

This application give you ability to use prepared classes for making Contacts Book and Notes with ability to manipulate with rows of book and notes.
Contacts Book contains Contact Name, Phones, Email, Address and Birthday information.
Notes contains Text Note and Tags for each note. 

## Features

- Add full contact
- Add name of person
- Add phone \ list of phones to person
- Add email
- Add address
- Add birthday

- Get person by query (searching in all fields)
- Paginated iterator for Contacts Book (realized but not implemented)

- Add text note
- Add tags to note

- Find notes by query

- Colored table output

- Save data to file

## Files

- main.py: starts Bot
- fields.py: contains the fields of Contacts Book and Notes with validation and set methods
- record.py:  class Record with Person info 
- note.py: class Note with Note info
- book_methods.py: contains the methods to manage contacts
- note_methods.py: contains the methods to manage notes
- bot.py: contains the methods of Console Bot
- iterators.py: contains iterator and paginate iterator for Contacts Book and Notes
- exceptions.py: contains the exceptions
- commands.py: contains the methods to generate commands to manage contacts, notes and bot
- output.py: contains the methods to generate output information
- format.py: contains some variables and methods for formatting output

