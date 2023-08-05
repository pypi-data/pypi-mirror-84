#!/usr/bin/env python

import os

import click

import numpy as np
import astropy.stats as astats

import scipy.ndimage

from losoto.h5parm import h5parm
from losoto.operations import plot as loplot

from nenucal import __version__


t_file = click.Path(exists=True, dir_okay=False)


@click.group()
@click.version_option(__version__)
def main():
    ''' DPPP gains solution utilities ...'''


def ctoap(r, i):
    c = r + 1j * i
    return abs(c), np.angle(c)


def aptoc(amp, phase):
    c = amp * np.exp(1j * phase)
    return c.real, c.imag


def gauss_filter(arr, dx, kernel_fwhm, axis=0):
    """"Apply a gaussian filter to an array with nans.
        Allows intensity to leak into the nan area.

    Source: https://stackoverflow.com/questions/18697532/gaussian-filtering-a-image-with-nan-in-python
    """
    sigma = kernel_fwhm / dx / 2.3
    nan_msk = np.isnan(arr) | arr.mask

    gauss = arr.copy()
    gauss[nan_msk] = 0
    gauss = scipy.ndimage.gaussian_filter1d(gauss, sigma=sigma, axis=axis)

    norm = np.ones(shape=arr.shape)
    norm[nan_msk] = 0
    norm = scipy.ndimage.gaussian_filter1d(norm, sigma=sigma, axis=axis)

    # avoid RuntimeWarning: invalid value encountered in true_divide
    norm = np.where(norm == 0, 1, norm)
    gauss = gauss / norm

    return gauss


def filter(amp, phase, dx, kernel_fwhm, axis=0, sigma_clip=None):
    real, imag = aptoc(amp, phase)
    if sigma_clip is not None:
        real = astats.sigma_clip(real, axis=axis, sigma=sigma_clip)
        imag = astats.sigma_clip(imag, axis=axis, sigma=sigma_clip)
    real = gauss_filter(real, kernel_fwhm, dx, axis=axis)
    imag = gauss_filter(imag, kernel_fwhm, dx, axis=axis)

    return ctoap(real, imag)


@main.command('smooth')
@click.argument('sols', nargs=-1, type=t_file)
@click.option('--fwhm_time', help='Time coherence scale (min)', type=float, default=16)
@click.option('--fwhm_freq', help='Freq coherence scale (MHz)', type=float, default=2)
@click.option('--main_fwhm_time', help='Time coherence scale (min) for Main direction', type=float, default=20)
@click.option('--main_fwhm_freq', help='Freq coherence scale (MHz) for Main direction', type=float, default=4)
@click.option('--clip_nsigma', help='Clip solution above NSIGMA', type=float, default=4)
@click.option('--main_name', help='Name of the main direction', type=str, default='main')
def smooth(sols, fwhm_time, fwhm_freq, main_fwhm_time, main_fwhm_freq, clip_nsigma, main_name):
    ''' Smooth solutions with a Gaussian kernel'''
    for sol_file in sols:
        sol = h5parm(sol_file, readonly=False)
        try:
            solset = sol.getSolsets()[0]
            soltab_amp = solset.getSoltab('amplitude000')
            soltab_phase = solset.getSoltab('phase000')

            freq = soltab_amp.getAxisValues('freq')
            time = soltab_amp.getAxisValues('time')

            direction = [k.strip('[ ]').lower() for k in soltab_amp.getAxisValues('dir')]
            idx = list(range(len(direction)))

            if 'main' in direction:
                idx_main = (direction.index(main_name.lower()),)
                idx.remove(idx_main[0])
                print(f'Smoothing directions {idx_main} of {sol_file} with fwhm_time={main_fwhm_time}\
                        and fwhm_freq={main_fwhm_freq}')

            print(f'Smoothing directions {idx} of {sol_file} with fwhm_time={fwhm_time} and fwhm_freq={fwhm_freq}')

            weight = soltab_amp.getValues(weight=True)[0].astype(bool)
            amp = np.ma.array(soltab_amp.getValues(weight=False)[0], mask=~weight)
            phase = np.ma.array(soltab_phase.getValues(weight=False)[0], mask=~weight)

            if len(time) >= 2:
                dx_min = (time[1] - time[0]) / 60.
                if 'main' in direction and main_fwhm_time > 0:
                    amp[:, :, :, idx_main], phase[:, :, :, idx_main] = filter(amp[:, :, :, idx_main],
                                                                              phase[:, :, :, idx_main], main_fwhm_time,
                                                                              dx_min, sigma_clip=clip_nsigma)
                if fwhm_time > 0:
                    amp[:, :, :, idx], phase[:, :, :, idx] = filter(amp[:, :, :, idx],
                                                                    phase[:, :, :, idx], fwhm_time,
                                                                    dx_min, sigma_clip=clip_nsigma)

            if len(freq) >= 2:
                dx_mhz = (freq[1] - freq[0]) * 1e-6
                if 'main' in direction and main_fwhm_freq > 0:
                    amp[:, :, :, idx_main], phase[:, :, :, idx_main] = filter(amp[:, :, :, idx_main],
                                                                              phase[:, :, :, idx_main], main_fwhm_freq,
                                                                              dx_mhz, sigma_clip=clip_nsigma, axis=1)
                if fwhm_freq > 0:
                    amp[:, :, :, idx], phase[:, :, :, idx] = filter(amp[:, :, :, idx],
                                                                    phase[:, :, :, idx], fwhm_freq,
                                                                    dx_mhz, sigma_clip=clip_nsigma, axis=1)

            soltab_amp.setValues(amp)
            soltab_phase.setValues(phase)
        finally:
            sol.close()
            os.sync()


@main.command('plot')
@click.argument('sols', nargs=-1, type=t_file)
@click.option('--plot_dir', help='Plot directory', type=str, default='sol_plots')
@click.option('--clip', help='Clip ', is_flag=True)
def plot(sols, plot_dir, clip):
    ''' Plot solutions of the h5 files SOLS '''
    for sol_file in sols:
        sol = h5parm(sol_file, readonly=not clip)
        try:
            soltab_amp = sol.getSolset('sol000').getSoltab('amplitude000')
            soltab_phase = sol.getSolset('sol000').getSoltab('phase000')

            mask = ~(soltab_amp.getValues(weight=True)[0].astype(bool))
            amp = np.ma.array(soltab_amp.getValues(weight=False)[0], mask=mask)

            print('Plotting %s ...' % sol_file)
            path = os.path.join(os.path.dirname(sol_file), plot_dir)

            if (amp.shape[0] > 1) & (amp.shape[1] > 1):
                loplot.run(soltab_amp, ['time', 'freq'], axisInTable='ant', prefix='%s/amp_' % path, ncpu=1)
                loplot.run(soltab_phase, ['time', 'freq'], axisInTable='ant', prefix='%s/phase_' % path, ncpu=1)
            elif amp.shape[0] > 1:
                loplot.run(soltab_amp, ['time'], axisInTable='ant', prefix='%s/amp_' % path, ncpu=1)
                loplot.run(soltab_phase, ['time'], axisInTable='ant', prefix='%s/phase_' % path, ncpu=1)
            else:
                loplot.run(soltab_amp, ['freq'], axisInTable='ant', prefix='%s/amp_' % path, ncpu=1)
                loplot.run(soltab_phase, ['freq'], axisInTable='ant', prefix='%s/phase_' % path, ncpu=1)

        finally:
            sol.close()
            os.sync()


if __name__ == '__main__':
    main()
