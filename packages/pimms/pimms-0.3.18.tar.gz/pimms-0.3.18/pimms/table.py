####################################################################################################
# pimms/table.py
# Classes for storing immutable data tables.
# By Noah C. Benson

import copy, types, sys, pint, six
import numpy                      as     np
import pyrsistent                 as     ps
from   functools                  import reduce
from   .util                      import (merge, is_pmap, is_map, LazyPMap, lazy_map, is_lazy_map,
                                          is_quantity, is_unit, is_str, is_int, is_vector,
                                          quant, iquant, mag, unit, qhash, units, imm_array,
                                          getargspec_py27like)
from   .immutable                 import (immutable, value, param, require, option)

if sys.version_info[0] == 3: from   collections import abc as colls
else:                        import collections            as colls

def _ndarray_assoc(arr, k, v):
    '_ndarray_assoc(arr, k, v) duplicates arr to a writeable array, sets arr2[k]=v, returns arr2'
    arr = np.array(arr)
    arr[k] = v
    arr.setflags(write=False)
    return arr    

class ITableRow(colls.Mapping):
    '''
    ITableRow is a class that works with the ITable class to quickly and lazily allow access to
    individual rows as if they were individual persistent maps. For all intents and purposes, an
    ITableRow object should be treated as a dict object that cannot be changed.
    Note that ITableRow is not an immutable class, but its members cannot be changed. The class
    is intended as a hidden subclass that is very efficient.
    '''
    def __init__(self, data, colnames, rownum):
        object.__setattr__(self, 'data',         data)
        object.__setattr__(self, 'column_names', colnames)
        object.__setattr__(self, 'row_number',   rownum)
    def keys(self):
        return self.column_names
    def __setattr__(self, k, v):
        raise RuntimeError('ITableRow object is immutable')
    def __getitem__(self, key):
        return self.data[key][self.row_number]
    def __setitem__(self, key, value):
        raise RuntimeError('Cannot set row of immutable table')
    def __delitem__(self, key):
        raise RuntimeError('Cannot set row of immutable table')
    def __iter__(self):
        dat = self.data
        n = self.row_number
        for col in self.column_names:
            yield col
    def __len__(self):
        return len(self.column_names)
    def asdict(self):
        return {k:self.data[k][self.row_number] for k in self.__iter__()}
    def aspmap(self):
        return ps.pmap(self.asdict())
    def __repr__(self):
        return repr(self.asdict())
    def __hash__(self):
        return hash(self.aspmap())

