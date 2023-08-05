from django.core.files.storage import FileSystemStorage
from django.conf import settings

from .exception import AVException
from .scanner import AVScanner

av_scanner = AVScanner()

USE_SCANNER = settings.ANTIVIRUS_ENABLED if hasattr(settings, 'ANTIVIRUS_ENABLED') else True


class AVFileSystemStorage(FileSystemStorage):
    parallel = True

    def save(self, name, content, max_length=None):
        if USE_SCANNER:
            av_result = av_scanner.has_virus(content, parallel=self.parallel)
            if av_result[0] is False:
                return super().save(name, content, max_length)
            raise AVException(av_result[1])
        else:
            return super().save(name, content, max_length)


class SingleCoreAVFileSystemStorage(AVFileSystemStorage):
    """
    Same as AVFileSystemStorage, but doesn't run multiple scanners in parallel
    """
    parallel = False
