import logging
import os


class ControlFile:

    __slots__ = ("path","Package","Version",
                 "Section","Priority","Architecture",
                 "Depends","Maintainer","Description")

    def __init__(self,path):

        self.path = path
        
        # reading the control file
        with open(path,"r") as f:
            content = f.readlines()

        # updating attributes values based on content
        for line in content:
            line = line.strip()
            parts = line.split()
            key = parts[0][:-1] # removing ':'
            if key not in self.__slots__:
                raise ValueError("error when parsing {}: {}".format(path,key))
            setattr(self,key,parts[1])


    @staticmethod
    def search_files(root_folder):
        # goes down root folder, and return
        # all "control" named files which are directly in a
        # "debian" named folder
        r = {}
        for root,subdirs,files in os.walk(root_folder):
            if "debian" in subdirs:
                control_file_path = os.path.join(root,"debian","control")
                if os.path.isfile(control_file_path):
                    try :
                        cf = ControlFile(control_file_path)
                    except ValueError as ve:
                        logging.warning(ve)
                        cf = None
                    if cf:
                        r[cf.Package]=control_file_path
                    
        return r

    
        
