from pathlib import Path
from typing import List
import re


IMPORT_PATTERN = r"`import\s+\"(\w+.lfr)\""


class PreProcessor(object):

    def __init__(self, file_list: List[str]) -> None:
        self.resolved_paths = dict()
        self.text_dump = None
        for file_path in file_list:

            extension = Path(file_path).suffix
            if extension != '.lfr':
                print("Unrecognized file Extension")
                exit()

            p = Path(file_path).resolve()
            print("Input Path: {0}".format(p))
            # Open a file: file
            file = open(p, mode='r')

            # read all lines at once
            all_of_it = file.read()

            # close the file
            file.close()

            self.resolved_paths[p.name] = all_of_it

    def process(self) -> None:
        # TODO - Go through the files and then replace
        # each of the individual files and them replace
        # it whereever you see an import statement
        text = " blah \n`import \"test.lfr\" \n blah"
        find_results = re.findall(IMPORT_PATTERN, text)
        for result in find_results:
            if result in self.resolved_paths.keys():
                pass
        print(find_results)
        pass
