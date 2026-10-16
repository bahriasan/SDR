"""GNU Radio UDP telemetry sender (3 float streams AZ, EL, FIT)."""
import socket
import struct
import threading
import time

import numpy as np
from gnuradio import gr

PACKET = struct.Struct('<4sB5f')


class udp_aoa_sender(gr.sync_block):
    """Send latest AoA and target angles via UDP, at most send_hz times/s."""

    def __init__(self, true_az_deg=0.0, true_el_deg=0.0,
                 host='127.0.0.1', port=50100, send_hz=10.0):
        gr.sync_block.__init__(
            self, name='UDP AoA Telemetry Sender',
            in_sig=[np.float32, np.float32, np.float32], out_sig=None
        )
        self._lock = threading.Lock()
        self._true_az = float(true_az_deg)
        self._true_el = float(true_el_deg)
        self._destination = (str(host), int(port))
        self._period = 1.0 / max(0.1, float(send_hz))
        self._next_send = 0.0
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.setblocking(False)
        self._packets_sent = 0
        self._packets_dropped = 0

    def set_true_az_deg(self, value):
        with self._lock:
            self._true_az = float(value)

    def set_true_el_deg(self, value):
        with self._lock:
            self._true_el = float(value)

    def work(self, input_items, output_items):
        n = min(len(x) for x in input_items)
        if not n:
            return 0
        now = time.monotonic()
        if now >= self._next_send:
            with self._lock:
                true_az, true_el = self._true_az, self._true_el
            az = float(input_items[0][n - 1])
            el = float(input_items[1][n - 1])
            fit = float(input_items[2][n - 1])
            if np.isfinite([true_az, true_el, az, el, fit]).all():
                payload = PACKET.pack(b'AOA1', 1, true_az, true_el, az, el, fit)
                try:
                    self._socket.sendto(payload, self._destination)
                    self._packets_sent += 1
                except (BlockingIOError, OSError):
                    self._packets_dropped += 1
            self._next_send = now + self._period
        return n

    def stop(self):
        self._socket.close()
        return True
