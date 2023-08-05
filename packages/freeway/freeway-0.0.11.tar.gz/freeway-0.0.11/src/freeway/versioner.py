# cython: language_level=2, boundscheck=False
import os
import re
import fnmatch
from .errors import (NoValidVersion, NoVersionNumber, 
                     VersionZero, ExceededPaddingVersion)

regex_splits = '(?P<head>.*%s)(?P<version>[0-9]+)(?P<tail>[.]%s)'


class BaseVersion(object):
    def __init__(self, filename, pads=3, postfix='.v', ext='.*'):
        if isinstance(filename, str):
            self.filename = filename
        elif isinstance(filename, Version) or isinstance(filename, VersionFileSystem):
            self.filename = filename.filename
            pads = filename.pads
            postfix = filename.postfix
            ext = filename.ext
        else:
            raise TypeError

        self.postfix = postfix
        self.pads = pads
        extension = os.path.splitext(self.filename)[-1]
        self.ext = extension[1:] if extension else ext
        self.regex_splits = re.compile(regex_splits % (self.postfix, self.ext))
        self.head, self.version, self.tail = self._splits(self.filename)

    def __str__(self):
        return str(self.filename)

    def __repr__(self):
        return str(self.filename)

    def __eq__(self, version):
        if isinstance(version, str):
            return self.current == Version(version).current
        elif isinstance(version, int):
            return self.current == version
        elif isinstance(version, Version):
            return self.current == version.current
        raise TypeError

    @staticmethod
    def int_to_pad(pads, number):
        return ('%s%sd' % ('%0', '%d' % pads)) % number

    def _splits(self, filename):
        info = [match.groupdict()
                for match in self.regex_splits.finditer(filename)]
        if info:
            return info[0]['head'], info[0]['version'], info[0]['tail']
        else:
            try:
                return [filename[:filename.rindex('.')],
                        None,
                        filename[filename.rindex('.'):]]
            except ValueError:
                return [None, None, None]

    def _current(self, path):
        try:
            return int(self.version)
        except Exception:
            return None

    @property
    def current(self):
        return self._current(self.filename)

    @property
    def isVersionless(self):
        return not self.version

    def to(self, version):
        version = self.int_to_pad(int(self.pads), int(version))

        if self.isVersionless:
            self.filename = '%s%s%s%s' % (self.head, self.postfix,
                                          version, self.tail)
        else:
            self.filename = '%s%s%s' % (self.head, version, self.tail)

        return self.__class__(self)

    @property
    def versionless(self):
        try:
            if not self.tail:
                return self.head
            else:
                if not self.isVersionless:
                    filename = self.head[:len(self.postfix) * -1]
                    return Version('%s%s' % (filename, self.tail))
                else:
                    return Version('%s%s' % (self.head, self.tail))
        except Exception:
            raise NoValidVersion


class Version(BaseVersion):
    @property
    def next(self):
        if not self.current:
            return None

        if self.current + 1 <= int(self.pads * '9'):
            return self.to(self.current + 1)
        else:
            raise ExceededPaddingVersion

    @property
    def previous(self):
        version = self.current
        if not version:
            return None

        elif version > 1:
            return self.to(self.current - 1)

        elif version == 1:
            raise VersionZero

    @property
    def fs(self):
        return VersionFileSystem(self)


class VersionFileSystem(BaseVersion):
    def __init__(self, filename, pads=3, postfix='.v', ext='.*'):
        if isinstance(filename, str):
            self.filename = filename
        elif isinstance(filename, Version) or isinstance(filename, VersionFileSystem):
            self.filename = filename.filename
            pads = filename.pads
            postfix = filename.postfix
            ext = filename.ext
        else:
            raise TypeError

        if os.path.exists(self.filename) and not os.path.isabs(self.filename):
            self.filename = '/'.join([os.getcwd(), self.filename])
        
        # Python3.x
        #super().__init__(str(self.filename), pads=pads, postfix=postfix, ext=ext)
        super(VersionFileSystem, self).__init__(str(self.filename), pads=pads, postfix=postfix, ext=ext)


    def __iter__(self):
        dirname, basename = os.path.split(self.head)

        for root, dirnames, filenames in os.walk(dirname):
            for filename in sorted(fnmatch.filter(filenames, basename + '*')):
                yield VersionFileSystem('/'.join([root, filename]))


    def __contains__(self, version):
        return VersionFileSystem(self).to(version).exists

    def __next__(self):
        vers = list(self)
        current = self.current
        while vers:
            if current == vers.pop(0):
                try:
                    return vers.pop(0)
                except IndexError:
                    return None

    def __previous__(self):
        vers = list(self)
        current = self.current
        while vers:
            if current == vers.pop():
                try:
                    return vers.pop()
                except IndexError:
                    return None

    @property
    def first(self):
        for ver in self:
            return ver

    @property
    def last(self):
        old = 0
        last = None
        for ver in self:
            try:
                new = ver.current
                if new and old <= new:
                    old = new
                    last = ver
            except NoVersionNumber:
                pass

        return last

    @property
    def next(self):
        return self.__next__()

    @property
    def previous(self):
        return self.__previous__()

    @property
    def exists(self):
        return os.path.exists(self.filename)
