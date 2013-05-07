# -*- coding: utf-8 -*-
"""
    Copyright (C) 2013 Kouhei Maeda <mkouhei@palmtb.net>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import unittest
from mock import patch
import swiftsc.client
import sys
import os.path
sys.path.append(os.path.abspath('src'))
import backup2swift.backup as b
import test_vars as v


class BackupTests(unittest.TestCase):

    @patch('swiftsc.client.retrieve_token', return_value=(v.token, v.s_url))
    def setUp(self, m):
        self.b = b.Backup(v.auth_url, v.username, v.password)

    @patch('swiftsc.client.is_container', return_value=201)
    @patch('swiftsc.client.create_container', return_value=201)
    @patch('swiftsc.client.list_objects', return_value=v.objects)
    @patch('swiftsc.client.create_object', return_value=201)
    def test_backup(self, m1, m2, m3, m4):
        self.assertEqual(self.b.backup("."), True)

    @patch('swiftsc.client.is_container', return_value=201)
    @patch('swiftsc.client.create_container', return_value=201)
    @patch('swiftsc.client.list_objects', return_value=v.objects)
    @patch('swiftsc.client.create_object', return_value=201)
    def test_backup_file(self, m1, m2, m3, m4):
        self.assertEqual(self.b.backup_file("examples/bu2sw.conf"), True)

    @patch('swiftsc.client.copy_object', return_value=201)
    @patch('swiftsc.client.create_object', return_value=201)
    @patch('swiftsc.client.delete_object', return_value=204)
    def test_rotate(self, m1, m2, m3):
        self.assertEqual(self.b.rotate(v.test_file, v.object_name,
                                       v.objects_name_l), True)

    @patch('swiftsc.client.list_objects', return_value=v.objects)
    def test_retrieve_backup_data_list(self, m):
        self.assertEqual(self.b.retrieve_backup_data_list(),
                         v.objects_name_l)
        self.assertEqual(self.b.retrieve_backup_data_list(True),
                         v.objects)
