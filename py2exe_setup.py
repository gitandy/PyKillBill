# This will create a dist directory containing the executable file, all the data
# directories. All Libraries will be bundled in executable file.
#
# To build exe, python, and py2exe have to be installed. After
# building exe none of this libraries are needed.

try:
    from distutils.core import setup
    import py2exe
    from modulefinder import Module
    import glob, fnmatch
    import sys, os, shutil
    import operator
    import version
except ImportError, message:
    raise SystemExit,  "Unable to load module. %s" % message

#import version
 
class BuildExe:
    def __init__(self):
        #Name of starting .py
        self.script = "killBillTray.pyw"
 
        #Name of program
        self.project_name = "Kill Bill"
 
        #Project url
        self.project_url = "about:none"
 
        #Version of program
        self.project_version = version.VERSION[1:]
 
        #License of the program
        self.license = "Copyright (c) 2011-2012, Andreas Schawo"
 
        #Auhor of program
        self.author_name = "Andreas Schawo"
        self.author_email = "andreas@schawo.de"
        self.copyright = "Copyright (c) 2011-2012, Andreas Schawo"
 
        #Description
        self.project_description = "Kill Bill"
 
        #Icon file
        self.icon_file = 'images/logo.ico'
 
        #Extra files/dirs copied to game
        self.extra_datas = []
 
        #Extra/excludes python modules
        self.extra_modules = ['sip']
        self.exclude_modules = []
        
        #DLL Excludes
        self.exclude_dll = ['MSVCP90.dll']
 
        #Zip file name (None will bundle files in exe instead of zip file)
        self.zipfile_name = None
 
        #Dist directory
        self.dist_dir = 'dist'
 
    ## Code from DistUtils tutorial at http://wiki.python.org/moin/Distutils/Tutorial
    ## Originally borrowed from wxPython's setup and config files
    def opj(self, *args):
        path = os.path.join(*args)
        return os.path.normpath(path)
 
    def find_data_files(self, srcdir, *wildcards, **kw):
        # get a list of all files under the srcdir matching wildcards,
        # returned in a format to be used for install_data
        def walk_helper(arg, dirname, files):
            if '.svn' in dirname:
                return
            names = []
            lst, wildcards = arg
            for wc in wildcards:
                wc_name = self.opj(dirname, wc)
                for f in files:
                    filename = self.opj(dirname, f)
 
                    if fnmatch.fnmatch(filename, wc_name) and not os.path.isdir(filename):
                        names.append(filename)
            if names:
                lst.append( (dirname, names ) )
 
        file_list = []
        recursive = kw.get('recursive', True)
        if recursive:
            os.path.walk(srcdir, walk_helper, (file_list, wildcards))
        else:
            walk_helper((file_list, wildcards),
                        srcdir,
                        [os.path.basename(f) for f in glob.glob(self.opj(srcdir, '*'))])
        return file_list
 
    def run(self):
        if os.path.isdir(self.dist_dir): #Erase previous destination dir
            shutil.rmtree(self.dist_dir)
        
        #List all data files to add
        extra_datas = []
        for data in self.extra_datas:
            if os.path.isdir(data):
                extra_datas.extend(self.find_data_files(data, '*'))
            else:
                extra_datas.append(('.', [data]))
        
        setup(
            version = self.project_version,
            description = self.project_description,
            name = self.project_name,
            url = self.project_url,
            author = self.author_name,
            author_email = self.author_email,
            license = self.license,
 
            # targets to build
            windows = [{
                'script': self.script,
                'icon_resources': [(0, self.icon_file)],
                'copyright': self.copyright
            }],
            options = {'py2exe': {'optimize': 2, 'bundle_files': 1, 'compressed': True, \
                                  'excludes': self.exclude_modules, 'packages': self.extra_modules, \
                                  'dll_excludes': self.exclude_dll} },
            zipfile = self.zipfile_name,
            data_files = extra_datas,
            dist_dir = self.dist_dir
            )
        
        if os.path.isdir('build'): #Clean up build dir
            shutil.rmtree('build')
 
if __name__ == '__main__':
    if operator.lt(len(sys.argv), 2):
        sys.argv.append('py2exe')
    BuildExe().run() #Run generation