@immutable
class ITable(colls.Mapping):
    '''
    The ITable class is a simple immutable datatable.
    '''
    def __init__(self, data, n=None):
        self.data = data
        self._row_count = n
    def __hash__(self):
        # we want to make sure arrays are immutable
        return qhash(self.data)
    def __getstate__(self):
        d = self.__dict__.copy()
        d['data'] = {k:(mag(v), unit(v)) if is_quantity(v) else (v, None)
                     for (k,v) in six.iteritems(self.data)}
        return d
    def __setstate__(self, d):
        dat = d['data']
        object.__setattr__(self, 'data',
                           ps.pmap({k:(imm_array(u) if v is None else iquant(u, v))
                                    for (k,(u,v)) in six.iteritems(dat)}))
        object.__setattr__(self, '_row_count', None)
    @staticmethod
    def _filter_col(vec):
        '_filter_col(vec) yields a read-only numpy array version of the given column vector'
        if isinstance(vec, types.FunctionType) and getargspec_py27like(vec)[0] == []:
            return lambda:ITable._filter_col(vec())
        elif is_quantity(vec):
            m = mag(vec)
            mm = ITable._filter_col(m)
            return vec if m is mm else quant(mm, unit(vec))
        else:
            return imm_array(vec)
    @param
    def data(d):
        '''
        itbl.data is an immutable map of the given itable in which property names are associated
        with their data vectors.
        '''
        # we want to check these values and clean them up as we go, but if this is a lazy map, we
        # want to do that lazily...
        if is_map(d):
            if not is_lazy_map(d): d = lazy_map(d)
            def _make_lambda(k): return (lambda:ITable._filter_col(d[k]))
            return lazy_map(
                {k:_make_lambda(k) if d.is_lazy(k) else ITable._filter_col(d[k])
                 for k in six.iterkeys(d)})
        else:
            raise ValueError('Unable to interpret data argument; must be a mapping')
    @param
    def _row_count(n):
        '''
        itbl._row_count is the row count, as provided by internal methods when the row count can be
        known ahead of time. It should not geberally be used; use itbl.row_count instead.
        '''
        return n
    @require
    def validate_data(data):
        '''
        ITable data is required to be a PMap with keys that are strings.
        '''
        if not isinstance(data, ps.PMap):
            raise ValueError('data is required to be a persistent map')
        if not all(isinstance(k, six.string_types) for k in six.iterkeys(data)):
            raise ValueError('data keys must be strings')
        return True
    @require
    def validate_row_count(_row_count):
        '''
        ITable _row_count must be a non-negative integer or None.
        '''
        if _row_count is None: return True
        else: return is_int(_row_count) and _row_count >= 0
    @value
    def column_names(data):
        '''
        itbl.column_names is a tuple of the names of the columns of the data table.
        '''
        return tuple(six.iterkeys(data))
    @value
    def row_count(data, _row_count):
        '''
        itbl.row_count is the number of rows in the given datatable itbl.
        '''
        if len(data) == 0:
            return 0
        elif _row_count:
            return _row_count
        elif is_lazy_map(data):
            # if data is a lazy map, we look first for a column that isn't lazy:
            k = next(data.iternormal(), None)
            k = k if k else next(data.itermemoized(), None)
            k = k if k else next(data.iterkeys())
            return len(data[k])
        else:
            return len(next(six.itervalues(data), []))
    @value
    def columns(data, row_count):
        '''
        itbl.columns is a tuple of the columns in the given datatable itbl. Anything that depends on
        columns includes a de-facto check that all columns are the same length.
        '''
        cols = tuple(v for v in six.itervalues(data))
        if not all(len(c) == row_count for c in cols):
            raise ValueError('itable columns do not all have identical lengths!')
        return cols
    @value
    def rows(data, row_count, column_names):
        '''
        itbl.rows is a tuple of all the persistent maps that makeup the rows of the data table.
        '''
        return tuple([ITableRow(data, column_names, i) for i in range(row_count)])
    @value
    def dataframe(data):
        '''
        itbl.dataframe is a pandas dataframe object that is equivalent to the given itable. Note
          you must have pandas installed for this to work; an exception will be raised when this
          value is requested if you do not.
        '''
        import pandas
        return pandas.DataFrame.from_dict(dict(data))
    # Methods
    def set(self, k, v):
        '''
        itbl.set(name, val) yields a new itable object identical to the given itbl except that it
          includes the vector val under the given column name.
        itbl.set(row, map) updates just the given row to have the properties in the given map; if
          this results in a new column being added, it will have the value None for all other rows.
        itbl.set(rows, m) allows a sequence of rows to be set by passing rows as either a list or
          slice; m may also be a single map or a sequence of maps whose size matches that of rows.
          Alternately, m may be an itable whose row-size matches that of rows; in this case new
          column names may again be added.
        '''
        dat = self.data
        if isinstance(k, six.string_types):
            if isinstance(v, (ITable, colls.Mapping)): v = v[k]
            v = self._filter_col(v)
            new_data = self.data.set(k, v)
            return ITable(new_data, n=len(v))
        elif is_int(k):
            # This is an awful slow way to do things
            def _make_lambda(k):
                return lambda:_ndarray_assoc(dat[k], k, v[k]) if k in v else dat[k]
            new_map = {k:_make_lambda(k) for k in six.iterkeys(dat)}
            nones = np.full((self.row_count,), None)
            for (vk,v) in six.iteritems(v):
                if vk not in new_map:
                    new_map[vk] = _ndarray_assoc(nones, k, v)
            return ITable(lazy_map(new_map), n=self.row_count)
        elif not k:
            return self
        elif isinstance(k[0], six.string_types):
            nones = np.full((self.row_count,), None)
            newdat = self.data
            if isinstance(v, ITable):
                def _make_lambda(k): return (lambda:self._filter_col(v[kk]))
                v = lazy_map({kk:_make_lambda(kk) for kk in k})
            elif not isinstance(v, colls.Mapping):
                v = np.asarray(v)
                if len(v) == self.row_count and v.shape[1] == len(k): v = v.T
                v = {kk:self._filter_col(vv) for (kk,vv) in zip(k,v)}
            for kk in six.iterkeys(v):
                def _make_lambda(k): return (lambda:self._filter_col(v[kk]))
                newdat = newdat.set(kk, _make_lambda(kk) if kk in v else nones)
            return ITable(newdat, n=self.row_count)
        else:
            (keys, vals) = (k,v)
            dat = self.data
            nones = np.full((self.row_count,), None)
            knones = np.full((len(keys),), None)
            if isinstance(vals, (ITable, colls.Mapping)):
                def _make_lambda(k):
                    return lambda:_ndarray_assoc(
                        dat[k] if k in dat else nones,
                        keys,
                        vals[k] if k in vals else knones)
                dat = reduce(
                    lambda m,k: m.set(k, _make_lambda(k)),
                    six.iteritems(vals.data if isinstance(vals, ITable) else vals),
                    dat)
            else:
                def _make_lambda(k): return lambda:np.asarray([v[k] for v in vals])
                cols = lazy_map({k:_make_lambda(k) for k in six.iterkeys(vals[0])})
                def _make_lambda(k):
                    return lambda:_ndarray_assoc(
                        dat[k] if k in dat else nones,
                        keys,
                        cols[k])
                dat = reduce(
                    lambda m,k: m.set(k, _make_lambda(k)),
                    six.iterkeys(vals[0]),
                    dat)
            return ITable(dat, n=self.row_count)
    def discard(self, cols):
        '''
        itbl.discard(arg) discards either the list of rows, given as ingtegers, or the list of
          columns, given as strings.
        '''
        if not cols: return self
        dat = self.data
        vecq = is_vector(cols)
        if is_str(cols) or (vecq and len(cols) > 0 and is_str(cols[0])):
            cols = set(cols if vecq else [cols])
            def _make_lambda(k): return lambda:dat[k]
            return ITable(lazy_map({k:_make_lambda(k) for k in six.iterkeys(dat) if k not in cols}),
                          n=self.row_count)
        elif isinstance(cols, slice) or is_int(cols) or \
             (vecq and len(cols) > 0 and is_int(cols[0])):
            def _make_lambda(k): return lambda:np.delete(dat[k], cols, 0)
            newdat = lazy_map({k:_make_lambda(k) for k in six.iterkeys(dat)})
            return ITable(newdat, n=len(np.delete(np.ones((self.row_count,)), cols, 0)))
        elif vecq and len(cols) == 0: return self
        else: raise ValueError('ITable.discard requires integers or strings')
    def is_lazy(self, k):
        '''
        itable.is_lazy(k) yields True if k is a lazy value in the given itable, as in a lazy map.
        '''
        return self.data.is_lazy(k)
    def is_memoized(self, k):
        '''
        itable.is_memoized(k) yields True if k is a memoized value in the given itable, as in a lazy
          map.
        '''
        return self.data.is_memoized(k)
    def is_normal(self, k):
        '''
        itable.is_normal(k) yields True if k is a normal value in the given itable, as in a lazy
          map.
        '''
        return self.data.is_normal(k)
    def iterkeys(self):
        return self.data.iterkeys()
    def iteritems(self):
        return self.data.iteritems()
    def iterlazy(self):
        '''
        itable.iterlazy() yields an iterator over the lazy keys only (memoized lazy keys are not
          considered lazy).
        '''
        return self.data.iterlazy()
    def itermemoized(self):
        '''
        itable.itermemoized() yields an iterator over the memoized keys only (neihter unmemoized
          lazy keys nor normal keys are considered memoized).
        '''
        return self.data.itermemoized()
    def iternormal(self):
        '''
        itable.iternormal() yields an iterator over the normal unlazy keys only (memoized lazy keys
          are not considered normal).
        '''
        return self.data.iternormal()
    def map(self, f):
        '''
        itbl.map(f) yields the result of mapping the rows of the given datatable itbl over the
          given function f.
        '''
        if isinstance(f, six.string_types) and f in self.data: return self.data[f]
        (args, vargs, kwargs, dflts) = getargspec_py27like(f)
        dflts = dflts if dflts else ()
        dflts = tuple([None for _ in range(len(args) - len(dflts))]) + dflts
        # we have to decide what to map over...
        return map(f, self.rows)
    def where(self, f):
        '''
        itbl.where(f) yields the indices for which itbl.map(f) yields True.
        '''
        return [i for (i,v) in enumerate(self.map(f)) if v]
    def select(self, arg):
        '''
        itbl.select(idcs) yields a sub-table in which only the rows indicated by the given list of
          indices are kept.
        itbl.select(f) keeps all rows for which the function f yields True.
        '''
        if isinstance(arg, types.FunctionType):
            arg = self.where(arg)
        else:
            n = len(arg)
            if n == self.row_count and set(arg) == set([0,1]):
                arg = [i for (i,b) in enumerate(arg) if b]
                n = len(arg)
            dat = self.data
            def _make_lambda(k): return lambda:dat[k][arg]
            return ITable(
                lazy_map({k:_make_lambda(k) for k in six.iterkeys(dat)}),
                n=n)
    def merge(self, *args, **kwargs):
        '''
        itbl.merge(...) yields a copy of the ITable object itbl that has been merged left-to-right
          with the given arguments.
        '''
        return itable(self.data, *args, **kwargs).persist()
    def __getitem__(self, rows, cols=Ellipsis):
        '''
        itbl[row_number] yields the map associated with the given row in the ITable object itbl; the
          row_number may alternately be a slice.
        itbl[[r1, r2...]] yields a duplicate itable containing only the given rows of itbl.
        itbl[column_name] yields the numpy array associated with the given column name.
        itbl[[c1, c2...]] yields a duplicate itable containing only the given columns of itbl.
        itbl[rows, cols] is equivalent to itbl[rows][cols] (in fact, rows and cols may be given in
          any order).
        '''
        if cols is not Ellipsis: return self[rows][cols]
        if is_int(rows):
            return self.rows[rows]
        elif isinstance(rows, six.string_types):
            return self.data[rows]
        elif rows is None or len(rows) == 0:
            return ITable(ps.m(), n=0)
        elif isinstance(rows, slice) or is_int(rows[0]):
            n = len(range(rows.start, rows.stop, rows.step)) if isinstance(rows, slice) else \
                len(rows)
            dat = self.data
            def _make_lambda(dat,k): return lambda:dat[k][rows]
            return ITable(
                lazy_map({k:_make_lambda(dat,k) for k in six.iterkeys(dat)}),
                n=n)
        else:
            rows = set(rows)
            dat = self.data
            return ITable(
                reduce(lambda m,k: m if k in rows else m.remove(k), six.iterkeys(dat), dat),
                n=self.row_count)
    def __repr__(self):
        return 'itable(%s, <%d rows>)' % (self.column_names, self.row_count)
    def __iter__(self):
        return six.iterkeys(self.data)
    def __len__(self):
        return len(self.data)
    def __contains__(self, k):
        return ((0 <= k < self.row_count) if is_int(k)  else
                (k in self.data)          if isinstance(k, six.string_types)   else
                False)
    def iterrows(self):
        '''
        itbl.iterrows() iterates over the rows of the givan itable itbl.
        '''
        return iter(self.rows)
