#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2026 VEC-TEK.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy as np
from gnuradio import gr


class cst_pattern(gr.sync_block):
    """CST 8-column pattern + target polarization response.

    Expected columns:
      Theta[deg], Phi[deg], Abs(Realized Gain), Abs(Theta)[dB],
      Phase(Theta)[deg], Abs(Phi)[dB], Phase(Phi)[deg], Axial Ratio[dB]

    The Theta/Phi component magnitudes are interpreted as dB field-pattern
    levels and converted to relative linear field amplitudes with 10**(dB/20).
    The total realized-gain and axial-ratio columns are loaded for validation
    but are not multiplied into the response again.
    """

    def __init__(self, pattern_file=r'C:/SDR/WS/SDR/SDR_generic/antenna/c5_klasik_1_UL_1575.42MHz_gerceklesen_kazanc.txt',
                 azm_deg=0.0, elev_deg=0.0,
                 pol_angle_deg=0.0, ellipticity_deg=0.0):
        gr.sync_block.__init__(
            self, name='CST Pattern + Target Polarization',
            in_sig=[np.complex64], out_sig=[np.complex64]
        )

        self._azm_deg = float(azm_deg)
        self._elev_deg = float(elev_deg)
        self._pol_angle_deg = float(pol_angle_deg)
        self._ellipticity_deg = float(ellipticity_deg)

        rows = []
        with open(pattern_file, 'r', encoding='utf-8-sig', errors='replace') as f:
            for line in f:
                fields = line.split()
                if len(fields) < 8:
                    continue
                try:
                    rows.append([float(v) for v in fields[:8]])
                except ValueError:
                    # Skip CST headers, separators, and units.
                    continue

        if not rows:
            raise ValueError(
                'No numeric 8-column CST pattern rows found in: ' + str(pattern_file)
            )

        data = np.asarray(rows, dtype=np.float64)
        theta_col = data[:, 0]
        phi_col = data[:, 1]

        self.thetas = np.unique(theta_col)
        self.phis = np.unique(phi_col)

        if len(self.thetas) < 2 or len(self.phis) < 2:
            raise ValueError('Need at least two Theta and two Phi values')

        expected = len(self.thetas) * len(self.phis)
        if data.shape[0] != expected:
            raise ValueError(
                'Pattern grid is not rectangular: got %d rows, expected %d '
                '(%d Phi x %d Theta)' %
                (data.shape[0], expected, len(self.phis), len(self.thetas))
            )

        # Build grids by angle values, so input row ordering does not matter.
        shape = (len(self.phis), len(self.thetas))
        self.e_theta = np.empty(shape, dtype=np.complex128)
        self.e_phi = np.empty(shape, dtype=np.complex128)
        self.realized_gain = np.empty(shape, dtype=np.float64)
        self.axial_ratio = np.empty(shape, dtype=np.float64)
        filled = np.zeros(shape, dtype=bool)

        phi_index = {float(v): i for i, v in enumerate(self.phis)}
        theta_index = {float(v): i for i, v in enumerate(self.thetas)}

        # CST component levels are dB. Convert to relative field amplitude,
        # then combine with their phase to create complex components.
        for row in data:
            theta_v, phi_v, gain_total, th_db, th_phase, ph_db, ph_phase, ar_db = row
            i = phi_index[float(phi_v)]
            j = theta_index[float(theta_v)]
            amp_th = 10.0 ** (th_db / 20.0)
            amp_ph = 10.0 ** (ph_db / 20.0)
            self.e_theta[i, j] = amp_th * np.exp(1j * np.deg2rad(th_phase))
            self.e_phi[i, j] = amp_ph * np.exp(1j * np.deg2rad(ph_phase))
            self.realized_gain[i, j] = gain_total
            self.axial_ratio[i, j] = ar_db
            filled[i, j] = True

        if not np.all(filled):
            raise ValueError('CST pattern contains duplicate/missing angular grid cells')

        # Normalize both field components by one shared peak, preserving
        # relative polarization amplitude and phase.
        peak = float(np.max(np.sqrt(np.abs(self.e_theta)**2 +
                                    np.abs(self.e_phi)**2)))
        if not np.isfinite(peak) or peak <= 0:
            raise ValueError('Invalid or zero CST field amplitude')


        self.update_pattern()

    @property
    def azm_deg(self):
        return self._azm_deg

    @azm_deg.setter
    def azm_deg(self, value):
        self._azm_deg = float(value)
        self.update_pattern()

    def set_azm_deg(self, value):
        self.azm_deg = value

    @property
    def elev_deg(self):
        return self._elev_deg

    @elev_deg.setter
    def elev_deg(self, value):
        self._elev_deg = float(value)
        self.update_pattern()

    def set_elev_deg(self, value):
        self.elev_deg = value

    @property
    def pol_angle_deg(self):
        return self._pol_angle_deg

    @pol_angle_deg.setter
    def pol_angle_deg(self, value):
        self._pol_angle_deg = float(value)
        self.update_pattern()

    def set_pol_angle_deg(self, value):
        self.pol_angle_deg = value

    @property
    def ellipticity_deg(self):
        return self._ellipticity_deg

    @ellipticity_deg.setter
    def ellipticity_deg(self, value):
        self._ellipticity_deg = float(value)
        self.update_pattern()

    def set_ellipticity_deg(self, value):
        self.ellipticity_deg = value

    def _interpolate_phi_theta(self, field, phi_deg, theta_deg):
        """Bilinear interpolation, with periodic Phi wrap-around."""
        # Theta is bounded by the file's available range.
        theta = float(np.clip(theta_deg, self.thetas[0], self.thetas[-1]))
        j = int(np.clip(np.searchsorted(self.thetas, theta, side='right') - 1,
                        0, len(self.thetas) - 2))
        t0, t1 = self.thetas[j], self.thetas[j + 1]
        b = 0.0 if t1 == t0 else (theta - t0) / (t1 - t0)

        # Wrap query angle to the pattern's phi convention and interpolate
        # periodically across the last/first azimuth sample.
        phi = float(phi_deg) % 360.0
        phis = self.phis
        if len(phis) >= 2 and (phis[-1] - phis[0]) >= 359.999:
            phi = phis[0] + ((phi - phis[0]) % 360.0)

        if phi < phis[0] or phi > phis[-1]:
            i0, i1 = len(phis) - 1, 0
            p0, p1 = phis[-1], phis[0] + 360.0
            q = phi if phi >= p0 else phi + 360.0
            a = (q - p0) / (p1 - p0)
        else:
            i0 = int(np.clip(np.searchsorted(phis, phi, side='right') - 1,
                             0, len(phis) - 2))
            i1 = i0 + 1
            p0, p1 = phis[i0], phis[i1]
            a = 0.0 if p1 == p0 else (phi - p0) / (p1 - p0)

        f00, f10 = field[i0, j], field[i1, j]
        f01, f11 = field[i0, j + 1], field[i1, j + 1]
        return ((1-a)*(1-b)*f00 + a*(1-b)*f10 +
                (1-a)*b*f01 + a*b*f11)

    def update_pattern(self):
        # Platform axes: +X forward, +Y azimuth, +Z elevation.
        az = np.deg2rad(self._azm_deg)
        el = np.deg2rad(self._elev_deg)

        # Global: X = ileri, Y = sağ, Z = yukarı
        # CST: local Z = global X
        #      local X = global Y
        #      local Y = global Z

        local_x = np.cos(el) * np.sin(az)
        local_y = np.sin(el)
        local_z = np.cos(el) * np.cos(az)

        theta = np.rad2deg(
            np.arccos(np.clip(local_z, -1.0, 1.0))
        )

        phi = np.rad2deg(
            np.arctan2(local_y, local_x)
        ) % 360.0

        e_th = self._interpolate_phi_theta(self.e_theta, phi, theta)
        e_ph = self._interpolate_phi_theta(self.e_phi, phi, theta)

        # Target Jones polarization in the local (e_theta, e_phi) basis.
        alpha = np.deg2rad(self._pol_angle_deg)
        chi = np.deg2rad(np.clip(self._ellipticity_deg, -45.0, 45.0))
        j_th = np.cos(chi) * np.cos(alpha) - 1j * np.sin(chi) * np.sin(alpha)
        j_ph = np.cos(chi) * np.sin(alpha) + 1j * np.sin(chi) * np.cos(alpha)

        # Preserve the original block's scalar receive-response convention.
        self.h = np.complex64(e_th * j_th + e_ph * j_ph)

    def work(self, input_items, output_items):
        n = min(len(input_items[0]), len(output_items[0]))
        output_items[0][:n] = input_items[0][:n] * self.h
        return n
