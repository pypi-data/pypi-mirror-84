import os
import lmdb
import pandas as pd
import pyarrow as pa
import numpy as np
import cv2
from torch.utils import data

from typing import Union


class FileBackend:

    def __init__(self, root_folder: str):
        self.root_folder = root_folder

    def retreive(self, key: str, decoder: str = 'raw'):
        full_name = os.path.join(self.root_folder, key)

        if(decoder == 'image_color'):
            return cv2.imread(full_name, cv2.IMREAD_COLOR)
        elif(decoder == 'image_gray'):
            return cv2.imread(full_name, cv2.IMREAD_GRAYSCALE)
        elif(decoder == 'video'):
            cap = cv2.VideoCapture(full_name)
            frame_list = []
            while(cap.isOpened()):
                ret, frame = cap.read()
                if(ret is False):
                    break
                frame_list.append(frame)
            video_frames = np.stack(frame_list, axis=0)
            return video_frames
        elif(decoder == 'numpy'):
            return np.load(full_name)
        else:
            # Return raw byte
            with open(full_name, 'rb') as f:
                byteflow = f.read()
            return byteflow


class LMDBBackend:

    def __init__(self, lmdb_path: str):
        self.lmdb_path = lmdb_path
        self.env = lmdb.open(lmdb_path, subdir=os.path.isdir(lmdb_path),
                             readonly=True, lock=False,
                             readahead=False, meminit=False)

        with self.env.begin(write=False) as txn:
            self.length = pa.deserialize(txn.get(b'__len__'))
            self.keys = pa.deserialize(txn.get(b'__keys__'))

    def retreive(self, key: str, decoder: str = 'raw'):
        with self.env.begin(write=False) as txn:
            byteflow = txn.get(key)
        unpacked = pa.deserialize(byteflow)

        if(decoder == 'image_color'):
            return cv2.imdecode(np.fromstring(unpacked, np.uint8), cv2.IMREAD_COLOR)
        elif(decoder == 'image_gray'):
            return cv2.imdecode(np.fromstring(unpacked, np.uint8), cv2.IMREAD_GRAYSCALE)
        elif(decoder == 'video'):
            tmp_full_path = self._write_to_tmp(key, unpacked)
            cap = cv2.VideoCapture(tmp_full_path)
            frame_list = []
            while(cap.isOpened()):
                ret, frame = cap.read()
                if(ret is False):
                    break
                frame_list.append(frame)
            video_frames = np.stack(frame_list, axis=0)
            os.remove(tmp_full_path)
            return video_frames
        else:
            # Unlike filebackend, assume numpy arrays have been serialized by pyarrow
            # So we can directly return.
            return unpacked

    def _write_to_tmp(self, key, byteflow):
        tmp_name = '_'.join(key.split(os.sep))
        tmp_full_path = os.path.join('/dev/shm', tmp_name)
        with open(tmp_full_path, 'wb') as f:
            f.write(byteflow)
        return tmp_full_path


# A general dataset class.
# The data items are managed by CSV file,
# while the raw data can be saved either as folder of small files (convinent but slow)
# or packed as one LMDB (fast but hard to debug).
# This class hides the details inside so users can seamlessly switch between
# folder backend and lmdb backend.
class GeneralDataset(data.Dataset):

    @staticmethod
    # Filter csv via pandas engine.
    def filter_csv(csv, query):
        df = pd.read_csv(csv)
        bn = os.path.basename(csv)
        if query == 'none':
            print('Loaded %d rows from %s.' % (len(df), bn))
        else:
            full_len = len(df)
            df = df.query(query, engine='python')
            print('Loaded %d/%d rows from %s using <%s>.' % (len(df), full_len, bn, query))
        return df

    def __init__(self, root_folder_or_lmdb_path: str,
                 dataframe_or_csv_path: Union[pd.DataFrame, str],
                 csv_query: str = 'none',
                 backend: str = 'folder'):
        # Initialize backend
        if(backend == 'folder'):
            self.data_backend = FileBackend(root_folder_or_lmdb_path)
        elif(backend == 'lmdb'):
            self.data_backend = LMDBBackend(root_folder_or_lmdb_path)
        else:
            raise NotImplementedError("Backend not supported.")

        # Load csv
        if(isinstance(dataframe_or_csv_path, str)):
            self.df = self.filter_csv(dataframe_or_csv_path, csv_query)
        else:
            self.df = dataframe_or_csv_path

    def __len__(self):
        return len(self.df)

    def get_csv_row(self, position):
        return self.df.iloc[position]

    def retreive(self, key: str, decoder: str = 'raw'):
        return self.data_backend.retreive(key, decoder)

    def __getitem__(self, position):
        raise NotImplementedError("Please implement in inherited class!")
