"""A simple pythonic module which can be used as an inheritable
class to lock, hide, and unhide attributes from the class """

__version__ = "1.0"
__author__ = "Jude BC"
__github__ = "https://github.com/judev1/attribmanager"
__license__ = "GNU General Public License v3.0"

class manage:
    """ A simple inheritable class which manages attributes
        visibility and interactivity

            lock():
                Makes the attribute read only. Locked attributes
                will not appear in the __dict__ attribute but
                instead in the __locked__ attribute.

            hide():
                Makes the attribute invisible. Hidden attributes
                will not appear anywhere, even in the __hidden__
                attribute where it is stored.

            unhide():
                Makes the attribute visible again.
    """

    def __getattribute__(self, name):
        """ Returns the value of an attribute while preventing
            the change of locked attributes and the __locked__
            attribute through mutations
        """

        if name == "__hidden__":
            return {}
        elif name == "__dict__":
            return super().__getattribute__(name)
        elif name == "__locked__":
            return super().__getattribute__(name).copy()
        else:
            if name in self.__locked__:
                try: return self.__locked__[name].copy()
                except: return self.__locked__[name]
            elif name in super().__getattribute__("__hidden__"):
                main = type(self).__name__
                raise AttributeError(f"'{main}' has no attribute '{name}'")

        if name in self.__dict__:
            return self.__dict__[name]
        else:
            return super().__getattribute__(name)

    def __setattr__(self, name, value):
        """ Sets the value of an object while preventing
            manual changes to the __locked__ attribute and
            raises an error if the value of a locked attribute
            is attempted to be changed
        """

        if name == "__locked__":
            for attr in self.__locked__:
                if attr not in value:
                    raise AttributeError(f"'{name}' cannot be removed")
                elif self.__locked__[attr] != value[attr]:
                    raise AttributeError(f"'{name}' cannot be changed")
        elif name in self.__locked__:
            raise AttributeError(f"'{name}' cannot be changed")

        super().__setattr__(name, value)
        if name != "__dict__":
            self.__dict__[name] = value

    def lock(self, name):
        """ Adds an attribute to the __locked__ attribute """

        attr = super().__getattribute__(name)
        super().__getattribute__("__locked__")[name] = attr
        self.__dict__.pop(name)
        del attr

    def hide(self, name):
        """ Adds an attribute to the __hidden__ attribute """

        attr = super().__getattribute__(name)
        if name in self.__dict__:
            super().__getattribute__("__hidden__")[name] = attr
            self.__dict__.pop(name)
        else:
            raise AttributeError(f"'{name}' cannot be hidden")

    def unhide(self, name):
        """ Removes an attribute from the __hidden__ attribute """

        hidden = super().__getattribute__("__hidden__")
        if name in hidden:
            self.__dict__[name] = hidden[name]
            hidden.pop(name)
        else:
            raise AttributeError(f"'{name}' is not hidden")

    __locked__ = {}
    __hidden__ = {}
