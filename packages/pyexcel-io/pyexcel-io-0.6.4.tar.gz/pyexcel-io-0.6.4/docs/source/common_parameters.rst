Common parameters
================================================================================


'library' option is added
--------------------------------------------------------------------------------

In order to have overlapping plugins co-exist, 'library' option is added to
get_data and save_data.


get_data only parameters
--------------------------------------------------------------------------------

keep_trailing_empty_cells
********************************************************************************

default: False

If turned on, the return data will contain trailing empty cells.


auto_dectect_datetime
********************************************************************************

The datetime formats are:

#. %Y-%m-%d
#. %Y-%m-%d %H:%M:%S
#. %Y-%m-%d %H:%M:%S.%f

Any other datetime formats will be thrown as ValueError


csv only parameters
--------------------------------------------------------------------------------

pep_0515_off
********************************************************************************

This is related to `PEP 0515 <https://www.python.org/dev/peps/pep-0515/>`_, where
'_' in numeric values are considered legal in python 3.6. This behavior is
not consistent along with other python versions. PEP 0515 by default is suppressed.
And this flag allows you to turn it on in python 3.6.

