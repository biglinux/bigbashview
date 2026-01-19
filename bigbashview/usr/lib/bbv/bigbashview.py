# -*- coding: utf-8 -*-
#
#  Copyright (C) 2008 Wilson Pinto J�nior <wilson@openlanhouse.org>
#  Copyright (C) 2011 Thomaz de Oliveira dos Reis <thor27@gmail.com>
#  Copyright (C) 2021 Elton Fabrício Ferreira <eltonfabricio10@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import glob

def _enable_python_version_fallback():
    """
    Append site-packages from other python versions to sys.path
    to allow importing modules not yet available in the current version.
    """
    # glob pattern for site-packages
    # We assume standard linux paths: /usr/lib/pythonX.Y/site-packages
    paths = glob.glob('/usr/lib/python3.*/site-packages')
    
    current_version_path = f"/usr/lib/python{sys.version_info.major}.{sys.version_info.minor}/site-packages"

    for path in paths:
        if path == current_version_path:
            continue
            
        if path not in sys.path:
            # Append to end of path to use as fallback
            sys.path.append(path)

_enable_python_version_fallback()

from bbv.main import Main

if __name__ == "__main__":
    app = Main()
    app.run()
