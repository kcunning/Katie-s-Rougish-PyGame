# INTIALISATION
import pygame, math, sys, random
from pygame.locals import *

from constants import *

class Treasure(object):
    ''' Not implemented yet. 
    '''
    def __init__(self, title, description, item_type, **kwargs):
        # These attributes are required for all Treasures
        self.title = title
        self.description = description
        self.item_type = item_type

        # The rest of the attibutes are optional depending on the item type
        [setattr(self, key, value) for key, value in kwargs.iteritems()]
        
    @classmethod
    def from_xml(cls, xml):
        """
        Creates a Treasure object from an etree XML object.
        Treasures can have abitrary attribute but must always have
        the required attributes, 'title', 'description', 'item_type'.
        If the XML element describing a Treasure attribute has
        a "type" attribute in its XML tag, this can be used to convert
        its value to int or float.
        """
        attribs = {}
        for element in xml:
            attribute = element.tag
            value = element.text.strip()

            # convert to appropriate type if that attribute is supplied
            if "type" in element.attrib:
                # the "type" attribute tells us what to convert this value to.
                attr_type = element.attrib["type"]
                try:
                    # Hopefully the "type" attribute is "int" or "float"
                    value = {
                        "int": int,
                        "float": float,
                        "string": str,
                    }[attr_type](value)
                except KeyError:
                    print "%s attribute has illegal 'type' attribute '%d'"
                    print "Supported conversion types: 'int', 'float', 'string'"

            attribs[attribute] = value

        # Now that we have all of the attribute, we can create the treasure
        # Note that if any of the required arguments of name, description and
        # item_type are absent, this will raise an exception
        return cls(**attribs)

