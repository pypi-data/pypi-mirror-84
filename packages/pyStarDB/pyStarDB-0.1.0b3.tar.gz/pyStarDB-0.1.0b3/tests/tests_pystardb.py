import unittest
import os
import pandas as pd
from pyStarDB import sp_pystardb as pystar
import numpy as np

class MyTestCase(unittest.TestCase):

    def test_file_is_written_loop_notag(self):
        try:
            os.remove("name.star")
        except FileNotFoundError:
            pass

        a = pd.DataFrame([[0, 1], [2, 3]], columns=['col1', 'col2'])
        b = pystar.StarFile('name.star')
        b.update('', a, True)
        b.write_star_file()
        exists = os.path.exists('name.star')
        os.remove("name.star")

        self.assertTrue(exists,"File (loop) was not written")

    def test_file_is_written_no_loop_notag(self):
        try:
            os.remove("name.star")
        except FileNotFoundError:
            pass

        a = pd.DataFrame([[0, 1], [2, 3]], columns=['col1', 'col2'])
        b = pystar.StarFile('name.star')
        b.update('', a, False)
        b.write_star_file()
        exists = os.path.exists('name.star')

        try:
            os.remove("name.star")
        except FileNotFoundError:
            pass

        self.assertTrue(exists,"File (no-loop) was not written")

    def test_create_and_read(self):

        try:
            os.remove("name.star")
        except FileNotFoundError:
            pass

        a = pd.DataFrame([[0, 1], [2, 3]], columns=['_col1', '_col2'])
        b = pystar.StarFile('name.star')
        b.update('', a, True)
        b.write_star_file()

        c = pystar.StarFile('name.star')

        is_equal_col1 = a['_col1'].equals(c['']['_col1'])
        is_equal_col2 = a['_col2'].equals(c['']['_col2'])

        try:
            os.remove("name.star")
        except FileNotFoundError:
            pass

        self.assertTrue(is_equal_col1 and is_equal_col2,"Write / Read test failed")



    #Test to fix the tag bug
    def test_create_and_read_tag(self):

        try:
            os.remove("name.star")
        except FileNotFoundError:
            pass

        a = pd.DataFrame([[0, 1], [2, 3]], columns=['_col1', '_col2'])
        b = pystar.StarFile('name.star')
        b.update('my_tag', a, True)
        b.write_star_file()

        c = pystar.StarFile('name.star')

        is_equal_col1 = a['_col1'].equals(c['my_tag']['_col1'])
        is_equal_col2 = a['_col2'].equals(c['my_tag']['_col2'])

        try:
            os.remove("name.star")
        except FileNotFoundError:
            pass

        self.assertTrue(is_equal_col1 and is_equal_col2,"Write / Read test failed")

    def test_create_and_read_tag_multitag(self):

        fname="name.star"
        try:
            os.remove(fname)
        except FileNotFoundError:
            pass

        a = pd.DataFrame([[0, 1], [2, 3]], columns=['_col1', '_col2'])
        a2 = pd.DataFrame([[4, 5], [6, 7]], columns=['_col1', '_col2'])
        b = pystar.StarFile(fname)
        b.update('my_tag', a, True)
        b.update('my_tag_2', a2, True)
        b.write_star_file()

        c = pystar.StarFile(fname)

        is_equal_col1_mytag = a['_col1'].equals(c['my_tag']['_col1'])
        is_equal_col2_mytag = a['_col2'].equals(c['my_tag']['_col2'])
        is_equal_col1_mytag2 = a2['_col1'].equals(c['my_tag_2']['_col1'])
        is_equal_col2_mytag2 = a2['_col2'].equals(c['my_tag_2']['_col2'])
        all_is_equal = is_equal_col1_mytag and is_equal_col2_mytag and is_equal_col1_mytag2 and is_equal_col2_mytag2
        try:
            os.remove(fname)
        except FileNotFoundError:
            pass

        self.assertTrue(all_is_equal,"Write / Read test failed")



    def test_linespacing_after_header(self):

        a = pd.DataFrame([[0, 1], [2, 3], [2,3]], columns=['_col1', '_col2'])
        a2 = pd.DataFrame([[4, 5], [6, 7], [3,3]], columns=['_col1', '_col2'])
        b = pystar.StarFile('name.star')
        b.update('my_tag', a, True)
        b.update('my_tag_2', a2, True)
        starpath = os.path.join(os.path.dirname(__file__), '../resources/name_space.star')
        c = pystar.StarFile(starpath)
        is_equal_col1_mytag = a['_col1'].equals(c['my_tag']['_col1'])
        is_equal_col2_mytag = a['_col2'].equals(c['my_tag']['_col2'])
        is_equal_col1_mytag2 = a2['_col1'].equals(c['my_tag_2']['_col1'])
        is_equal_col2_mytag2 = a2['_col2'].equals(c['my_tag_2']['_col2'])
        all_is_equal = is_equal_col1_mytag and is_equal_col2_mytag and is_equal_col1_mytag2 and is_equal_col2_mytag2


        self.assertTrue(all_is_equal,"Write / Read test failed")

    def test_wrong_file_provided(self):

        with self.assertRaises(TypeError) as cm:
            starpath = os.path.join(os.path.dirname(__file__), '../resources/TcdA1-0010_frames_sum.cbox')
            a = pystar.StarFile(starpath)
            self.assertEqual(cm.exception.code, 1)

    def test_zero_number_of_columns(self):
        with self.assertRaises(TypeError) as cm:
            starpath = os.path.join(os.path.dirname(__file__), '../resources/ActinLifeAct_00072_zerocol.star')
            a = pystar.StarFile(starpath)
            self.assertEqual(str(cm.exception), "Unable to grab the header information and column information")

    def test_throw_expection(self):
        starpath = os.path.join(os.path.dirname(__file__), '../resources/TcdA1-0010_frames_sum.cbox')
        got_exception = False
        try:
            a = pystar.StarFile(starpath)
        except TypeError:
            got_exception = True

        self.assertTrue(got_exception)


    def test_write_non_loop(self):
        fname = "name.star"
        try:
            os.remove(fname)
        except FileNotFoundError:
            pass

        a = pd.DataFrame([[0, 1], [2, 3]], columns=['_col1', '_col2'])
        b = pystar.StarFile(fname)
        b.update('my_tag', a, True)

        version_df = pd.DataFrame([["1.0"]], columns=['_cbox_format_version'])
        b.update('global', version_df, False)
        b.write_star_file()

        c = pystar.StarFile(fname)

        global_is_written = ('global' in c) and ('my_tag' in c)
        try:
            os.remove(fname)
        except FileNotFoundError:
            pass

        self.assertTrue(global_is_written, True)

    def test_data_no_copy(self):
        fname = "name.star"
        try:
            os.remove(fname)
        except FileNotFoundError:
            pass
        b = pystar.StarFile(fname)

        a = pd.DataFrame([[0, 1], [2, 3]], columns=['_col1', '_col2'])
        b.update('my_tag', a, True)
        version_df = pd.DataFrame([["1.0"]], columns=['_cbox_format_version'])
        b.update('global', version_df, False)
        b.write_star_file()

        c = pystar.StarFile(fname)
        a = pd.DataFrame([[0, 1], [2, 3]], columns=['_col1', '_col2'])
        c.update('my_tag', a, True)
        version_df = pd.DataFrame([["1.0"]], columns=['_cbox_format_version'])
        c.update('global', version_df, False)

        c.write_star_file(overwrite=True, tags=["global","my_tag"])

        col_1_counter = 0
        col_2_counter = 0
        with open(fname) as f:
            lines = f.readlines()
            for line in lines:
                if '_col1' in line:
                    col_1_counter = col_1_counter + 1
                if '_col2' in line:
                    col_2_counter = col_2_counter +1

        try:
            os.remove(fname)
        except FileNotFoundError:
            pass

        self.assertTrue(col_1_counter == 1 and col_2_counter == 1, "Data block seems to be copied...")

    def test_non_loop_entries_on_singleline(self):
        fname = "name.star"
        try:
            os.remove(fname)
        except FileNotFoundError:
            pass
        b = pystar.StarFile(fname)

        a = pd.DataFrame([[0, 1], [2, 3]], columns=['_col1', '_col2'])
        b.update('my_tag', a, True)
        version_df = pd.DataFrame([["1.0", "20"]], columns=['_cbox_format_version','_cbox_format_version_2'])
        b.update('global', version_df, False)
        b.write_star_file()

        c = pystar.StarFile(fname)

        try:
            os.remove(fname)
        except FileNotFoundError:
            pass

        global_is_written = ('global' in c) and ('global' in b)
        self.assertTrue(global_is_written, True)


    def test_pandas_merging(self):
        fname = "name.star"
        fname1 = "name1.star"

        b = pystar.StarFile(fname)
        a = pd.DataFrame([[0, 1], [2, 3]], columns=['_c1', '_c2'])
        b.update('my_tag', a, True)

        c = pystar.StarFile(fname1)
        d = pd.DataFrame([[9, 3], [3, 6]], columns=['_c1', '_c2'])
        c.update('my_tag', d, True)

        newd =  b + c
        b += c
        self.assertTrue(b , newd)



    def test_markus_specification(self):

        fname = "name.star"
        fname1 = "name1.star"
        x = pd.DataFrame([[0, 1], [1, 2]], columns=['_c1', '_c2'])
        y = pd.DataFrame([[3, 4], [5, 6]], columns=['_c1', '_c2'])
        a = pystar.StarFile(fname)
        a.update('a', x, True)
        b = pystar.StarFile(fname1)
        b.update('a', y, True)

        c = pystar.StarFile.add_star([a, b])
        self.assertTrue(np.array_equal(c['a']['_c1'].values, [0, 1, 3, 5]) )
        self.assertTrue(np.array_equal(c['a']['_c2'].values, [1, 2, 4, 6]))

        d = pystar.StarFile(None)
        pystar.StarFile.add_star([a, b], d)
        self.assertTrue(np.array_equal(d['a']['_c1'].values, [0, 1, 3, 5]) )
        self.assertTrue(np.array_equal(d['a']['_c2'].values, [1, 2, 4, 6]))

        e = a + b
        self.assertTrue(np.array_equal(e['a']['_c1'].values, [0, 1, 3, 5]) )
        self.assertTrue(np.array_equal(e['a']['_c2'].values, [1, 2, 4, 6]))

        f = a
        f += b
        self.assertTrue(np.array_equal(f['a']['_c1'].values, [0, 1, 3, 5]))
        self.assertTrue(np.array_equal(f['a']['_c2'].values, [1, 2, 4, 6]))



if __name__ == '__main__':
    unittest.main()


