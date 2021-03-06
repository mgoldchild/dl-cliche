import unittest
from dlcliche.utils import *
from dlcliche.big_h5_array import *
from dlcliche.test import *

class TestBigH5Array(unittest.TestCase):
    ROW_SIZE = 2*2*1056
    COL_SIZE = 23

    @classmethod
    def tearDownClass(self):
        ensure_delete('test.h5')

    def do_test_as_normal_array(self, shape, testdata):
        # write test - just confirm no error
        h5array = BigH5Array('test.h5', shape)
        h5array.open_for_write()
        h5array()[...] = testdata
        h5array.close()

        # read test - real test
        h5array = BigH5Array('test.h5')
        h5array.open_for_read()
        for col in range(shape[0]):
            #print('Testing ...[%d]' % col, testdata.shape, testdata[col])
            recursive_test_array(self, h5array()[col], testdata[col], msg='failed@', fn=self.assertAlmostEqual)
        h5array.close()

        # big_h5_load test
        x = big_h5_load('test.h5')
        for col in range(shape[0]):
            #print('Testing big_h5_load ...[%d]' % col, testdata.shape, testdata[col])
            recursive_test_array(self, x[col], testdata[col], msg='failed@', fn=self.assertAlmostEqual)

        print('')

    def test_1_as_normal_array(self):
        self.do_test_as_normal_array((TestBigH5Array.COL_SIZE, TestBigH5Array.ROW_SIZE),
                                    np.random.rand(TestBigH5Array.COL_SIZE, TestBigH5Array.ROW_SIZE))

    def test_2_as_3d_normal_array(self):
        self.do_test_as_normal_array((TestBigH5Array.COL_SIZE, TestBigH5Array.ROW_SIZE, 3),
                                    np.random.rand(TestBigH5Array.COL_SIZE, TestBigH5Array.ROW_SIZE, 3))

    def test_3_write_expandable(self):
        # write test - just confirm no error
        self.test_data = []
        writer = BigH5Array('test.h5', (TestBigH5Array.COL_SIZE, TestBigH5Array.ROW_SIZE))
        writer.open_for_write_expandable()
        for col in range(TestBigH5Array.COL_SIZE):
            x = np.random.rand(1, TestBigH5Array.ROW_SIZE)
            self.test_data.append(x[0])
            writer.append(x)
        writer.close()

        # read test - real test
        reader = BigH5Array('test.h5')
        reader.open_for_read()
        self.test_data = np.array(self.test_data)
        for col in range(TestBigH5Array.COL_SIZE):
            #print('Testing ...[%d]' % col, self.test_data.shape, self.test_data[col])
            recursive_test_array(self, reader.data()[col], self.test_data[col], msg='failed@', fn=self.assertAlmostEqual)
        reader.close()

        print('')

if __name__ == '__main__':
    unittest.main()
