"""GNU Radio OOT Python Block: 4-channel unknown-polarization CST AoA.

Four input complex streams in UL, UR, LL, LR order.
Three output float streams: estimated azimuth, elevation, normalized fit (0..1).
The block decimates by window_size. For useful GUI rate feed reduced-rate streams
(e.g. <=100 ksample/s); the physical RF center frequency is 1575.42 MHz.
"""
import numpy as np
from gnuradio import gr
from scipy.ndimage import map_coordinates
import time


class aoa_estimator(gr.decim_block):
    def __init__(self,
                 pattern_UL='C:/SDR/WS/SDR/SDR_generic/antenna/c5_klasik_1_UL_1575.42MHz_gerceklesen_kazanc.txt',
                 pattern_UR='C:/SDR/WS/SDR/SDR_generic/antenna/c5_klasik_1_UR_1575.42MHz_gerceklesen_kazanc.txt',
                 pattern_LL='C:/SDR/WS/SDR/SDR_generic/antenna/c5_klasik_1_LL_1575.42MHz_gerceklesen_kazanc.txt',
                 pattern_LR='C:/SDR/WS/SDR/SDR_generic/antenna/c5_klasik_1_LR_1575.42MHz_gerceklesen_kazanc.txt',
                 window_size=1024,
                 grid_step_deg=5,
                 max_abs_elevation=85):
        self.window_size = max(64, int(window_size))
        
        gr.decim_block.__init__(self,
                               name='4 Channel CST AoA - Unknown Polarization',
                               in_sig=[np.complex64]*4,
                               out_sig=[np.float32]*3,
                               decim=self.window_size)
        paths = [pattern_UL, pattern_UR, pattern_LL, pattern_LR]
        patterns = []
        for path in paths:
            data = np.loadtxt(path, skiprows=2)
            if data.shape != (361*181, 8):
                raise ValueError('Expected 361x181 8-column CST file: ' + path)
            # Rows in original export: phi outer loop, theta inner loop.
            if not (np.isclose(data[0, 0], 0) and np.isclose(data[0, 1], 0)
                    and np.isclose(data[180, 0], 180) and np.isclose(data[181, 1], 1)):
                raise ValueError('Unexpected CST theta/phi ordering: ' + path)
            e_theta = (10.0**(data[:, 3]/20.0) *
                       np.exp(1j*np.deg2rad(data[:, 4]))).reshape(361,181)
            e_phi = (10.0**(data[:, 5]/20.0) *
                     np.exp(1j*np.deg2rad(data[:, 6]))).reshape(361,181)
            patterns.append((e_theta, e_phi))
        self._patterns = patterns
        step = max(1, int(grid_step_deg))
        limit = min(89, max(1, int(max_abs_elevation)))
        az_values = np.arange(-90, 91, step, dtype=np.float64)
        el_values = np.arange(-limit, limit+1, step, dtype=np.float64)
        azmesh, elmesh = np.meshgrid(az_values, el_values)
        self._az_grid = azmesh.ravel().astype(np.float32)
        self._el_grid = elmesh.ravel().astype(np.float32)
        az = np.deg2rad(self._az_grid.astype(np.float64))
        el = np.deg2rad(self._el_grid.astype(np.float64))
        # CST local axes: x_local=global Y, y_local=global Z, z_local=global X.
        local_x = np.cos(el)*np.sin(az)
        local_y = np.sin(el)
        local_z = np.cos(el)*np.cos(az)
        theta = np.rad2deg(np.arccos(np.clip(local_z, -1, 1)))
        phi = np.rad2deg(np.arctan2(local_y, local_x)) % 360.0
        coords = np.vstack((phi,theta))
        response = np.empty((len(self._az_grid),4,2),dtype=np.complex128)
        for ch, (et,ep) in enumerate(patterns):
            for pol, field in enumerate((et,ep)):
                response[:,ch,pol] = (
                    map_coordinates(field.real, coords, order=1, mode='nearest') +
                    1j*map_coordinates(field.imag, coords, order=1, mode='nearest'))
        # The 2 columns of H form the possible (unknown) polarization responses.
        # Common scaling of *all four files* is irrelevant. Per-channel peak
        # normalization is NOT performed because it destroys gain ratios.
        q, _ = np.linalg.qr(response)
        self._q_h = np.ascontiguousarray(np.conjugate(q).transpose(0,2,1),dtype=np.complex64)
        self._q_h_flat = np.ascontiguousarray(self._q_h.reshape(-1, 4))
        
        self._last_az = 0.0
        self._last_el = 0.0
        self._last_fit = 0.0
        self._rate_t0 = time.perf_counter()
        self._rate_samples = 0

    def work(self, input_items, output_items):
        n_out = len(output_items[0])
        n = self.window_size
        for i in range(n_out):
            sl = slice(i*n,(i+1)*n)
            X = np.stack([input_items[ch][sl] for ch in range(4)],axis=0)
            # Unknown common waveform: estimate the dominant signal vector
            # from sample covariance, rather than averaging raw I/Q samples.
            cov = (X @ X.conj().T)/float(n)
            _,eigenvectors = np.linalg.eigh(cov)
            u = eigenvectors[:,-1].astype(np.complex64)
            projected = (self._q_h_flat @ u).reshape(-1, 2)
            scores = np.sum(np.abs(projected)**2,axis=1)
            index = int(np.argmax(scores))
            self._last_az = float(self._az_grid[index])
            self._last_el = float(self._el_grid[index])
            self._last_fit = float(np.clip(scores[index],0.0,1.0))
            output_items[0][i] = self._last_az
            output_items[1][i] = self._last_el
            output_items[2][i] = self._last_fit

        # Effective per-channel input throughput (not nominal SDR sample rate).
        self._rate_samples += n_out * self.window_size
        elapsed = time.perf_counter() - self._rate_t0
        if elapsed >= 2.0:
            actual_rate = self._rate_samples / elapsed
            aoa_rate = (self._rate_samples / self.window_size) / elapsed
            #print(f"ACTUAL INPUT RATE: {actual_rate / 1e6:.3f} MS/s | AoA/s: {aoa_rate:.1f}")
            self._rate_t0 = time.perf_counter()
            self._rate_samples = 0

        return n_out
