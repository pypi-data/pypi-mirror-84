"""
The `frame` module allows working with StarTable tables as pandas dataframes.

This is implemented by providing both `Table` and `TableDataFrame` interfaces to the same object.

## Idea

The central idea is that as much as possible of the table information is stored as a pandas
dataframe, and that the remaining information is stored as a `ComplementaryTableInfo` object
attached to the dataframe as registered metadata. Further, access to the full table data
structure is provided through a facade object (of class `Table`). `Table` objects have no state
(except the underlying decorated dataframe) and are intended to be created when needed
and discarded afterwards:

```
dft = make_table_dataframe(...)
unit_height = Table(dft).height.unit
```

Advantages of this approach are that:

1. Code can be written for (and tested with) pandas dataframes and still operate on `TableDataFrame`
   objects. This avoids unnecessary coupling to the StarTable project.
2. The table access methods of pandas are available for use by consumer code. This both saves
   the work of making startable-specific access methods, and likely allows better performance
   and documentation.

## Implementation details

The decorated dataframe objects are represented by the `TableDataFrame` class.

### Dataframe operations

Pandas allows us to hook into operations on dataframes via the `__finalize__` method.
This makes it possible to propagate table metadata over select dataframe operations.
See `TableDataFrame` documentation for details.

### Column metadata

Propagating metadata would be greatly simplified if column-specific metadata was stored with the
column. However, metadata attached to `Series` object is not retained within the dataframe, see
https://github.com/pandas-dev/pandas/issues/6923#issuecomment-41043225.

## Alternative approaches

It should be possible to maintain column metadata together with the column data through the use of
`ExtensionArray`. This option was discarded early due to performance concerns, but might be viable
and would the be preferable to the chosen approach.
"""

import pandas as pd
import warnings
from typing import Set, Dict, Optional, Iterable

from .table_metadata import TableMetadata, ColumnMetadata, ComplementaryTableInfo

_TABLE_INFO_FIELD_NAME = "_table_data"


class UnknownOperationError(Exception):
    pass


class InvalidTableCombineError(Exception):
    pass


def _combine_tables(obj: "TableDataFrame", other, method, **kwargs) -> ComplementaryTableInfo:
    """
    Called from __finalize__ when operations have been performed via the pandas.DataFrame API.

    Implementation policy is that this will fail except for situations where
    the metadata combination is safe.
    For other cases, the operations should be implemented via the Table facade
    """

    if method is None:
        # slicing
        src = [other]
    elif method == "merge":
        src = [other.left, other.right]
    elif method == "concat":
        src = other.objs
    elif method == "copy":
        src = [other]  # TODO should it be obj?  Test it
    else:
        raise UnknownOperationError(
            f"Unknown method while combining metadata: {method}. Keyword args: {kwargs}"
        )

    if len(src) == 0:
        raise UnknownOperationError(f"No operands for operation {method}")

    data = [get_table_info(s) for s in src if is_table_dataframe(s)]

    # 1: Create table metadata as combination of all
    meta = TableMetadata(
        name=data[0].metadata.name, operation=f"Pandas {method}", parents=[d.metadata for d in data]
    )

    # 2: Check that units match for columns that appear in more than one table
    out_cols: Set[str] = set(obj.columns)
    columns: Dict[str, ColumnMetadata] = {}
    for d in data:
        for name, c in d.columns.items():
            if name not in out_cols:
                continue
            col = columns.get(name, None)
            if not col:
                # not seen before in input
                col = c.copy()
                columns[name] = col
            else:
                if not col.unit == c.unit:
                    raise InvalidTableCombineError(
                        "Column {name} appears with incompatible units.", col.unit, c.unit
                    )
                col.update_from(c)

    return ComplementaryTableInfo(table_metadata=meta, columns=columns)


class TableDataFrame(pd.DataFrame):
    """
    A pandas.DataFrame subclass with associated table metadata.

    Behaves exactly as a pandas.DataFrame, and will try to retain metadata
    through pandas operations. If this is not possible, the manipulations
    will return a plain pandas.DataFrame.

    No StarTable-specific methods are available directly on this class, and TableDataFrame
    objects should not be created directly.
    Instead, use either the methods in the this module, or the Table proxy
    object, which can be constructed for a TableDataFrame object 'tdf' via Table(tdf).
    """

    _metadata = [_TABLE_INFO_FIELD_NAME]  # Register metadata fieldnames here

    # If implemented, must handle metadata copying etc
    # def __init__(self, *args, **kwargs):
    #    super().__init__(*args, **kwargs)

    # These are implicit by inheritance from dataframe
    # We could override _constructor_sliced to add metadata to exported columns
    # but not clear if this would add value
    #     @property
    #     def _constructor_expanddim(self):
    #         return pd.DataFrame
    #     @property
    #     def _constructor_sliced(self):
    #         return pd.Series

    @property
    def _constructor(self):
        return TableDataFrame

    def __finalize__(self, other, method=None, **kwargs):
        """
        Overrides pandas.core.generic.NDFrame.__finalize__()

        This method is responsible for populating TableDataFrame metadata
        when creating a new Table object.

        If left out, no metadata would be retained across table
        operations. This might be a viable solution?
        Alternatively, we could return a raw frame object on some operations
        """

        try:
            data = _combine_tables(self, other, method, **kwargs)
            object.__setattr__(self, _TABLE_INFO_FIELD_NAME, data)
        except UnknownOperationError as e:
            warnings.warn(f"Falling back to dataframe: {e}")
            return pd.DataFrame(self)
        return self

    @staticmethod
    def from_table_info(df: pd.DataFrame, table_info: ComplementaryTableInfo) -> "TableDataFrame":
        df = TableDataFrame(df)
        object.__setattr__(df, _TABLE_INFO_FIELD_NAME, table_info)
        table_info._check_dataframe(df)
        return df


