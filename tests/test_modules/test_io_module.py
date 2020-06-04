import numpy as np
from pathlib import Path
from tifffile import imread
from suite2p import io


def get_binary_file_data(tmp_dir, op):
    # Read in binary file's contents as int16 np array
    binary_file_data = np.fromfile(
        str(Path(tmp_dir).joinpath('suite2p', 'plane0', 'data.bin')),
        np.int16
    )
    return np.reshape(binary_file_data, (-1, op['Ly'], op['Lx']))


class TestSuite2pIoModule:
    """
    Tests for the Suite2p IO module
    """
    def test_tiff_reconstruction_from_binary_file(self, setup_and_teardown, get_test_dir_path):
        """
        Tests to see if tif generated by tiff_to_binary and write_tiff matches test tif.
        """
        ops, tmp_dir = setup_and_teardown
        op = io.tiff_to_binary(ops)[0]
        output_data = get_binary_file_data(tmp_dir, op)
        # Make sure data in matrix is nonnegative
        assert np.all(output_data >= 0)
        io.write_tiff(output_data, op, 0, True)
        reconstructed_tiff_data = imread(
            str(Path(tmp_dir).joinpath('suite2p', 'plane0', 'reg_tif', 'file000_chan0.tif'))
        )
        # Compare to our test data
        prior_data = imread(
            str(Path(get_test_dir_path).joinpath('1plane1chan', 'suite2p', 'test_write_tiff.tif'))
        )
        assert np.array_equal(reconstructed_tiff_data, prior_data)

    def test_h5_to_binary_nonnegative_output(self, setup_and_teardown, get_test_dir_path):
        """
        Tests if the binary file produced by h5_to_binary contains nonnegative data.
        """
        op, tmp_dir = setup_and_teardown
        op['h5py'] = Path(get_test_dir_path).joinpath('input.h5')
        op['data_path'] = []
        op = io.h5py_to_binary(op)[0]
        output_data = get_binary_file_data(tmp_dir, op)
        assert np.all(output_data >= 0)