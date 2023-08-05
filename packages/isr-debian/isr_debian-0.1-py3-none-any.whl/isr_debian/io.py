import os
import shutil
import distutils
import functools
import logging
import subprocess
from distutils import dir_util


def _list_packages(install_path,excluded_packages):
    # list all package absolute paths located in install path
    # with the exception of excluded packages
    if not os.path.isdir(install_path):
        raise FileNotFoundError(install_path)
    return [ os.path.join(install_path,f) for f in os.listdir(install_path)
             if os.path.isdir(os.path.join(install_path,f))
             and not any([p in f for p in excluded_packages])]


def _get_library_file_paths(package_path):
    # given a package path (i.e. <>/install/my_package)
    # returns absolute paths to the so files it contains
    lib_folder = os.path.join(package_path,"lib")
    if not os.path.isdir(lib_folder):
        return []
    files = [ f for f in os.listdir(lib_folder)
              if os.path.isfile(os.path.join(lib_folder, f)) ]
    files = [ f for f in files
              if f.startswith("lib") and f.endswith(".so") ]
    return [ os.path.join(lib_folder,f) for f in files ]


def _get_site_packages_path(install_python_folder,package_path):
    # given a package path (i.e. <>/install/my_package)
    # returns absolute paths <>/install/my_package/lib/python/site-packages/
    # (None if no such directory)
    folder = os.path.join(package_path,install_python_folder)
    if not os.path.isdir(folder):
        return None
    return folder


def _list_libraries(package_paths):
    # given list of absolute paths to packages
    # i.e. [<...>/install/my_package1, <...>/install/my_package2, ... ]
    # return list of abs path to all libraries 
    #  [absolute path to so lib1, absolute path to lib2, ...]
    libs = list(map(_get_library_file_paths,package_paths))
    return [item for sublist in libs for item in sublist]


def _list_site_packages(install_python_folder,package_paths):
    # given list of absolute paths to packages
    # i.e. [<...>/install/my_package1, <...>/install/my_package2, ... ]
    # return list to abs paths to python/site-packages folders
    _partial_get_site_packages_path = functools.partial(_get_site_packages_path,
                                                        install_python_folder) 
    paths = list(map(_partial_get_site_packages_path,package_paths))
    return [p for p in paths if p is not None]


def _copy_library_file(target_folder,
                       target_lib_folder,
                       abs_path_to_lib):
    # copy file to <target_folder>/usr/lib/
    target = os.path.join(target_folder,target_lib_folder)
    try :
        os.makedirs(target)
    except FileExistsError:
        pass
    except OSError as e:
        raise OSError("failed to create {}: {}".format(target,e))
    logging.info("copying {} to {}".format(abs_path_to_lib,target))
    shutil.copy(abs_path_to_lib,target)

def _copy_site_packages_files(target_folder,
                              target_python_folder,
                              abs_path_to_folder):
    # copy content of abs_path_to_folder
    # to <target_folder>/usr/local/lib/python3.6/dist-packages/
    target = os.path.join(target_folder,target_python_folder)
    try :
        os.makedirs(target)
    except FileExistsError:
        pass
    except OSError as e:
        raise OSError("failed to create {}: {}".format(target,e))
    logging.info("copying {} to {}".format(abs_path_to_folder,target))
    dir_util.copy_tree(abs_path_to_folder,target)


def _call_dpkg_deb(root_folder,package_name):

    os.chdir(root_folder)
    
    def _call(command):
        try:
            out = subprocess.check_output(command,
                                          stderr=subprocess.STDOUT,
                                          shell=True)
        except Exception as e:
            raise RuntimeError("Failed to call {}: {}".format(
                command, e))
    
    _call("dpkg-deb --build debian")
    _call("mv debian.deb {}.deb".format(package_name))

    
def prepare_debian(config):
    
    # listing packages that are in install
    packages = _list_packages(config.install_folder,config.excluded_ament_packages)
    for package in packages:
        logging.info("package detected: {}".format(package))
        
    # getting list of all corresponding so files
    libraries = _list_libraries(packages)
    for lib in libraries:
        logging.info("library detected: {}".format(lib))
        
    # copying all these files to /usr/lib/
    logging.info("copying libraries to: {}".format(config.build_folder))
    _copy_lib=functools.partial(_copy_library_file,
                                config.build_folder,
                                config.debian_lib_folder)
    list(map(_copy_lib,libraries))
    
    # list of all python packages
    logging.info("copying python packages to: {}".format(config.debian_python_folder))
    python_packages = _list_site_packages(config.install_python_folder,packages)
    
    # copying all site-packages/* to /usr/local/lib/python3.6/dist-packages
    _copy_python_package=functools.partial(_copy_site_packages_files,
                                           config.build_folder,
                                           config.debian_python_folder)
    list(map(_copy_python_package,python_packages))
    
    # copying the control file path to the DEBIAN folder
    debian_folder = os.path.join(config.build_folder,"DEBIAN")
    try :
        os.makedirs(debian_folder)
    except FileExistsError:
        pass
    except OSError as e:
        raise OSError("failed to create {}: {}".format(debian_folder,e))
    logging.info("copying control file {} to {}".format(config.control_file_path,
                                                        debian_folder))
    shutil.copy(config.control_file_path,debian_folder)


    # creating the debian file
    logging.info("creating debian file")
    _call_dpkg_deb(os.path.join(config.build_folder,".."),
                   config.debian_package)
        
    # done !
    logging.info("done")
