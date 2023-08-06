from sitepipes import config
from sitepipes.datasets.meta import MetaDataset

from abc import abstractmethod

import logging
import os


class Dataset(metaclass=MetaDataset):
    """ A parent class for all data that flows between components """

    name = None

    _schema = []
    _df_history = []

    def __init__(self):
        pass

    def __eq__(self, other):
        if type(self) == type(other) and self.name == other.name:
            return True
        return False

    def __hash__(self):
        return hash(self.name)

    def __len__(self):
        return len(self.df)

    def __call__(self, *args, **kwargs):
        pass

    @abstractmethod
    def load_dataset(self):
        """ Loads a DataFrame into a predefined schema for a given dataset """
        if self._cols:
            assert self.df.cols == self._schema

    @abstractmethod
    def preprocess_dataset(self):
        """ Preprocesses a dataset """
        pass

    @property
    def df(self):
        """ Maintains a history of the DataFrame at each processing step """
        if len(self._df_history) > 0:
            return self._df_history[-1]
        return None

    @df.setter
    def df(self, dataframe):
        self._df_history.append(dataframe)

    def save_dataset(self, path, save_history=False, index_col=0):
        """
        Saves the current state of the DataFrame to path

        :param path: str - Path to save the DataFrame
        :param save_history: - Whether to save all histories of DataFrame
        :param index_col: int/str - Designation for index column in DataFrame
        :return: Saves the DataFrame(s) to disk
        """
        if save_history:
            filename, file_extension = os.path.splitext(path)
            for i, df in enumerate(self._df_history):
                logging.info(f'Saving DataFrame {i}/{len(self._df_history)} from {self.__name__} to path={path}...')
                path_i = f'{filename}-{i}{file_extension}'
                df.to_csv(path_i, index_col=index_col)
        else:
            logging.info(f'Saving DataFrame from {self.__name__} to path={path}...')
            self.df.to_csv(path, index_col=index_col)

    def downsample(self, n, balance_classes=False, do_random=False):
        """
        Selects N samples from self.df

        :param n: int - Number of samples to keep
        :param balance_classes: bool - Whether to balance classes
        :param do_random: bool - Whether to select randomly
        :return: Modifies self.df in-place
        """

        if balance_classes:
            logging.info(f'Downsampling {self.__name__} dataset with {n} balanced class samples...')
        elif do_random:
            logging.info(f'Downsampling {self.__name__} dataset with {n} random samples...')
            self.df = self.df.sample(n=n, random_state=config['seed'])
        else:
            logging.info(f'Downsampling {self.__name__} dataset with first {n} samples...')
            self.df = self.df[:n]
