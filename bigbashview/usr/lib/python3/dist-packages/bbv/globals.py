# -*- coding: utf-8 -*-
#
#  Copyright (C) 2008 Wilson Pinto Júnior <wilson@openlanhouse.org>
#  Copyright (C) 2011 Thomaz de Oliveira dos Reis <thor27@gmail.com>
#  Copyright Elton 2019
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
import os
import sys

APP_NAME = "BigBashView"
APP_VERSION = "3.5.1"
PROGDIR = os.path.dirname(os.path.realpath(__file__))
ICON = os.sep.join((PROGDIR, "img", "icone.png"))
LOGO = os.sep.join((PROGDIR, "img", "logo.png"))
COMPAT = False

def ADDRESS(): return '127.0.0.1'

def PORT(): return 9000
