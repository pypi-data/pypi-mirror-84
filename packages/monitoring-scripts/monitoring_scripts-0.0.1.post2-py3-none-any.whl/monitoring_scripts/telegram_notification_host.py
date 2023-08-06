#!/usr/bin/python3
# -*- coding: utf-8

#  monitoring-scripts
#
#  Monitoring monitoring-scripts are some useful scripts for notifications and more
#
#  Copyright (c) 2020 Fabian Fröhlich <mail@confgen.org> <https://icinga2.confgen.org>
#
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#  For all license terms see README.md and LICENSE Files in root directory of this Project.
#
#  Checkout this project on github <https://github.com/f-froehlich/monitoring-scripts>
#  and also my other projects <https://github.com/f-froehlich>


import sys

sys.path.insert(0, '/usr/local/monitoring')

from monitoring_utils.Notification.Telegram.HostNotification import HostNotification

if __name__ == '__main__':
    HostNotification()
