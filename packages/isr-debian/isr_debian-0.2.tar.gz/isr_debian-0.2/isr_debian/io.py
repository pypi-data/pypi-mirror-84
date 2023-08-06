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


def _get_config_path(install_config_folder,package_path):
    # given a package path (i.e. <>/install/my_package)
    # returns absolute path to the config files,
    # i.e. <>/install/my_package/opt/mpi-is/ (if default config)
    # (None if no such directory)
    folder = os.path.join(package_path,install_config_folder)
    if not os.path.isdir(folder):
        return None
    return folder


def list_executables(packages_path):
    # given list of absolute paths to packages
    # i.e. [<...>/install/my_package1, <...>/install/my_package2, ... ]
    # return list of all executables, i.e. content of bin folders
    r = []
    for path in packages_path:
        bin_folder = os.path.join(path,"bin")
        if os.path.isdir(bin_folder):
            content = os.listdir(bin_folder)
            files = [os.path.join(bin_folder,c) for c in content
                     if os.path.isfile(os.path.join(bin_folder,c))]
            r +=  files
    return r
    

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


def _list_config_folders(install_config_folder,package_path):
    # given list of absolute paths to packages
    # i.e. [<...>/install/my_package1, <...>/install/my_package2, ... ]
    # return list to abs paths to configuration folder,
    # i.e. opt/mpi-is (if default config) folders
    _partial_get_site_packages_path = functools.partial(_get_config_path,
                                                        install_config_folder) 
    paths = list(map(_partial_get_site_packages_path,package_path))
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


def _copy_config_folder(target_folder,
                        target_config_folder,
                        abs_path_to_folder):
    # copy content of abs_path_to_folder
    # to <target_folder>/opt/mpi-is/ (or other user selected
    # folder)
    target = os.path.join(target_folder,target_config_folder)
    try :
        os.makedirs(target)
    except FileExistsError:
        pass
    except OSError as e:
        raise OSError("failed to create {}: {}".format(target,e))
    logging.info("copying {} to {}".format(abs_path_to_folder,target))
    dir_util.copy_tree(abs_path_to_folder,target)


def _copy_include_folder(target_folder,
                         package_path):
    include_folder = os.path.join(package_path,"include")
    if not os.path.isdir(include_folder):
        # this package does not have an include folder
        return
    logging.info("copying {} to {}".format(include_folder,target_folder))
    dir_util.copy_tree(include_folder,target_folder)
    
    
def _copy_control_file(debian_folder,
                       control_file_path):
    try :
        os.makedirs(debian_folder)
    except FileExistsError:
        pass
    except OSError as e:
        raise OSError("failed to create {}: {}".format(debian_folder,e))
    shutil.copy(control_file_path,debian_folder)

    

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
    
    # listing packages that are in the "install" folder
    packages = _list_packages(config.install_folder,config.excluded_ament_packages)
    for package in packages:
        logging.info("package detected: {}".format(package))
        
    # getting list of all corresponding *.so files
    libraries = _list_libraries(packages)
    for lib in libraries:
        logging.info("library detected: {}".format(lib))
        
    # copying all these files to usr/local/lib/
    _copy_lib=functools.partial(_copy_library_file,
                                config.build_folder,
                                config.debian_lib_folder)
    list(map(_copy_lib,libraries))

    # copying include folders
    debian_include_folder = os.path.join(config.build_folder,
                                         config.debian_include_folder)
    try :
        os.makedirs(debian_include_folder)
    except FileExistsError:
        pass
    _copy_include=functools.partial(_copy_include_folder,
                                    debian_include_folder)
    list(map(_copy_include,packages))

    # listing abs path to executables
    executables = list_executables(packages)
    for executable in executables:
        logging.info("executable detected: {}".format(executable))

    # copying executables
    debian_bin_folder = os.path.join(config.build_folder,
                                     config.debian_bin_folder)
    try :
        os.makedirs(debian_bin_folder)
    except FileExistsError:
        pass
    for executable in executables:
        logging.info("copying {} to {}".format(executable,
                                               debian_bin_folder))
        shutil.copy(executable,debian_bin_folder)
    
    # list of all python packages
    python_packages = _list_site_packages(config.install_python_folder,packages)
    for python_package in python_packages:
        logging.info("python package detected: {}".format(python_package))
    
    # copying all site-packages/* to /usr/local/lib/python3.6/dist-packages
    _copy_python_package=functools.partial(_copy_site_packages_files,
                                           config.build_folder,
                                           config.debian_python_folder)
    list(map(_copy_python_package,python_packages))

    # list of all config folders
    config_folders = _list_config_folders(config.install_config_folder,packages)
    for config_folder in config_folders:
        logging.info("config folder detected: {}".format(config_folder))
    
    # copying all <package path>/opt/mpi-is/* to <debian>/opt/mpi-is/*
    logging.info("copying config folders to: {}".format(config.debian_config_folder))
    _p_copy_config_folder=functools.partial(_copy_config_folder,
                                            config.build_folder,
                                            config.debian_config_folder)
    list(map(_p_copy_config_folder,config_folders))
    
    # copying the (user selected) control file path
    # (which is in the selected package source) to the DEBIAN folder
    debian_folder = os.path.join(config.build_folder,"DEBIAN")
    logging.info("copying control file {} to {}".format(config.control_file_path,
                                                        debian_folder))
    _copy_control_file(debian_folder,config.control_file_path)

    # creating the debian file
    logging.info("creating debian file")
    _call_dpkg_deb(os.path.join(config.build_folder,".."),
                   config.debian_package)
        
    # done !
    logging.info("done")
