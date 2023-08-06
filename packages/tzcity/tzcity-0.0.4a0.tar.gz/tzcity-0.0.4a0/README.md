# tzcity

<a href="https://pypi.org/ju-sh/tzcity"><img alt="PyPI" src="https://img.shields.io/pypi/v/tzcity"></a>
<img alt="Build Status" src="https://api.travis-ci.com/ju-sh/tzcity.svg?branch=master"></img>
<a href="https://github.com/ju-sh/tzcity/blob/master/LICENSE"><img alt="License: MIT" src="https://img.shields.io/pypi/l/tzcity"></a>

A module to find the Olson database time zone names of some of the most populous cities in the world without an internet connection.

Only a few cities associated with each time zone are recognized to minimize the size of data bundled with the package.

<h2>Installation</h2>

You need Python>=3.6 to use tzcity.

It can be installed from PyPI with pip using

    pip install tzcity

<h2>Usage</h2>

> ##### `tzcity.tzcity(city: str) -> str`

Accepts a city name and returns the time zone name associated with that city.

Raises `UnknownTZCityException` if unable to recognize city.

    >>> tzcity.tzcity('abu dhabi')
    'Asia/Dubai'

    >>> tzcity.tzcity('bandar seri begawan')
    'Asia/Brunei'

    >>> tzcity.tzcity('myanmar')  # a country with only one time zone
    'Asia/Yangon'

---

> ##### `tzcity.capitalize(name: str) -> str`

Capitalize the city or time zone name provided as argument.

Raises `UnknownTZCityException` if unable to recognize name.

    >>> tzcity.capitalize('andorra la vella')
    'Andorra la Vella'

    >>> tzcity.capitalize("new york")
    'New York'

    >>> tzcity.capitalize("dumont d'urville")
    "Dumont d'Urville"
