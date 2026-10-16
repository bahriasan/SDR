"""3D CST AoA visualizer: measured single-element radiation patterns and AoA arrows.

CST geometry: local Z = global X (forward), local X = global Y (right),
local Y = global Z (up). Patterns use |E| = sqrt(|Etheta|^2+|Ephi|^2).
All four patterns use ONE shared magnitude scale (no per-element normalization).
Rendered radius and element separation are schematic display scales, not meters.
"""
import socket
import struct
import time
from pathlib import Path

import numpy as np
from PyQt5 import QtCore, QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

DEFAULT_ANTENNA_DIR = 'C:/SDR/WS/SDR_generic/antenna'
DEFAULT_NAMES = {
    channel: f'c5_klasik_1_{channel}_1575.42MHz_gerceklesen_kazanc.txt'
    for channel in ('UL', 'UR', 'LL', 'LR')
}


def direction(az_deg, el_deg):
    az = np.deg2rad(az_deg)
    el = np.deg2rad(el_deg)
    return np.array([np.cos(el) * np.cos(az),
                     np.cos(el) * np.sin(az),
                     np.sin(el)], dtype=np.float64)


def load_cst_surface(path, angular_step=6):
    """Load 8-column CST values and return a reduced-resolution mesh and amplitude."""
    data = np.loadtxt(str(path), skiprows=2)
    if data.shape != (361 * 181, 8):
        raise ValueError(f'Expected 361*181 rows, 8 columns in {path}; got {data.shape}')
    if not (np.isclose(data[0, 0], 0) and np.isclose(data[0, 1], 0)
            and np.isclose(data[180, 0], 180) and np.isclose(data[181, 1], 1)):
        raise ValueError(f'Unexpected phi/theta order in CST file: {path}')

    step = max(1, int(angular_step))
    pi = np.unique(np.r_[np.arange(0, 361, step), 360])
    ti = np.unique(np.r_[np.arange(0, 181, step), 180])

    shape = (361, 181)
    th_db = data[:, 3].reshape(shape)[np.ix_(pi, ti)]
    ph_db = data[:, 5].reshape(shape)[np.ix_(pi, ti)]
    # No phase needed for total-field radiation-magnitude surface;
    # phases are retained in the CST files for the AoA estimator itself.
    magnitude = np.sqrt(10.0 ** (th_db / 10.0) + 10.0 ** (ph_db / 10.0))
    phi = np.deg2rad(pi.astype(float))[:, None]
    theta = np.deg2rad(ti.astype(float))[None, :]

    # CST local XYZ -> scene global XYZ
    gx = np.broadcast_to(np.cos(theta), magnitude.shape)
    gy = np.sin(theta) * np.cos(phi)
    gz = np.sin(theta) * np.sin(phi)
    return (gx, gy, gz), magnitude


class DOAWindow(QtWidgets.QWidget):
    def __init__(self, owner):
        super().__init__()
        self.owner = owner
        self.setWindowTitle('3D CST AoA Visualizer - Measured Patterns')
        self.resize(1100, 850)

        self.figure = Figure(figsize=(10, 8), dpi=100)
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.ax = self.figure.add_subplot(111, projection='3d')
        self.ax.view_init(elev=22, azim=-65)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.canvas)

        # Antenna positions enlarged for readability (not physical coordinates).
        d = 0.14
        self.positions = {
            'UL': (0.0, +d, +d),
            'UR': (0.0, -d, +d),
            'LL': (0.0, +d, -d),
            'LR': (0.0, -d, -d),
        }
        self.colors = {'UL': '#2563eb', 'UR': '#eab308',
                       'LL': '#a855f7', 'LR': '#06b6d4'}

        meshes = {}
        for ch, path in owner.pattern_paths.items():
            meshes[ch] = load_cst_surface(path, owner.pattern_step_deg)
        common_peak = max(float(np.nanmax(amplitude)) for _, amplitude in meshes.values())
        if not np.isfinite(common_peak) or common_peak <= 0:
            raise ValueError('CST radiation field magnitudes are invalid')
        self.pattern_meshes = {}
        for ch, (unit_xyz, amplitude) in meshes.items():
            radius = owner.pattern_scale * amplitude / common_peak
            center = np.array(self.positions[ch], dtype=np.float64)
            self.pattern_meshes[ch] = tuple(center[i] + radius * unit_xyz[i] for i in range(3))

        # Static artists are created ONCE. Never clear the Axes in the timer.
        self._draw_static_scene()
        self._dynamic_artists = []
        self._last_render_state = None

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.redraw)
        self.timer.start(max(100, int(1000.0 / owner.update_hz)))
        self.redraw()

    def closeEvent(self, event):
        self.timer.stop()
        super().closeEvent(event)

    def _draw_static_scene(self):
        ax = self.ax
        for vector, label in (([1, 0, 0], 'X Forward'),
                              ([0, 1, 0], 'Y Right'),
                              ([0, 0, 1], 'Z Up')):
            ax.quiver(0, 0, 0, *vector, length=0.85, color='#64748b',
                      linewidth=1.5, arrow_length_ratio=0.08)
            p = np.asarray(vector) * 0.98
            ax.text(*p, label, fontsize=9)

        for name, mesh in self.pattern_meshes.items():
            ax.plot_surface(*mesh, color=self.colors[name], alpha=0.24,
                            linewidth=0, antialiased=False, shade=True,
                            rstride=1, cstride=1)
            x, y, z = self.positions[name]
            ax.scatter([x], [y], [z], color=self.colors[name], s=60,
                       depthshade=False)
            ax.text(x, y, z + 0.045, name, fontsize=10, weight='bold')

        ax.set(xlim=(-1.1, 1.1), ylim=(-1.1, 1.1), zlim=(-1.1, 1.1),
               xlabel='X / Forward', ylabel='Y / Right', zlabel='Z / Up')
        ax.set_box_aspect((1, 1, 1))

    def _draw_arrow(self, vector, color, label, length):
        arrow = self.ax.quiver(0, 0, 0, *vector, length=length,
                               normalize=True, color=color, linewidth=2.8,
                               arrow_length_ratio=0.12)
        p = vector * (length + 0.08)
        text = self.ax.text(*p, label, color=color, fontsize=10, weight='bold')
        self._dynamic_artists.extend((arrow, text))

    def redraw(self):
        # GNU Radio's work() only updates these scalar values.
        true_az, true_el = self.owner._true_az, self.owner._true_el
        est_az, est_el = self.owner._est_az, self.owner._est_el
        has_data = self.owner._has_data

        # No artist changes when telemetry has not changed. In particular,
        # mouse camera rotation remains under Matplotlib's own event handler.
        state = (true_az, true_el, est_az, est_el, has_data)
        if state == self._last_render_state:
            return
        self._last_render_state = state

        # Remove ONLY the moving arrows and texts, keeping four CST surfaces.
        for artist in self._dynamic_artists:
            artist.remove()
        self._dynamic_artists.clear()

        target_vector = direction(true_az, true_el)
        self._draw_arrow(target_vector, '#ef4444', 'TARGET', length=0.95)
        if has_data:
            estimated_vector = direction(est_az, est_el)
            self._draw_arrow(estimated_vector, '#16a34a', 'ESTIMATE', length=0.92)
            dot = np.clip(np.dot(target_vector, estimated_vector), -1, 1)
            error = float(np.rad2deg(np.arccos(dot)))
            detail = f'Estimate: AZ={est_az:.1f} EL={est_el:.1f} | 3D Error={error:.2f} deg'
        else:
            detail = 'Waiting for AoA estimates...'

        self.ax.set_title(f'Target: AZ={true_az:.1f} EL={true_el:.1f} | FIT={self.owner._fit:.3f}\n{detail}',
                          fontsize=12, pad=20)
        self.canvas.draw_idle()



