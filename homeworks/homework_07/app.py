import argparse
from connect import session
from models import Group, Student, Teacher, Subject, Grade

BD_OPERATIONS = ['create', 'list', 'update', 'remove']
BD_MODELS = [Group, Student, Teacher, Subject, Grade]

def create_object(model, name):
    if name:
        obj = model(name=name)
        session.add(obj)
    else:
        print(f'Please provide a name for the new {model.__name__}')

def list_objects(model):
    objs = session.query(model).all()
    for obj in objs:
        print(f'{obj.id} | {obj.name}')

def update_object(model, id_, name):
    if id_ and name:
        obj = session.get(model, id_)
        if not obj:
            print(f'No {model.__name__} with id {id_} found')
        else:
            setattr(obj, 'name', name)
    else:
        print(f'Please provide id and a name for the {model.__name__} to be updated')

def remove_object(model, id_):
    if id_:
        obj = session.get(model, id_)
        if not obj:
            print(f'No {model.__name__} with id {id_} found')
        else:
            session.delete(obj)
    else:
        print(f'Please provide an id for the {model.__name__} to be removed')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--action", "-a", required=True, type=str, choices=BD_OPERATIONS)
    parser.add_argument("--model", "-m", required=True, type=str, choices=[model.__name__ for model in BD_MODELS])
    parser.add_argument("--id", type=int, default=None)
    parser.add_argument("--name", "-n", type=str, default=None)
    args = parser.parse_args()

    action = args.action
    model = next(model for model in BD_MODELS if model.__name__ == args.model)
    id_ = args.id
    name_ = args.name

    if action == 'create':
        create_object(model, name_)
    elif action == 'list':
        list_objects(model)
    elif action == 'update':
        update_object(model, id_, name_)
    elif action == 'remove':
        remove_object(model, id_)

    session.commit()
    session.close()

if __name__ == "__main__":
    main()