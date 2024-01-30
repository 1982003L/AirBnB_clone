#!/usr/bin/python3
"""Setting console for AirBnB project"""


import cmd
import sys
import re
from models import storage
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class HBNBCommand(cmd.Cmd):
    """Setting methods and attributes for main console"""
    prompt = "(hbnb) "
    classes = ["BaseModel", "Amenity", "City", "Place", "Review",
               "State", "User"]
    aggregates = {"all()": 0, "count()": 1, r"show\(([^,]+)\)": 2,
                  r"destroy\(([^,]+)\)": 3,
                  r"update\(([^,]+),([^,]+),([^,]+)\)": 4}
    commands = ["do_all", "count", "do_show", "do_destroy", "do_update"]

    objects = storage.all()

    def do_quit(self, arg):
        "quit command to exit the program"
        return True

    def do_EOF(self, arg):
        """CTRL_C to Exit"""
        return True

    def emptyline(self):
        "dealing with an empty lines"
        pass

    def do_help(self, line):
        """overrides help method"""
        cmd.Cmd.do_help(self, line)

    def do_create(self, arg):
        """Creating instance of class"""
        if not arg:
            print("** class name missing **")
        else:
            try:
                instant_id = eval(arg)()
                instant_id.save()
                print(instant_id.id)
            except NameError:
                print("** class doesn't exist **")

    def do_show(self, arg):
        """Showing instance of class"""
        args = arg.split()
        if not arg:
            print("** class name missing **")
        else:
            class_name = args[0]
            if class_name not in self.classes:
                print("** class doesn't exist **")
            elif len(args) < 2:
                print("** instance id missing **")
            else:
                instant_id = args[1]
                key = "{}.{}".format(class_name, instant_id)
                if key in self.objects:
                    print(self.objects[key])
                else:
                    print("** no instance found **")

    def do_destroy(self, arg):
        """Destroy instance of class"""
        args = arg.split()
        if not args:
            print("** class name missing **")
        else:
            class_name = args[0]
            if class_name not in self.classes:
                print("** class doesn't exist **")
            elif len(args) < 2:
                print("** instance id missing **")
            else:
                instant_id = args[1]
                key = "{}.{}".format(class_name, instant_id)
                if key in self.objects:
                    del self.objects[key]
                    storage.save()
                else:
                    print("** no instance found **")

    def do_all(self, arg):
        """Printing all instance of class"""
        if not arg:
            print([str(value) for value in self.objects.values()])
        else:
            class_name = arg.split()[0]
            if class_name not in self.classes:
                print("** class doesn't exist **")
            else:
                filtered_objects = [str(value) for key, value in
                                    self.objects.items()
                                    if key.split(".")[0] == class_name]
                print(filtered_objects)

    def do_update(self, arg):
        """Updating instance of class"""
        args = arg.split()
        if not args:
            print("** class name missing **")
        else:
            class_name = args[0]
            if class_name not in self.classes:
                print("** class doesn't exist **")
            elif len(args) < 2:
                print("** instance id missing **")
            else:
                instant_id = args[1]
                key = "{}.{}".format(class_name, instant_id)
                if key not in self.objects:
                    print("** no instance found **")
                elif len(args) < 3:
                    print("** attribute name missing **")
                elif len(args) < 4:
                    print("** value missing **")
                else:
                    attribute_name = args[2]
                    attribute_value = args[3]
                    instant = self.objects[key]
                    setattr(instant, attribute_name, attribute_value)
                    instant.save()

    def count(self, arg):
        """counting all instance of class"""
        class_name = arg.split()[0]
        filtered_objects = [str(value) for key, value in
                            self.objects.items()
                            if key.split(".")[0] == class_name]
        print(len(filtered_objects))

    def default(self, arg):
        """Handles default behavior in console"""
        args = arg.split(".")
        if (len(args) == 2 and args[0] in self.classes and
            (self.aggregates.get(args[1]) is not None or
             (self.get_matching_index(args[1]) is not None
              and self.get_matching_index(args[1]) > 1))):
            module_name, method_name = arg.split(".")
            index = self.aggregates.get(method_name)
            if index is None:
                index = self.get_matching_index(args[1])
            if index is not None and module_name in self.classes:
                method = getattr(self, self.commands[index])
                if index > 1:
                    self.handle_commands_params(arg)
                else:
                    method(module_name)
        else:
            return super().default(arg)

    def get_matching_index(self, string):
        """Matches string with self.aggregates"""
        for pattern, index in self.aggregates.items():
            if re.match(pattern, string):
                return index
        return None

    def handle_commands_params(self, arg):
        """Handles commands params"""
        match = re.match(r'(\w+)\.(\w+)\((.*)\)$', arg)
        if match:
            class_name = match.group(1)
            method_name = match.group(2)
            param = match.group(3).replace('"', '').replace(',', ' ')
            if class_name not in self.classes:
                print(f"Unknown class: {class_name}")
            else:
                method = getattr(self, f"do_{method_name}")
                method(f"{class_name} {param}")

    def help_quit(self):
        """help for quit command"""
        print("Quit command to exit the program")
        print()

    def help_EOF(self):
        """help for EOF"""
        print()

        """commands: update
        """
    def help_create():
        """Create command creating a new instance"""
        print("Help command to create a new instance")
        print()

    def help_show():
        """Show command for Showing all attributes about instance"""
        print("Show command to display all attributes about instance")
        print()

    def help_destroy():
        """Destroy command for Deleting an instance"""
        print("Destroy command to delete an instance")
        print()

    def help_all():
        """All command to Display all objects"""
        print("All command to Displaying all objects")
        print()

    def help_update():
        """Update command to modify instance attributes"""
        print("Update command to modify instance attributes")
        print()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
