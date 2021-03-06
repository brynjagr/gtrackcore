from gtrackcore.track.core.VirtualNumpyArray import VirtualNumpyArray


class VirtualTrackColumn(VirtualNumpyArray):

    def __init__(self, array_node_names, db_reader, start_index=-1, end_index=-1):
        VirtualNumpyArray.__init__(self)

        self._db_reader = db_reader
        self._array_node_names = array_node_names
        self._start_index = start_index
        self._end_index = end_index
        self._step = 1

        self._db_reader.open()
        array = self._db_reader.get_node(self._array_node_names)
        self._shape = array.shape
        self._dtype = array.dtype
        self._db_reader.close()

    @property
    def offset(self):
        return self._start_index, self._end_index

    @offset.setter
    def offset(self, start_end_tuple):
        self._set_offset(start_end_tuple[0], start_end_tuple[1])

    def _set_offset(self, start_index, end_index, step=1):
        assert start_index <= end_index

        if self._cachedNumpyArray is not None:
            if start_index >= self._start_index and end_index <= self._end_index:
                self._cachedNumpyArray = self._cachedNumpyArray[start_index:end_index:step]
            else:
                self._cachedNumpyArray = None

        self._start_index = start_index
        self._end_index = end_index
        self._step = step

    @property
    def shape(self):
        return self._shape

    @property
    def dtype(self):
        return self._dtype

    @property
    def filename(self):
        raise NotImplementedError

    def update_offset(self, start=None, stop=None, step=None):
        if self._start_index == self._end_index:
            return

        if start is not None:
            if start >= 0:
                start_index = self._start_index + start
            else:
                start_index = self._end_index + start
        else:
            start_index = self._start_index

        if stop is not None:
            if stop >= 0:
                end_index = self._start_index + stop
            else:
                end_index = self._end_index + stop
        else:
            end_index = self._end_index

        step = step if step is not None else 1

        self._set_offset(start_index, end_index, step)

    def __copy__(self):
        vtc = VirtualTrackColumn(self._array_node_names, self._db_reader, self._start_index, self._end_index)
        vtc._cachedNumpyArray = self._cachedNumpyArray
        return vtc

    def __len__(self):
        return self._end_index - self._start_index

    def as_numpy_array(self):
        self._db_reader.open()
        array = self._db_reader.get_node(self._array_node_names)
        result = array[self._start_index:self._end_index:self._step]
        self._db_reader.close()
        return result

    def ends_as_numpy_array_points_func(self):
        """
        Used for points tracks for ends (== starts + 1)
        """
        self._db_reader.open()
        array = self._db_reader.get_node(self._array_node_names)
        result = array[self._start_index:self._end_index:self._step] + 1
        self._db_reader.close()
        return result