def itable(*args, **kwargs):
    '''
    itable(...) yields a new immutable table object from the given set of arguments. The arguments
      may be any number of maps or itables followed by any number of keyword arguments. All the
      entries from the arguments and keywords are collapsed left-to-right (respecting laziness),
      and the resulting column set is returned as the itable. Arguments and maps may contain
      values that are functions of zero arguments; these are considered lazy values and are not
      evaluated by the itable function.
    '''
    # a couple things we want to check first... does our argument list reduce to just an empty
    # itable or just a single itable?
    if len(args) == 0 and len(kwargs) == 0:
        return ITable({}, n=0)
    elif len(args) == 1 and len(kwargs) == 0 and isinstance(args[0], ITable):
        return args[0]
    # we want to try to convert any arguments we can from datatables into maps
    try:
        import pandas
        args = [{k:a[k].values for k in a.keys()} if isinstance(a, pandas.DataFrame) else a
                for a in args]
    except Exception: pass
    # now we want to merge these together and make them one lazy map
    m0 = lazy_map(merge(args, kwargs))
    # see if we can deduce the row size from a non-lazy argument:
    v = m0
    for mm in (list(args) + [kwargs]):
        if len(mm) == 0: continue
        if not is_lazy_map(mm):
            for k in six.iterkeys(mm):
                try: v = mm[k]
                except Exception: continue
                break
        else:
            for k in mm.iternormal():
                try: v = mm[k]
                except Exception: continue
                break
            for k in (mm.itermemoized() if v is m0 else []):
                try: v = mm[k]
                except Exception: continue
                break
        if v is not m0: break
    return ITable(m0, n=(None if v is m0 else len(v)))
def is_itable(arg):
    '''
    is_itable(x) yields True if x is an ITable object and False otherwise.
    '''
    return isinstance(arg, ITable)