def is_table_dataframe(df: pd.DataFrame) -> bool:
    return _TABLE_INFO_FIELD_NAME in df._metadata


def make_table_dataframe(
    df: pd.DataFrame,
    units: Optional[Iterable[str]] = None,
    unit_map: Optional[Dict[str, str]] = None,
    table_metadata: Optional[TableMetadata] = None,
    **kwargs,
) -> TableDataFrame:
    """
    Create TableDataFrame object from a pandas.DataFream and table metadata elements.

    Unknown keyword arguments (e.g. `name = ...`) are used to create a `TableMetadata` object.
    Alternatively, a `TableMetadata` object can be provided directly.

    Either a list of units for all columns, or a unit_map can be provided. Otherwise, default units
    are assigned.

    Example:
    tdf = make_table_dataframe(df, name='MyTable')
    """

    # build metadata
    if (table_metadata is not None) == bool(kwargs):
        raise Exception("Supply either metadata or keyword-arguments for TableMetadata constructor")
    if kwargs:
        # This is intended to fail if args are insufficient
        table_metadata = TableMetadata(**kwargs)

    df = TableDataFrame.from_table_info(
        df, table_info=ComplementaryTableInfo(table_metadata=table_metadata)
    )

    # set units
    if units and unit_map:
        raise Exception("Supply at most one of unit and unit_map")
    if units is not None:
        set_all_units(df, units)
    elif unit_map is not None:
        set_units(df, unit_map)

    return df


def get_table_info(
    df: TableDataFrame, fail_if_missing=True, check_dataframe=True
) -> Optional[ComplementaryTableInfo]:
    """
    Get ComplementaryTableInfo from existing TableDataFrame object.

    When called with default options, get_table_info will either raise an exception
    or return a ComplementaryTableInfo object with a valid ColumnMetadata defined for each column.

    check_dataframe: Check that the table data is valid with respect to dataframe.
                     If the dataframe has been manipulated directly, table will be updated to match.
    fail_if_missing: Whether to raise an exception if ComplementaryTableInfo object is missing
    """
    name: str = _TABLE_INFO_FIELD_NAME
    if name not in df._metadata:
        raise Exception(
            "Attempt to extract table data from normal pd.DataFrame object."
            "ComplementaryTableInfo can only be associated with TableDataFrame objects"
        )
    table_data = getattr(df, _TABLE_INFO_FIELD_NAME, None)
    if not table_data:
        if fail_if_missing:
            raise Exception(
                "Missing ComplementaryTableInfo object on TableDataFrame. TableDataFrame objects "
                "should be created via make_table_dataframe or a Table proxy."
            )
    elif check_dataframe:
        table_data._check_dataframe(df)
    return table_data


# example of manipulator function that directly manipulates TableDataFrame objects without constructing Table facade  # noqa
def add_column(df: TableDataFrame, name: str, values, unit: Optional[str] = None, **kwargs):
    """
    Add or update column in table. If omitted, unit will be partially inferred from value dtype.

    keyword arguments will be forwarded to ColumnMetadata constructor together with unit
    """
    df[name] = values
    columns = get_table_info(df, check_dataframe=False).columns

    new_col = (
        ColumnMetadata.from_dtype(df[name].dtype, **kwargs)
        if unit is None
        else ColumnMetadata(unit=unit, **kwargs)
    )

    col = columns.get(name, None)
    if col is None:
        columns[name] = new_col
    else:
        # Existing column
        col.update_from(new_col)


def set_units(df: TableDataFrame, unit_map: Dict[str, str]):
    columns = get_table_info(df).columns
    for col, unit in unit_map.items():
        columns[col] = unit


def set_all_units(df: TableDataFrame, units: Iterable[Optional[str]]):
    """
    Set units for all columns in table.
    """
    columns = get_table_info(df).columns
    for col, unit in zip(df.columns, units):
        columns[col].unit = unit
