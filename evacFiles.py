import os
import shutil

SRCFILE = ''
IMGPATH = ''
destPath = os.path.abspath(IMGPATH)

srcFiles = [SRCFILE, 'main_images', 'sub_images']
destFiles = [destPath, destPath, destPath]

if os.path.exists(destPath):
    for i, srcFile in enumerate(srcFiles):
        shutil.copy(srcFiles[i], destFiles[i])
    shutil.copyfile(SRCFILE, destPath)
    shutil.copytree('main_images', destPath)
    shutil.copytree('sub_images', destPath)
