#!/usr/bin/python3
"""Module for the HBnB console."""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.city import City
from models.review import Review
from models.place import Place
from models.amenity import Amenity
from models.state import State

def parse(arg):
    curly_braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if curly_braces is None:
        if brackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:brackets.span()[0]])
            retl = [i.strip(",") for i in lexer]
            retl.append(brackets.group())
            return retl
    else:
        lexer = split(arg[:curly_braces.span()[0]])
        retl = [i.strip(",") for i in lexer]
        retl.append(curly_braces.group())
        return retl


class HBNBCommand(cmd.Cmd):
    """Defines the HolbertonBnB command interpreter.

    Attributes:
        prompt (str): The command prompt.
    """

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        """Do nothing when an empty line is entered."""
        pass

    def default(self, arg):
        """Default behavior for cmd module when input is invalid"""
        argdict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", arg)
        if match is not None:
            command_args = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", command_args[1])
            if match is not None:
                command = [command_args[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in argdict.keys():
                    call = "{} {}".format(command_args[0], command[1])
                    return argdict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program."""
        print("")
        return True

    def do_create(self, arg):
        """Usage: create <class>
        Create a new class instance and print its id.
        """
        command_args = parse(arg)
        if len(command_args) == 0:
            print("** class name missing **")
        elif command_args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(command_args[0])().id)
            storage.save()

    def do_show(self, arg):
        """Usage: show <class> <id> or <class>.show(<id>)
        Show the string representation of a instance.
        """
        command_args = parse(arg)
        objdict = storage.all()
        if len(command_args) == 0:
            print("** class name missing **")
        elif command_args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(command_args) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(command_args[0], command_args[1]) not in objdict:
            print("** no instance found **")
        else:
            print(objdict["{}.{}".format(command_args[0], command_args[1])])

    def do_destroy(self, arg):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
        Delete an instance based on the class given name and id."""
        command_args = parse(arg)
        objdict = storage.all()
        if len(command_args) == 0:
            print("** class name missing **")
        elif command_args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(command_args) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(command_args[0], command_args[1]) not in objdict.keys():
            print("** no instance found **")
        else:
            del objdict["{}.{}".format(command_args[0], command_args[1])]
            storage.save()

    def do_all(self, arg):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects."""
        command_args = parse(arg)
        if len(command_args) > 0 and command_args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            objl = []
            for obj in storage.all().values():
                if len(command_args) > 0 and command_args[0] == obj.__class__.__name__:
                    objl.append(obj.__str__())
                elif len(command_args) == 0:
                    objl.append(obj.__str__())
            print(objl)

    def do_count(self, arg):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class."""
        command_args = parse(arg)
        count = 0
        for obj in storage.all().values():
            if command_args[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def do_update(self, arg):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
       <class>.update(<id>, <attribute_name>, <attribute_value>) or
       <class>.update(<id>, <dictionary>)
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary."""
        command_args = parse(arg)
        objdict = storage.all()

        if len(command_args) == 0:
            print("** class name missing **")
            return False
        if command_args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(command_args) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(command_args[0], command_args[1]) not in objdict.keys():
            print("** no instance found **")
            return False
        if len(command_args) == 2:
            print("** attribute name missing **")
            return False
        if len(command_args) == 3:
            try:
                type(eval(command_args[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(command_args) == 4:
            obj = objdict["{}.{}".format(command_args[0], command_args[1])]
            if command_args[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[command_args[2]])
                obj.__dict__[command_args[2]] = valtype(command_args[3])
            else:
                    obj.__dict__[k] = v
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