PACKET = struct.Struct('<4sB5f')


class UDPVisualizer(QtCore.QObject):
    """Standalone telemetry state. All socket/Qt/Matplotlib calls run in Qt GUI thread."""

    def __init__(self, host='127.0.0.1', port=50100,
                 pattern_dir=DEFAULT_ANTENNA_DIR, pattern_step_deg=6,
                 pattern_scale=0.30, update_hz=5.0):
        super().__init__()
        self._true_az = 0.0
        self._true_el = 0.0
        self._est_az = 0.0
        self._est_el = 0.0
        self._fit = 0.0
        self._has_data = False
        self.update_hz = max(0.1, float(update_hz))
        self.pattern_step_deg = max(1, int(pattern_step_deg))
        self.pattern_scale = max(0.01, float(pattern_scale))
        self.pattern_paths = {
            ch: Path(pattern_dir) / name for ch, name in DEFAULT_NAMES.items()
        }

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setblocking(False)
        self.socket.bind((host, int(port)))
        self.packets_received = 0
        self._last_stats = time.monotonic()
        self._last_count = 0

        self.window = DOAWindow(self)
        self.window.setWindowTitle('UDP 3D CST AoA Visualizer - Measured Patterns')
        self.window.destroyed.connect(self.shutdown)
        self.poll_timer = QtCore.QTimer(self)
        self.poll_timer.timeout.connect(self.poll_udp)
        self.poll_timer.start(20)

    def poll_udp(self):
        # No threads needed; drain queued datagrams and keep only the newest.
        newest = None
        while True:
            try:
                payload, _ = self.socket.recvfrom(4096)
            except (BlockingIOError, OSError):
                break
            if len(payload) != PACKET.size:
                continue
            magic, version, true_az, true_el, az, el, fit = PACKET.unpack(payload)
            if magic != b'AOA1' or version != 1:
                continue
            if not np.isfinite([true_az, true_el, az, el, fit]).all():
                continue
            newest = (true_az, true_el, az, el, fit)
            self.packets_received += 1
        if newest is not None:
            self._true_az, self._true_el, self._est_az, self._est_el, self._fit = newest
            self._has_data = True
        now = time.monotonic()
        if now - self._last_stats >= 5.0:
            rate = (self.packets_received - self._last_count) / (now - self._last_stats)
            self.window.setWindowTitle(f'UDP 3D CST AoA Visualizer | RX {rate:.1f} pkt/s')
            self._last_stats = now
            self._last_count = self.packets_received

    def shutdown(self, *_):
        self.poll_timer.stop()
        self.socket.close()


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Independent 3D CST AoA UDP visualizer')
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=50100)
    parser.add_argument('--pattern-dir', default=DEFAULT_ANTENNA_DIR)
    parser.add_argument('--pattern-step', type=int, default=6)
    parser.add_argument('--pattern-scale', type=float, default=0.30)
    parser.add_argument('--update-hz', type=float, default=5.0)
    args = parser.parse_args()
    app = QtWidgets.QApplication([])
    receiver = UDPVisualizer(args.host, args.port, args.pattern_dir,
                             args.pattern_step, args.pattern_scale, args.update_hz)
    receiver.window.show()
    app.aboutToQuit.connect(receiver.shutdown)
    app.exec_()

if __name__ == '__main__':
    main()
