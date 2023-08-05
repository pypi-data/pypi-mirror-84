# quad-filter

A couple of utility functions used to locate the regions of a cartesian
map where a condition is true or false

In many cases, this is not the optimal way to generate such tiles,
but it may be of use if you only have access to a function that
return true for an area.


See the script [examples/boundaries.py](examples/boundaries.py) for an
example of use.  That script produces the square kilometers containing
the boundary of the region of interest (aligned on the south-west point
of its bounding box) as well as square areas that do not contain the
boundary.
![Square kilometers containing Inverness and Nairn's boundary](examples/inverness-and-nairn.png)

The source data for the map above comes from [Scottish Parliamentary Constituencies (May 2016) Generalised Clipped Boundaries in Scotland ](https://data.gov.uk/dataset/2b34d337-b476-460b-bd51-65489eeb2167/scottish-parliamentary-constituencies-may-2016-generalised-clipped-boundaries-in-scotland)
and is licensed under the UK Open Government Licence.