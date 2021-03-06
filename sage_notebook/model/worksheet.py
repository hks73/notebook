"""
Model for the Worksheet
"""




class Cell(object):

    def __init__(self, cell_id=None):
        if cell_id is None:
            import uuid
            self._id = uuid.uuid4().hex
        else:
            self._id = cell_id
        self._index = None
        self._input = ''
        self._busy = False
        self.clear_output()

    def __repr__(self):
        return 'Cell id {0}'.format(self.id)

    @property
    def id(self):
        return self._id
    
    @property
    def index(self):
        """
        Return the ``n`` in ``In[n]/Out[n]``
        
        OUTPUT:

        An integer or ``None``.
        """
        return self._index

    @index.setter
    def index(self, value):
        self._index = value
        
    def clear_output(self):
        self._index = None
        self._stdout = ''
        self._stderr = ''
        
    def accumulate_stdout(self, stdout):
        assert self._busy
        self._stdout += stdout

    def accumulate_stderr(self, stderr):
        assert self._busy
        self._stderr += stderr

    @property
    def busy(self):
        """
        Whether a computation is in progress
        """
        return self._busy
        
    @busy.setter
    def busy(self, value):
        self._busy = value
        if value is True:
            self.clear_output()

    @property
    def input(self):
        return self._input

    @input.setter
    def input(self, value):
        self._input = value

    @property
    def stdout(self):
        return self._stdout

    @property
    def stderr(self):
        return self._stderr

    def as_plain_text(self):
        result = self._stdout.rstrip()
        if len(self._stderr) > 0:
            result += self._stderr.rstrip()
        return result


class Worksheet(object):

    def __init__(self):
        self._cells_dict = dict()
        self._order = list()

    def __repr__(self):
        return 'Worksheet containing {0} cells'.format(self.n_cells())

    @classmethod
    def create_default(cls):
        ws = cls()
        c = Cell()
        c.input = '123'
        ws.append(c)
        c = Cell()
        c.input = '123^2'
        ws.append(c)
        c = Cell()
        c.input = 'def f(x):\n    return 1'
        ws.append(c)
        c = Cell()
        c.input = 'for i in range(10):  # test\n    print i\n    sleep(0.4)\n'
        ws.append(c)
        return ws
        
    def insert(self, pos, cell):
        self._cells_dict[cell.id] = cell
        self._order.insert(pos, cell.id)

    def append(self, cell):
        self.insert(self.n_cells(), cell)

    def index(self, cell):
        return self._order.index(cell.id)

    def delete(self, cell):
        del self._cells_dict[cell.id]
        self._order.remove(cell.id)
        if self.n_cells() == 0:
            self.append(Cell())

    def n_cells(self):
        return len(self._cells_dict)

    __len__ = n_cells

    def get_cell(self, cell_id):
        return self._cells_dict[cell_id]

    def __getitem__(self, i):
        cell_id = self._order[i]
        return self._cells_dict[cell_id]

    def __iter__(self):
        for cell_id in self._order:
            yield self._cells_dict[cell_id]
