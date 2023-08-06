import pandas as pd
import os
from datetime import datetime
from pandas.errors import EmptyDataError


class Pipero:
    TODAY = datetime.today().date()

    def __init__(self, file_list, delimiter=None, start_row=None, index=True):
        self.file_list = file_list
        self.frame = pd.DataFrame()
        self.frames = []
        self.extract_frames = []
        self.path = []
        self.delimiter = delimiter
        self.start_row = start_row
        self.headers = None
        self.errors = []
        self.index = not index

    @property
    def delimiter(self):
        return self._delimiter

    @delimiter.setter
    def delimiter(self, value):
        if value:
            value = value.strip()

        if not value:
            value = r"\s+"
        else:
            value = value
        self._delimiter = value

    @property
    def start_row(self):
        return self._start_row

    @start_row.setter
    def start_row(self, value):
        _value = int(value) if value else None
        self._start_row = _value

    def get_headers(self):
        if self.headers is not None:
            return self.headers
        else:
            self.load_data()
            self.headers = self.frame.columns
            return self.headers

    def load_data(self):
        for file in self.file_list:
            try:
                self.frame = pd.read_csv(file, delimiter=self.delimiter, skiprows=self.start_row)
            except EmptyDataError:
                file.seek(0)
                self.frame = pd.read_csv(file, delimiter=self.delimiter, skiprows=self.start_row)
            self.frames.append(self.frame)

    def extract_data(self, header_choice=None):
        h = header_choice if header_choice else None
        if not self.frames:
            self.load_data()
        for frame in self.frames:
            self.frame = frame.get(h, frame.get(frame.columns))
            self.extract_frames.append(self.frame)

    def save_data(self):
        if not self.extract_frames:
            self.extract_data(None)
        try:
            names = [os.path.splitext(os.path.split(x.name)[-1])[0] for x in self.file_list]
            directory = os.path.dirname(self.file_list[0].name)
        except AttributeError:
            names = [os.path.splitext(os.path.split(x)[-1])[0] for x in self.file_list]
            directory = os.path.dirname(self.file_list[0])
        if self.index:
            frames = [x.rename_axis("Index").reset_index() for x in self.extract_frames]
        else:
            frames = [x for x in self.extract_frames]
        out = pd.concat(frames, axis=1, keys=names)
        try:
            out.to_csv(
                os.path.join(
                    directory,
                    f"extracted_output_{self.TODAY}.csv",
                ),
                index=not self.index,
            )
        except PermissionError:
            self.errors.append('Unable to write to an open file')
