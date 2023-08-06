#!/usr/bin/python3

'''
    Shared file
    
    xml_reader 
    
    version: 1.0.0
'''

# Line numbering
# https://stackoverflow.com/questions/6949395/is-there-a-way-to-get-a-line-number-from-an-elementtree-element

# Force python XML parser not faster C accelerators
# because we can't hook the C implementationimport sys
import sys
import os.path

sys.modules['_elementtree'] = None
import xml.etree.ElementTree as ET  # pylint: disable=wrong-import-position;     # noqa: E402


class _LineNumberingParser(ET.XMLParser):
    def __init__(self, file_name):
        super().__init__()
        self.file_name_ = os.path.basename(os.path.normpath(file_name))

    def _start(self, tag, attr_list):
        element = super()._start(tag, attr_list)

        element.line_number = self.parser.CurrentLineNumber
        element.file_name = self.file_name_

        return element


def get_node_location(node):
    if hasattr(node, 'line_number'):
        assert hasattr(node, 'file_name')
        return '{}|L{}|<{}>'.format(node.file_name, node.line_number, node.tag)
    else:
        return node.tag


def load_xml_file(file_name: str):
    return ET.parse(file_name, parser=_LineNumberingParser(file_name))


class XmlReader:
    def __init__(self, xml_node):
        self.node_ = xml_node

    def location(self):
        return get_node_location(self.node_)

    def get_str(self, name: str, default:str=None, allowed:(list, tuple)=None) -> str:
        v = self.node_.attrib.get(name, None)
        if v is None:
            if default is None:
                raise UserWarning(f'{self.location()}: attribute "{name}" is missing')
            return default

        if allowed and v not in allowed:
            raise UserWarning(f'{self.location()}: attribute "{name}={v}" is invalid. Allowed values: {allowed}')

        return v

    def get_bool(self, name: str, default=None) -> bool:
        s = self.node_.attrib.get(name, None)
        if s is None:
            if default is None:
                raise UserWarning(f'{self.location()}: attribute "{name}" is missing')
            return default

        if s == '0':
            return False
        elif s == '1':
            return True
        else:
            raise UserWarning(f'{self.location()}: attribute "{name}={v}" is not a valid bool. Use "0" and "1"')

    def get_int(self, name: str, default=None, min_val=None, max_val=None) -> int:
        v = self.node_.attrib.get(name, None)
        if v is None:
            if default is None:
                raise UserWarning(f'{self.location()}: attribute "{name}" is missing')
            return default
            
        try:
            iv = int(v)
        except ValueError as ex:
            raise UserWarning(f'{self.location()}: attribute "{name}={v}" is not a valid int: {ex}')

        if min_val is not None and iv < min_val:
            raise UserWarning(f'{self.location()}: Attribute "{name}={v}" is less than {min_val}')

        if max_val is not None and iv > max_val:
            raise UserWarning(f'{self.location()}: Attribute "{name}={v}" is greater than {max_val}')

        return iv
        