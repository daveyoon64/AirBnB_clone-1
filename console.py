#!/usr/bin/python3
'''
    Implementing the console for the HBnB project.
'''
import cmd
import json
import shlex
import os
import models
from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    '''
        Contains the entry point of the command interpreter.
    '''
    prompt = ("(hbnb) ")

    def do_quit(self, args):
        '''
            Quit command to exit the program.
        '''
        return True

    def do_EOF(self, args):
        '''
            Exits after receiving the EOF signal.
        '''
        return True

    def do_create(self, args):
        '''
            Create a new instance of class BaseModel and saves it
            to the JSON file.
        '''
        if len(args) == 0:
            print("** class name missing **")
            return
        try:
            args = args.split(" ")
            new_instance = eval(args[0])()
            for i in range(1, len(args)):
                if "=" in args[i]:
                    arg_list = args[i].split("=")
                    if arg_list[1][0] == "\"":
                        to_validate_value = arg_list[1][1:-1]
                        validated_value = to_validate_value.replace('"', r'\"')
                        validated_value = validated_value.replace("'", r"\'")
                        validated_value = validated_value.replace("_", r" ")
                    else:
                        if "." in arg_list[1]:
                            try:
                                validated_value = float(arg_list[1])
                            except Exception as e:
                                print(e)
                                pass
                        else:
                            try:
                                validated_value = int(arg_list[1])
                            except Exception as e:
                                print(e)
                                pass
                    if hasattr(new_instance, arg_list[0]):
                        setattr(new_instance, arg_list[0], validated_value)
                else:
                    pass
            new_instance.save()
            print(new_instance.id)
        except Exception as e:
            print(e)
            print("** class doesn't exist **")

    def do_show(self, args):
        '''
            Print the string representation of an instance baed on
            the class name and id given as args.
        '''
        args = shlex.split(args)
        if len(args) == 0:
            print("** class name missing **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        storage = models.storage
        obj_dict = storage.all()
        try:
            eval(args[0])
        except NameError:
            print("** class doesn't exist **")
            return
        key = args[0] + "." + args[1]
        key = args[0] + "." + args[1]
        try:
            value = obj_dict[key]
            print(value)
        except KeyError:
            print("** no instance found **")

    def do_destroy(self, args):
        '''
            Deletes an instance based on the class name and id.
        '''
        args = shlex.split(args)
        if len(args) == 0:
            print("** class name missing **")
            return
        elif len(args) == 1:
            print("** instance id missing **")
            return
        class_name = args[0]
        class_id = args[1]
        storage = models.storage
        obj_dict = storage.all()
        try:
            eval(class_name)
        except NameError:
            print("** class doesn't exist **")
            return
        key = class_name + "." + class_id
        try:
            del obj_dict[key]
        except KeyError:
            print("** no instance found **")
        storage.save()

    def do_all(self, args):
        '''
            Prints all string representation of all instances
            based or not on the class name.
        '''
        obj_list = []
        if os.environ['HBNB_TYPE_STORAGE'] == 'file':
            storage = models.storage
            objects = storage.all(args)
            try:
                if len(args) != 0:
                    eval(args)
            except NameError:
                print("** class doesn't exist **")
                return
            for key, val in objects.items():
                if len(args) != 0:
                    if type(val) is eval(args):
                        obj_list.append(val)
                else:
                    obj_list.append(val)
            print(obj_list)
        else:
            queries = []
            storage = models.storage
            query = storage.all(args)
            for k, v in query.items():
                queries.append(v)
            print(queries)

    def do_update(self, args):
        '''
            Update an instance based on the class name and id
            sent as args.
        '''
        storage = models.storage
        args = shlex.split(args)
        if len(args) == 0:
            print("** class name missing **")
            return
        elif len(args) == 1:
            print("** instance id missing **")
            return
        elif len(args) == 2:
            print("** attribute name missing **")
            return
        elif len(args) == 3:
            print("** value missing **")
            return
        try:
            eval(args[0])
        except NameError:
            print("** class doesn't exist **")
            return
        key = args[0] + "." + args[1]
        obj_dict = storage.all()
        try:
            obj_value = obj_dict[key]
        except KeyError:
            print("** no instance found **")
            return
        try:
            attr_type = type(getattr(obj_value, args[2]))
            args[3] = attr_type(args[3])
        except AttributeError:
            pass
        setattr(obj_value, args[2], args[3])
        obj_value.save()

    def emptyline(self):
        '''
            Prevents printing anything when an empty line is passed.
        '''
        pass

    def do_count(self, args):
        '''
            Counts/retrieves the number of instances.
        '''
        obj_list = []
        storage = models.storage
        objects = storage.all()
        try:
            if len(args) != 0:
                eval(args)
        except NameError:
            print("** class doesn't exist **")
            return
        for key, val in objects.items():
            if len(args) != 0:
                if type(val) is eval(args):
                    obj_list.append(val)
            else:
                obj_list.append(val)
        print(len(obj_list))

    def default(self, args):
        '''
            Catches all the function names that are not expicitly defined.
        '''
        functions = {"all": self.do_all, "update": self.do_update,
                     "show": self.do_show, "count": self.do_count,
                     "destroy": self.do_destroy, "update": self.do_update}
        args = (args.replace("(", ".").replace(")", ".")
                .replace('"', "").replace(",", "").split("."))

        try:
            cmd_arg = args[0] + " " + args[2]
            func = functions[args[1]]
            func(cmd_arg)
        except Exception:
            print("*** Unknown syntax:", args[0])


if __name__ == "__main__":
    '''
        Entry point for the loop.
    '''
    HBNBCommand().cmdloop()
