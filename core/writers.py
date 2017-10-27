import csv


class TimeValueLogger:
    def __init__(self, path):
        self._csvfile = open(path, 'w')
        self._csvwriter = csv.writer(self._csvfile, delimiter=' ')

    def log(self, time: float, value: float):
        self._csvwriter.writerow([time, value])

    def complete(self):
        self._csvfile.close()

        del self._csvwriter
        del self._csvfile
