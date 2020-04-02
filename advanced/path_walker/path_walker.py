import os

ROOT_PATH = r"C:\Users\SNIR-PC\Desktop\backup\snir\school&courses\python_playground\kumpus_course\6-Modules"


def recourse_files(root_path):
    """
    This func traverse from the root_path over the filesystem tree,
    and print the names of all files in the same tree.
    :param root_path = The path from which the filesystem tree starts.
    """
    check_path_name(root_path)

    if os.path.isfile(root_path):
        print(root_path)

    only_files_lst = [f for f in os.listdir(root_path) if os.path.isfile(os.path.join(root_path, f))]
    only_dir_lst = [d for d in os.listdir(root_path) if os.path.isdir(os.path.join(root_path, d))]

    for file in only_files_lst:
        print(os.path.join(root_path, file))

    for dir_ in only_dir_lst:
        recourse_files(os.path.join(root_path, dir_))


def check_path_name(path_name):
    """
    Checks if the path_name is a valid path.
    :raise TypeError or FileNotFoundError otherwise.
    """
    if type(path_name) != str:
        raise TypeError("file or directory can't be a '%s' object" % path_name.__class__.__name__)

    elif not os.path.isfile(path_name) and not os.path.isdir(path_name):
        raise FileNotFoundError("The system cannot find the path specified. " + path_name)


class PathWalker:
    """
    Class that represent a path name.
    """
    def __init__(self, path_name):
        """
        Initialize method, sets the path_name.
        :param path_name: A path of a file or directory, str object.
        """
        self._path_name = path_name
        self._check_input()

    def _check_input(self):
        """
        Checks if the path_name is a valid path.
        :raise TypeError or FileNotFoundError otherwise.
        """
        if type(self._path_name) != str:
            raise TypeError("file or directory can't be a '%s' object" % self._path_name.__class__.__name__)

        elif not os.path.isfile(self._path_name) and not os.path.isdir(self._path_name):
            raise FileNotFoundError("The system cannot find the path specified. " + self._path_name)

    def __str__(self):
        """
        :return: A str presentation of the path_name.
        """
        return self._path_name

    def __repr__(self):
        """
        :return: A str presentation of the path_name, in this format: PathWalker('path_name').
        """
        return r"PathWalker('%s')" % self._path_name

    def __getitem__(self, item="."):
        """
        :param item: String object - file name in the self._path_name directory.
        Item also could be '.' - represent the self._path_name or ".." that represent the former folder.
        :raise TypeError or ValueError otherwise.
        """
        if item == ".":
            return self

        elif item == "..":
            return PathWalker(os.path.dirname(self._path_name))

        elif item in os.listdir(self._path_name):
            return PathWalker(os.path.join(self._path_name, item))

        elif type(item) != str:
            raise TypeError("file or directory can't be a '%s' object" % item.__class__.__name__)

        else:
            raise ValueError("The system cannot find the path specified. " + os.path.join(self._path_name, item))

    def __iter__(self):
        return iter([PathWalker(os.path.join(self._path_name, f)) for f in os.listdir(self._path_name)])

    def get_path(self):
        """
        :return: the self._path_name
        """
        return self._path_name

    def recourse_files(self):
        """
        This func traverse from the self._path_name over the filesystem tree,
        and print the names of all files in the same tree.
        """
        if os.path.isfile(self._path_name):
            print(self._path_name)

        for sub_walker in self:
            if os.path.isfile(sub_walker._path_name):
                print(sub_walker._path_name)
            else:
                sub_walker.recourse_files()


def main():

    recourse_files(ROOT_PATH)
    # walker = PathWalker(ROOT_PATH)
    # recourse_files(walker)
    # print(repr(walker))
    # print(walker)
    # print(repr(walker["drawing_photo.jpg"]))
    # print(repr(walker[".."]))
    # print(repr(walker["."]))
    #
    # for subwalker in walker:
    #     print(subwalker)
    # walker.recourse_files()


if __name__ == '__main__':
    main()
