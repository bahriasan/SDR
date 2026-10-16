
import numpy as np
from gnuradio import gr


class blk(gr.decim_block):
    def __init__(self, window_size=4096):
        self.window_size = int(window_size)

        if self.window_size <= 0:
            raise ValueError("window_size must be positive")

        gr.decim_block.__init__(
            self,
            name="SNR Meter Optimized",
            in_sig=[np.complex64, np.complex64],
            out_sig=[np.float32],
            decim=self.window_size
        )

    def work(self, input_items, output_items):
        signal = input_items[0]
        noise = input_items[1]
        output = output_items[0]

        n_windows = min(
            len(output),
            len(signal) // self.window_size,
            len(noise) // self.window_size
        )

        if n_windows == 0:
            return 0

        n = n_windows * self.window_size

        s = signal[:n].reshape(n_windows, self.window_size)
        w = noise[:n].reshape(n_windows, self.window_size)

        # |x|^2 = Re(x)^2 + Im(x)^2
        signal_power = np.sum(
            s.real * s.real + s.imag * s.imag,
            axis=1,
            dtype=np.float64
        ) / self.window_size

        noise_power = np.sum(
            w.real * w.real + w.imag * w.imag,
            axis=1,
            dtype=np.float64
        ) / self.window_size

        with np.errstate(divide="ignore", invalid="ignore"):
            output[:n_windows] = (
                10.0 * np.log10(signal_power / noise_power)
            ).astype(np.float32)

        return n_windows
