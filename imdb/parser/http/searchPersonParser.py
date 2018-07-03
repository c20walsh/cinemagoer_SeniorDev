# Copyright 2004-2017 Davide Alberani <da@erlug.linux.it>
#           2008-2018 H. Turgut Uyar <uyar@tekir.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

"""
This module provides the classes (and the instances) that are used to parse
the results of a search for a given person.

For example, when searching for the name "Mel Gibson", the parsed page
would be:

http://www.imdb.com/find?q=Mel+Gibson&s=nm
"""

from __future__ import absolute_import, division, print_function, unicode_literals

from imdb.utils import analyze_name

from .piculet import Path, Rule, Rules
from .searchMovieParser import DOMHTMLSearchMovieParser
from .utils import analyze_imdbid


def _cleanName(n):
    """Clean the name in a title tag."""
    if not n:
        return ''
    n = n.replace('Filmography by type for', '')    # FIXME: temporary.
    return n


class DOMHTMLSearchPersonParser(DOMHTMLSearchMovieParser):
    """Parse the html page that the IMDb web server shows when the
    "new search system" is used, for persons."""
    _linkPrefix = '/name/nm'

    rules = [
        Rule(
            key='data',
            extractor=Rules(
                foreach='//td[@class="result_text"]/a[starts-with(@href, "/name/nm")]/..',
                rules=[
                    Rule(
                        key='link',
                        extractor=Path('./a[1]/@href')
                    ),
                    Rule(
                        key='name',
                        extractor=Path('./a[1]/text()')
                    ),
                    Rule(
                        key='index',
                        extractor=Path('./text()[1]')
                    ),
                    Rule(
                        key='akas',
                        extractor=Path('.//div[@class="_imdbpyAKA"]/text()')
                    )
                ],
                transform=lambda x: (
                    analyze_imdbid(x.get('link') or ''),
                    analyze_name((x.get('name') or '') + (x.get('index') or ''),
                                 canonical=1), x.get('akas')
                )
            )
        )
    ]


_OBJECTS = {
    'search_person_parser': ((DOMHTMLSearchPersonParser,), {'kind': 'person'})
}
