"""

Copyright 2019-2020 European Union

Licensed under the EUPL, Version 1.2 or as soon they will be approved by the European Commission  subsequent versions of the EUPL (the "Licence");

You may not use this work except in compliance with the Licence.
You may obtain a copy of the Licence at:

https://joinup.ec.europa.eu/sites/default/files/inline-files/EUPL%20v1_2%20EN(1).txt

Unless required by applicable law or agreed to in writing, software distributed under the Licence is distributed on an "AS IS" basis,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the Licence for the specific language governing permissions and limitations under the Licence.

"""

import os
import itertools
import datetime

from nine import IS_PYTHON2
if IS_PYTHON2:
    from pathlib2 import Path
else:
    from pathlib import Path

import numpy as np
from netCDF4 import Dataset, date2index

from ..readers import PCRasterMap
from .. import logger


class Comparator(object):
    """

    """
    glob_expr = None

    def __init__(self, array_equal=False, for_testing=False):
        """

        """
        self.array_equal = array_equal
        self.for_testing = for_testing
        self.errors = []

    def compare_dirs(self, path_a, path_b, skip_missing=False, timestep=None):
        """
        :param path_a
        :param path_b
        :param skip_missing (bool, default False). If True, ignore files that are in path_a and not in path_b
        :param timestep (default None). If passed, comparison happens only at the defined timestep
        """
        logger.info('Comparing %s and %s %s[skip missing: %s]', path_a, path_b, '(time: %s) ' % timestep if timestep else '', skip_missing)
        path_a = Path(path_a)
        path_b = Path(path_b)
        for fa in itertools.chain(*(path_a.glob(e) for e in self.glob_expr)):
            fb = path_b.joinpath(fa.name)
            if not fb.exists():
                if skip_missing:
                    logger.info('skipping %s as it is not in %s', fb.name, path_b.as_posix())
                    continue
                else:
                    message = '{} is missing in {}'.format(fb.name, path_b.as_posix())
                    if self.for_testing:
                        assert False, message
                    else:
                        self.errors.append(message)
                        continue

            self.compare_files(fa.as_posix(), fb.as_posix(), timestep)
        if not self.for_testing:
            return self.errors

    def compare_files(self, fa, fb, timestep=None):
        raise NotImplementedError()


class PCRComparator(Comparator):
    # TODO add comparison with tolerance
    glob_expr = ['**/*.[0-9][0-9][0-9]', '**/*.map']

    def compare_files(self, file_a, file_b, timestep=None):
        logger.info('Comparing %s and %s', file_a, file_b)
        map_a = PCRasterMap(file_a)
        map_b = PCRasterMap(file_b)

        if map_a != map_b:
            map_a.close()
            map_b.close()
            message = '{} different from {}'.format(file_a, file_b)
            if self.for_testing:
                assert False, message
            else:
                self.errors.append(message)
                return message
        else:
            map_a.close()
            map_b.close()
            assert True


def find_timestep(tss_file, timestep):
    found_timestep = False
    current_line = tss_file.readline()
    while not found_timestep:
        if not current_line:
            break
        try:
            current_timestep = current_line.strip().split()[0]
        except IndexError:
            current_line = tss_file.readline()
        else:
            if current_timestep.decode() == str(timestep):
                found_timestep = True
                break
            else:
                current_line = tss_file.readline()
    return current_line, found_timestep


