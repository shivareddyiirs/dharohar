from cx_Freeze import setup, Executable as cxExecutable
import matplotlib
import os
wrk_drr=os.path.dirname(os.path.realpath('__file__'))
os.chdir(wrk_drr)

includefiles = ['debug/','forms/','images/','release/','document/','language script/']                
excludes = []
packages = ['numpy', 'matplotlib', 'PIL','skimage','scipy']

WIN_Target = cxExecutable(
    script='main.py',
    targetName='Dharohar.exe',
    base = "Win32GUI",
    icon = 'icon.ico'
)

setup(
    name='main',
    description="Script to test pubsub for packaging with cxfreeze",
    version='0.1',

    options={'build_exe': {'excludes': excludes, 'packages': packages, 'include_files': includefiles, }},
    executables=[WIN_Target]
)
