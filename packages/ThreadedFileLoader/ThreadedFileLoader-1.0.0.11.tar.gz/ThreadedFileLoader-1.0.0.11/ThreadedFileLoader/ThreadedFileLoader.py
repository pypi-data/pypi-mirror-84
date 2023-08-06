from threading import Thread
import imageio
import glob
import time


class ThreadedFileLoader:
    """
    Class to load files via threading.
    Usage:
    =====
    Overload the `self.object_loader` for customized file type.
    """

    def __init__(self, folder_path_glob):
        self.loaded_objects = []
        self.file_paths = self.glob_resolver(folder_path_glob)

    def glob_resolver(self, path_glob):
        return glob.glob(path_glob)

    def object_loader(self, path):
        return imageio.imread(path)

    def loading_function(self, path):
        image = self.object_loader(path)
        self.loaded_objects.append(image)

    def __thread_worker(self):
        for i, file_path in enumerate(self.file_paths):
            Thread(target=self.loading_function(file_path)).start()

    def batched_thread_worker(self, batch_size, delay):
        """
        This function waits `delay` seconds after every batch for the
        previous threads to start finish it's work.
        In case start_loading gives max thread error use this.

        """
        for i, file_path in enumerate(self.file_paths):
            Thread(target=self.loading_function(file_path)).start()
            if i % batch_size == 0:
                time.sleep(delay)

    def start_loading(self):
        self.__thread_worker()


class ThreadedImageLoader(ThreadedFileLoader):
    def object_loader(self, path):
        print(path)
        return imageio.imread(path)


class ThreadedTextLoader(ThreadedFileLoader):
    def object_loader(self, path):
        with open(path) as afile:
            return afile.readlines()