class TSSComparator(Comparator):
    glob_expr = ['**/*.tss']

    def __init__(self, atol=0.0001, rtol=0.001,
                 array_equal=False, for_testing=True):

        super(TSSComparator, self).__init__(array_equal=array_equal, for_testing=for_testing)
        self.atol = atol
        self.rtol = rtol

    def _findline_at_timestep(self, tss_file, timestep):
        b1, found_timestep = find_timestep(tss_file, timestep)
        if not found_timestep:
            message = '{} not found in {}'.format(timestep, tss_file.name)
            if self.for_testing:
                assert False, message
            else:
                self.errors.append(message)
        return b1

    def compare_lines_equal(self, file_a, file_b, timestep=None):
        tss1 = open(file_a, 'rb')
        tss2 = open(file_b, 'rb')
        # skip first line in TSS as it just reports settings filename
        tss1.readline()
        tss2.readline()

        if not timestep:
            # identical TSS files
            while True:
                b1 = tss1.readline()
                b2 = tss2.readline()
                if (b1 != b2) or (not b1 and b2) or (not b2 and b1):
                    message = '{} different from {}'.format(file_a, file_b)
                    if self.for_testing:
                        assert False, message
                    else:
                        self.errors.append(message)
                        return message
                if not b1:
                    break
        else:
            # check line at a given timestep
            b1 = self._findline_at_timestep(tss1, timestep)
            b2 = self._findline_at_timestep(tss2, timestep)

            if b1 != b2:
                message = '{} different from {} for timestep {}'.format(file_a, file_b, timestep)
                if self.for_testing:
                    assert False, message
                else:
                    self.errors.append(message)
        assert True
        return self.errors

    def compare_lines_tolerance(self, file_a, file_b, timestep=None):
        tss1 = open(file_a, 'rb')
        tss2 = open(file_b, 'rb')
        # skip first lines in TSS as it just reports settings filename
        line = b''
        numline = 1
        while 'timestep' not in line.decode():
            tss1.readline()
            line = tss2.readline()
            numline += 1

        while True:
            if not timestep:
                b1 = tss1.readline().strip().split()
                b2 = tss2.readline().strip().split()
                if not b1:
                    break
                self._check_tss_line_tol(b1, b2, file_a, file_b, numline)
            else:
                b1 = self._findline_at_timestep(tss1, timestep)
                b2 = self._findline_at_timestep(tss2, timestep)

                b1 = b1.strip().split()
                b2 = b2.strip().split()
                self._check_tss_line_tol(b1, b2, file_a, file_b, numline)
                # just one line
                break

        assert True
        return self.errors

    def _check_tss_line_tol(self, b1, b2, file_a, file_b, numline):
        array1 = np.array(b1, dtype='float64')
        array2 = np.array(b2, dtype='float64')
        if not np.allclose(array1, array2, rtol=self.rtol, atol=self.atol, equal_nan=True):
            message = '{} different from {} (line: {})\n line A: {}\n line B: {}'.format(file_a, file_b, numline,
                                                                                         array1, array2)
            message += '\n {}'.format(np.abs(array1 - array2))
            if self.for_testing:
                np.testing.assert_allclose(array1, array2, rtol=self.rtol, atol=self.atol, equal_nan=True)
                assert False, message
            else:
                self.errors.append(message)

    def compare_files(self, file_a, file_b, timestep=None):
        logger.info('Comparing %s and %s', file_a, file_b)
        if self.array_equal:
            self.compare_lines_equal(file_a, file_b, timestep)
        else:
            self.compare_lines_tolerance(file_a, file_b, timestep)


