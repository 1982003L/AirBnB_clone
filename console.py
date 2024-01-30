#!/usr/bin/python3
"""
Airbnb Console
"""
import cmd
from models.base_model import BaseModel
from models.__init__ import storage
from models.user import User
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models.city import City
from models.state import State
import re


class HBNBCommand(cmd.Cmd):
    """
    The entry point for the command interpreter
    """
    prompt = '(hbnb) '
    classes = ['BaseModel', 'User', 'Place', 'State',
               'City', 'Amenity', 'Review']
    dotcmds = ['.all()']

    def do_create(self, line):
        """Creates a new instance of a given class, saves it
        (to the JSON file) and prints the id
        """
        if line == '':
            print('** class name missing **')
        elif line not in HBNBCommand.classes:
            print('** class doesn\'t exist **')
        else:
            if line == 'BaseModel':
                obj = BaseModel()
            elif line == 'User':
                obj = User()
            elif line == 'Place':
                obj = Place()
            elif line == 'State':
                obj = State()
            elif line == 'City':
                obj = City()
            elif line == 'Amenity':
                obj = Amenity()
            elif line == 'Review':
                obj = Review()
            storage.save()
            print(obj.id)

    def do_show(self, line):
        """A string representation of an instance depending
        on the class name and id
        """
        args = line.split()
        if line == '':
            print('** class name missing **')
        elif args[0] not in HBNBCommand.classes:
            print('** class doesn\'t exist **')
        else:
            if len(args) < 2:
                print('** instance id missing **')
            else:
                classname = args[0]
                objid = args[1]
                key = classname + '.' + objid
                try:
                    print(storage.all()[key])
                except KeyError:
                    print('** no instance found **')

    def do_destroy(self, line):
        """
        Remove an instance depending on class Name
        and id (changed saved at the JSON file)
        """
        args = line.split()
        if line == '':
            print('** class name missing **')
        elif args[0] not in HBNBCommand.classes:
            print('** class doesn\'t exist **')
        else:
            if len(args) < 2:
                print('** instance id missing **')
            else:
                classname = args[0]
                objid = args[1]
                key = classname + '.' + objid
                try:
                    del storage.all()[key]
                    storage.save()
                except KeyError:
                    print('** no instance found **')

    def do_all(self, line):
        """
        String representation of instance printing
        based or not on the class name. Ex: $ all BaseModel or $ all
        """
        args = line.split()
        result = []
        if len(args) != 0:
            if args[0] not in HBNBCommand.classes:
                print('** class doesn\'t exist **')
                return
            else:
                for _, value in storage.all().items():
                    if type(value).__name__ == args[0]:
                        result.append(value.__str__())
        else:
            for _, value in storage.all().items():
                result.append(value.__str__())
        print(result)

    def do_update(self, arg):
        """
        Handles update command
        """
        arg = arg.split()
        objects = storage.all()
        if len(arg) == 0:
            print("** class name missing **")
        elif arg[0] not in self.classes:
            print("** class doesn't exist **")
        elif len(arg) == 1:
            print("** instance id missing **")
        elif len(arg) > 1:
            try:
                instance = objects["{}.{}".format(arg[0], arg[1])]
            except Exception:
                print("** no instance found **")
                return
            if len(arg) == 2:
                print("** attribute name missing **")
            elif len(arg) == 3:
                print("** value missing **")
            else:
                attr = arg[2]
                value = str(arg[3])
                strings = ["\"", "\'"]
                if value[0] in strings or value[-1] in strings:
                    value = value.strip("'\"")
                else:
                    dot = False
                    letter = False
                    for c in value:
                        if c.isalpha():
                            letter = True
                        if c == ".":
                            dot = True
                    if letter is True:
                        value = str(value)
                    elif dot is True:
                        value = float(value)
                    else:
                        value = int(value)
                setattr(instance, attr, value)
                storage.save()

    def do_count(self, arg):
        """
        Counts the ocurence of a class Instance in storage
        """
        inst = storage.all()
        arg = arg.split()
        count = 0
        for instance in inst.values():
            if instance.__class__.__name__ == arg[0]:
                count += 1
        print(count)

    def default(self, line):
        """
        Handling the default behaviour when command that doesn't match
        defined methods is passed
        E.G => User.all()
        """
        full_match = re.search(r'[A-Z][a-z]+\.\w+\((.*?)\)', line)
        met_match = re.search(r'(?<=\.)\w+\((.*?)\)', line)
        met_dict = {
                "all": self.do_all,
                "show": self.do_show,
                "count": self.do_count,
                "update": self.do_update,
                "destroy": self.do_destroy,
                "create": self.do_create
                }
        if full_match and met_match:
            cls = re.search(r'^[A-Z][a-z]+', full_match.group(0))
            met = re.search(r'^\w+(?=\()', met_match.group(0))
            if not met or not cls:
                print("** Unknown syntax:", line)
            else:
                cls = cls.group(0)
                met = met.group(0)
                if cls in self.classes and met in met_dict.keys():
                    pattern = r'(?<=\()(.+?)(?=\))'
                    arg_search = re.search(pattern, met_match.group(0))
                    if arg_search:
                        args = arg_search.group(0).split(",")
                        args = " ".join([arg.strip("()\"' ") for arg in args])
                        met_dict[met](cls + " " + args)
                    else:
                        met_dict[met](cls)
                elif cls not in self.classes:
                    print("** class doesn't exist **")
                else:
                    print("** Unknown syntax:", line)
        else:
            print(" *** Unknown syntax:", line)

    def do_quit(self, line):
        """Quit command to exit from cmd"""
        return True

    def do_EOF(self, line):
        """Ctrl D - to kill the program or exit from cmd"""
        print()
        return True

    def emptyline(self):
        """Empty line + Enter shouldn't execute anything"""
        pass


if __name__ == '__main__':
    HBNBCommand().cmdloop()
