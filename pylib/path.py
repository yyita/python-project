import os
import stat
import pathlib
import datetime
import typing
class CategoryID:
    all = 0
    file = 1
    folder = 2
def search(
    #1 通用匹配项
    topFolder = os.getcwd(),
    deepSearch = False,
    category = CategoryID.all,
    nameMatcher: typing.Callable[[str], bool] = None,
    excludeReadonly = True,
    excludeHidden = True,
    creationTimeLowerLimit: datetime.datetime = None,
    creationTimeUpperLimit: datetime.datetime = None,
    modificationTimeLowerLimit: datetime.datetime = None,
    modificationTimeUpperLimit: datetime.datetime = None,
    accessTimeLowerLimit: datetime.datetime = None,
    accessTimeUpperLimit: datetime.datetime = None,
    #2 文件专用项
    # 单位：B
    sizeMinimum: int = None,
    sizeMaximum: int = None,
    encoding = "UTF-8",
    dataMatcher: typing.Callable[[str], bool] = None,
):
    need_gettingStatus = any((
        creationTimeLowerLimit, creationTimeUpperLimit,
        modificationTimeLowerLimit, modificationTimeUpperLimit,
        accessTimeLowerLimit, accessTimeUpperLimit,
        excludeHidden, excludeReadonly, sizeMinimum, sizeMaximum
    ))
    need_gettingCreationTime = any((creationTimeLowerLimit, creationTimeUpperLimit))
    need_gettingModificationTime = any((modificationTimeLowerLimit, modificationTimeUpperLimit))
    need_gettingAccessTime = any((accessTimeLowerLimit, accessTimeUpperLimit))
    def isInvalidStatus_for_generic(status: os.stat_result):
        if excludeReadonly and (status.st_file_attributes & stat.FILE_ATTRIBUTE_READONLY):
            return True
        if excludeHidden and (status.st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN):
            return True
        if need_gettingCreationTime:
            creationTime = datetime.datetime.fromtimestamp(status.st_ctime)
            if creationTimeLowerLimit and (creationTime < creationTimeLowerLimit):
                return True
            if creationTimeUpperLimit and (creationTimeUpperLimit < creationTime):
                return True
        if need_gettingModificationTime:
            modificationTime = datetime.datetime.fromtimestamp(status.st_mtime)
            if modificationTimeLowerLimit and (modificationTime < modificationTimeLowerLimit):
                return True
            if modificationTimeUpperLimit and (modificationTimeUpperLimit < modificationTime):
                return True
        if need_gettingAccessTime:
            accessTime = datetime.datetime.fromtimestamp(status.st_atime)
            if accessTimeLowerLimit and (accessTime < accessTimeLowerLimit):
                return True
            if accessTimeUpperLimit and (accessTimeUpperLimit < accessTime):
                return True
        return False
    for parentFolder, folderNames, fileNames in os.walk(topFolder):
        if category == CategoryID.all or category == CategoryID.file:
            for fileName in fileNames:
                if nameMatcher and not nameMatcher(fileName):
                    continue
                filePath = os.path.join(parentFolder, fileName)
                if need_gettingStatus:
                    fileStatus = os.stat(filePath, follow_symlinks=False)
                    if sizeMinimum and fileStatus.st_size < sizeMinimum:
                        continue
                    if sizeMaximum and sizeMaximum < fileStatus.st_size:
                        continue
                    if isInvalidStatus_for_generic(fileStatus):
                        continue
                if dataMatcher:
                    try:
                        with open(filePath, "r", encoding=encoding) as fileHandle:
                            fileData = fileHandle.read()
                    except (UnicodeDecodeError, PermissionError):
                        continue
                    if not dataMatcher(fileData):
                        continue
                yield filePath
        if category == CategoryID.all or category == CategoryID.folder:
            for folderName in folderNames:
                if nameMatcher and not nameMatcher(folderName):
                    continue
                folderPath = os.path.join(parentFolder, folderName)
                if need_gettingStatus:
                    folderStatus = os.stat(folderPath, follow_symlinks=False)
                    if isInvalidStatus_for_generic(folderStatus):
                        continue
                yield folderPath
        if not deepSearch:
            break
def unique_path(path: pathlib.Path) -> pathlib.Path:
    if not path.exists():
        return path
    stem = path.stem
    suffix = path.suffix
    parent = path.parent
    n = 2
    while True:
        new_path = parent / f"{stem} ({n}){suffix}"
        if not new_path.exists():
            return new_path
        n += 1