class NetCDFComparator(Comparator):
    glob_expr = ['**/*.nc']

    def __init__(self, mask, atol=0.0001, rtol=0.001,
                 max_perc_diff=0.2, max_perc_large_diff=0.1,
                 array_equal=False, for_testing=True):

        super(NetCDFComparator, self).__init__(array_equal=array_equal, for_testing=for_testing)

        if isinstance(mask, str):
            mask = Dataset(mask)
            maskvar = [k for k in mask.variables if len(mask.variables[k].dimensions) == 2][0]
            self.maskarea = np.logical_not(mask.variables[maskvar][:, :])
        else:
            self.maskarea = mask

        self.atol = atol
        self.rtol = rtol
        self.max_perc_large_diff = max_perc_large_diff
        self.max_perc_diff = max_perc_diff
        self.large_diff_th = self.atol * 10

    def compare_arrays(self, vara_step, varb_step, varname=None, step=None, filepath=None):

        vara_step = np.ma.compressed(np.ma.masked_array(vara_step, self.maskarea)).astype('float64')
        varb_step = np.ma.compressed(np.ma.masked_array(varb_step, self.maskarea)).astype('float64')
        diff_values = np.ma.abs(vara_step - varb_step)
        diff_values = diff_values[~np.isnan(diff_values)]
        same_values = np.ma.allclose(diff_values, np.zeros(diff_values.shape), atol=self.atol, rtol=self.rtol)
        all_ok = vara_step.size == varb_step.size and same_values
        array_ok = np.isclose(diff_values, np.zeros(diff_values.shape), atol=self.atol, rtol=self.rtol, equal_nan=True)
        different_values_size = array_ok[~array_ok].size
        if (not all_ok) and (different_values_size > 0):
            max_diff = np.ma.amax(diff_values)  # returns a scalar
            perc_wrong = different_values_size * 100 / vara_step.size
            result = np.ma.where(diff_values >= max_diff)
            if perc_wrong >= self.max_perc_diff or (perc_wrong >= self.max_perc_large_diff and max_diff > self.large_diff_th):
                step = step if step is not None else '(no time)'
                filepath = os.path.basename(filepath) if filepath else '<mem>'
                varname = varname or '<unknown var>'
                message = '{}/{}@{} - {:3.2f}% of different values - max diff: {:3.6f}'.format(filepath, varname, step, perc_wrong, max_diff)
                logger.error(message)
                if self.for_testing:
                    assert False, message
                else:
                    self.errors.append(message)
                    return message
        assert True

    def compare_files(self, file_a, file_b, timestep=None):
        logger.info('Comparing %s and %s %s', file_a, file_b, timestep or '')
        if timestep and not isinstance(timestep, datetime.datetime):
            raise ValueError('timestep must be of type datetime.datetime but type {} was found'.format(str(type(timestep))))
        with Dataset(file_a) as nca, Dataset(file_b) as ncb:
            num_dims = 3 if 'time' in nca.variables else 2
            var_name = [k for k in nca.variables if len(nca.variables[k].dimensions) == num_dims][0]
            vara = nca.variables[var_name]
            try:
                varb = ncb.variables[var_name]
            except KeyError:
                var_nameb = [k for k in ncb.variables if len(ncb.variables[k].dimensions) == num_dims][0]
                message = 'Files: {} vs {} have different variables names A:{} B:{}'.format(file_a, file_b, var_name, var_nameb)
                if self.for_testing:
                    assert False, message
                else:
                    self.errors.append(message)
                    return message
            if 'time' in nca.variables:
                if not timestep:
                    stepsa = nca.variables['time'][:]
                    stepsb = ncb.variables['time'][:]
                    if len(stepsa) != len(stepsb):
                        message = 'Files: {} vs {}: different number of steps A:{} B:{}'.format(file_a, file_b, len(stepsa), len(stepsb))
                        if self.for_testing:
                            assert False, message
                        else:
                            self.errors.append(message)
                            return message
                    for step, _ in enumerate(stepsa):
                        values_a = vara[step][:, :]
                        values_b = varb[step][:, :]
                        if not self.array_equal:
                            mess = self.compare_arrays(values_a, values_b, var_name, step, file_a)
                        else:
                            mess = self.compare_arrays_equal(values_a, values_b, var_name, step, file_a)
                        if mess:
                            self.errors.append(mess)
                else:
                    # check arrays at a given timestep
                    ia = date2index(timestep, nca.variables['time'], nca.variables['time'].calendar)
                    ib = date2index(timestep, ncb.variables['time'], ncb.variables['time'].calendar)
                    values_a = vara[ia][:, :]
                    values_b = varb[ib][:, :]
                    if not self.array_equal:
                        mess = self.compare_arrays(values_a, values_b, var_name, ia, file_a)
                    else:
                        mess = self.compare_arrays_equal(values_a, values_b, var_name, ia, file_a)
                    if mess:
                        self.errors.append(mess)
            else:
                values_a = vara[:, :]
                values_b = varb[:, :]
                if not self.array_equal:
                    mess = self.compare_arrays(values_a, values_b, var_name, filepath=file_a)
                else:
                    mess = self.compare_arrays_equal(values_a, values_b, var_name, filepath=file_a)
                if mess:
                    self.errors.append(mess)
            return self.errors

    def compare_arrays_equal(self, values_a, values_b, varname=None, step=None, filepath=None):
        filepath = os.path.basename(filepath) if filepath else '<mem>'
        message = '{}/{}@{} is different'.format(filepath, varname, step)
        if self.for_testing:
            np.testing.assert_array_equal(values_a, values_b, message)
        else:
            if not np.array_equal(values_a, values_b):
                self.errors.append(message)
                return message
