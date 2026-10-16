#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.10.12.0

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import analog
from gnuradio import blocks
from gnuradio import channels
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import sdr
import sip
import threading



class options_0(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "options_0")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)
        self.flowgraph_started = threading.Event()

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 20e6
        self.polarization_angle = polarization_angle = 0
        self.fc = fc = 1.575e9
        self.elipticity_angle = elipticity_angle = 0
        self.elevation_angle = elevation_angle = 55
        self.c = c = 299792458.0
        self.azimuth_angle = azimuth_angle = -30

        ##################################################
        # Blocks
        ##################################################

        self._polarization_angle_range = qtgui.Range(-90, 90, 1, 0, 200)
        self._polarization_angle_win = qtgui.RangeWidget(self._polarization_angle_range, self.set_polarization_angle, "'polarization_angle'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._polarization_angle_win)
        self._elipticity_angle_range = qtgui.Range(-45, 45, 1, 0, 200)
        self._elipticity_angle_win = qtgui.RangeWidget(self._elipticity_angle_range, self.set_elipticity_angle, "'elipticity_angle'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._elipticity_angle_win)
        self._elevation_angle_range = qtgui.Range(-90, 90, 1, 55, 200)
        self._elevation_angle_win = qtgui.RangeWidget(self._elevation_angle_range, self.set_elevation_angle, "'elevation_angle'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._elevation_angle_win)
        self._azimuth_angle_range = qtgui.Range(-90, 90, 1, -30, 200)
        self._azimuth_angle_win = qtgui.RangeWidget(self._azimuth_angle_range, self.set_azimuth_angle, "'azimuth_angle'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._azimuth_angle_win)
        self.sdr_cst_pattern_3 = sdr.cst_pattern("C:/SDR/WS/SDR/SDR_generic/antenna/c5_klasik_1_LR_1575.42MHz_gerceklesen_kazanc.txt", azimuth_angle, elevation_angle, polarization_angle, elipticity_angle)
        self.sdr_cst_pattern_2 = sdr.cst_pattern("C:/SDR/WS/SDR/SDR_generic/antenna/c5_klasik_1_LL_1575.42MHz_gerceklesen_kazanc.txt", azimuth_angle, elevation_angle, polarization_angle, elipticity_angle)
        self.sdr_cst_pattern_1 = sdr.cst_pattern("C:/SDR/WS/SDR/SDR_generic/antenna/c5_klasik_1_UR_1575.42MHz_gerceklesen_kazanc.txt", azimuth_angle, elevation_angle, polarization_angle, elipticity_angle)
        self.sdr_cst_pattern_0 = sdr.cst_pattern("C:/SDR/WS/SDR/SDR_generic/antenna/c5_klasik_1_UL_1575.42MHz_gerceklesen_kazanc.txt", azimuth_angle, elevation_angle, polarization_angle, elipticity_angle)
        self.sdr_aoa_visualizer_3d_0 = sdr.aoa_visualizer_3d(azimuth_angle, elevation_angle, 10.0, 1)
        self.sdr_aoa_estimator_0 = sdr.aoa_estimator('C:/SDR/WS/SDR/SDR_generic/antenna/c5_klasik_1_UL_1575.42MHz_gerceklesen_kazanc.txt', 'C:/SDR/WS/SDR/SDR_generic/antenna/c5_klasik_1_UR_1575.42MHz_gerceklesen_kazanc.txt', 'C:/SDR/WS/SDR/SDR_generic/antenna/c5_klasik_1_LL_1575.42MHz_gerceklesen_kazanc.txt', 'C:/SDR/WS/SDR/SDR_generic/antenna/c5_klasik_1_LR_1575.42MHz_gerceklesen_kazanc.txt', 1024, 1, 85)
        self.rational_resampler_xxx_0_2 = filter.rational_resampler_ccc(
                interpolation=3,
                decimation=25,
                taps=[],
                fractional_bw=0.4)
        self.rational_resampler_xxx_0_1 = filter.rational_resampler_ccc(
                interpolation=3,
                decimation=25,
                taps=[],
                fractional_bw=0.4)
        self.rational_resampler_xxx_0_0 = filter.rational_resampler_ccc(
                interpolation=3,
                decimation=25,
                taps=[],
                fractional_bw=0.4)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=3,
                decimation=25,
                taps=[],
                fractional_bw=0.4)
        self.qtgui_time_sink_x_0_0_0_1 = qtgui.time_sink_f(
            1024, #size
            586, #samp_rate
            "Azimuth", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_0_0_1.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0_0_1.set_y_axis(0, 360)

        self.qtgui_time_sink_x_0_0_0_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0_0_1.enable_tags(True)
        self.qtgui_time_sink_x_0_0_0_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0_0_1.enable_autoscale(True)
        self.qtgui_time_sink_x_0_0_0_1.enable_grid(True)
        self.qtgui_time_sink_x_0_0_0_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0_0_1.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0_0_1.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_0_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0_0_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0_0_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0_0_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0_0_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0_0_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_0_1_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0_0_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_0_0_1_win)
        self.qtgui_time_sink_x_0_0_0_0 = qtgui.time_sink_f(
            1024, #size
            586, #samp_rate
            "Elevation", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_0_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0_0_0.set_y_axis(0, 360)

        self.qtgui_time_sink_x_0_0_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0_0_0.enable_tags(True)
        self.qtgui_time_sink_x_0_0_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0_0_0.enable_autoscale(True)
        self.qtgui_time_sink_x_0_0_0_0.enable_grid(True)
        self.qtgui_time_sink_x_0_0_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0_0_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_0_0_0_win)
        self.qtgui_time_sink_x_0_0_0 = qtgui.time_sink_f(
            1024, #size
            586, #samp_rate
            "Fit Quality", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0_0.set_y_axis(0, 360)

        self.qtgui_time_sink_x_0_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0_0.enable_tags(True)
        self.qtgui_time_sink_x_0_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0_0.enable_autoscale(True)
        self.qtgui_time_sink_x_0_0_0.enable_grid(True)
        self.qtgui_time_sink_x_0_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_0_0_win)
        self.low_pass_filter_1_2 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                samp_rate,
                1e6,
                0.2e6,
                window.WIN_HAMMING,
                6.76))
        self.low_pass_filter_1_1 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                samp_rate,
                1e6,
                0.2e6,
                window.WIN_HAMMING,
                6.76))
        self.low_pass_filter_1_0 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                samp_rate,
                1e6,
                0.2e6,
                window.WIN_HAMMING,
                6.76))
        self.low_pass_filter_1 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                samp_rate,
                1e6,
                0.2e6,
                window.WIN_HAMMING,
                6.76))
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                samp_rate,
                9.5e6,
                0.5e6,
                window.WIN_HAMMING,
                6.76))
        self.channels_quantizer_1_2 = channels.quantizer(8)
        self.channels_quantizer_1_1 = channels.quantizer(8)
        self.channels_quantizer_1_0 = channels.quantizer(8)
        self.channels_quantizer_1 = channels.quantizer(8)
        self.channels_quantizer_0_2 = channels.quantizer(8)
        self.channels_quantizer_0_1 = channels.quantizer(8)
        self.channels_quantizer_0_0 = channels.quantizer(8)
        self.channels_quantizer_0 = channels.quantizer(8)
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_gr_complex*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_probe_rate_0 = blocks.probe_rate(gr.sizeof_gr_complex*1, 500.0, 0.15, "probeRate")
        self.blocks_float_to_complex_0_2 = blocks.float_to_complex(1)
        self.blocks_float_to_complex_0_1 = blocks.float_to_complex(1)
        self.blocks_float_to_complex_0_0 = blocks.float_to_complex(1)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_complex_to_real_0_2 = blocks.complex_to_real(1)
        self.blocks_complex_to_real_0_1 = blocks.complex_to_real(1)
        self.blocks_complex_to_real_0_0 = blocks.complex_to_real(1)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.blocks_complex_to_imag_0_2 = blocks.complex_to_imag(1)
        self.blocks_complex_to_imag_0_1 = blocks.complex_to_imag(1)
        self.blocks_complex_to_imag_0_0 = blocks.complex_to_imag(1)
        self.blocks_complex_to_imag_0 = blocks.complex_to_imag(1)
        self.blocks_add_xx_3 = blocks.add_vcc(1)
        self.blocks_add_xx_2 = blocks.add_vcc(1)
        self.blocks_add_xx_1 = blocks.add_vcc(1)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.analog_noise_source_x_1_2 = analog.noise_source_c(analog.GR_GAUSSIAN, 0, 0)
        self.analog_noise_source_x_1_1 = analog.noise_source_c(analog.GR_GAUSSIAN, 0, 0)
        self.analog_noise_source_x_1_0 = analog.noise_source_c(analog.GR_GAUSSIAN, 0, 0)
        self.analog_noise_source_x_1 = analog.noise_source_c(analog.GR_GAUSSIAN, 0, 0)
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, 1, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.analog_noise_source_x_1, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.analog_noise_source_x_1_0, 0), (self.blocks_add_xx_1, 0))
        self.connect((self.analog_noise_source_x_1_1, 0), (self.blocks_add_xx_2, 0))
        self.connect((self.analog_noise_source_x_1_2, 0), (self.blocks_add_xx_3, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_complex_to_imag_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.blocks_add_xx_1, 0), (self.blocks_complex_to_imag_0_0, 0))
        self.connect((self.blocks_add_xx_1, 0), (self.blocks_complex_to_real_0_0, 0))
        self.connect((self.blocks_add_xx_2, 0), (self.blocks_complex_to_imag_0_1, 0))
        self.connect((self.blocks_add_xx_2, 0), (self.blocks_complex_to_real_0_1, 0))
        self.connect((self.blocks_add_xx_3, 0), (self.blocks_complex_to_imag_0_2, 0))
        self.connect((self.blocks_add_xx_3, 0), (self.blocks_complex_to_real_0_2, 0))
        self.connect((self.blocks_complex_to_imag_0, 0), (self.channels_quantizer_1, 0))
        self.connect((self.blocks_complex_to_imag_0_0, 0), (self.channels_quantizer_1_0, 0))
        self.connect((self.blocks_complex_to_imag_0_1, 0), (self.channels_quantizer_1_1, 0))
        self.connect((self.blocks_complex_to_imag_0_2, 0), (self.channels_quantizer_1_2, 0))
        self.connect((self.blocks_complex_to_real_0, 0), (self.channels_quantizer_0, 0))
        self.connect((self.blocks_complex_to_real_0_0, 0), (self.channels_quantizer_0_0, 0))
        self.connect((self.blocks_complex_to_real_0_1, 0), (self.channels_quantizer_0_1, 0))
        self.connect((self.blocks_complex_to_real_0_2, 0), (self.channels_quantizer_0_2, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.sdr_aoa_estimator_0, 0))
        self.connect((self.blocks_float_to_complex_0_0, 0), (self.sdr_aoa_estimator_0, 1))
        self.connect((self.blocks_float_to_complex_0_1, 0), (self.sdr_aoa_estimator_0, 2))
        self.connect((self.blocks_float_to_complex_0_2, 0), (self.sdr_aoa_estimator_0, 3))
        self.connect((self.blocks_throttle2_0, 0), (self.blocks_probe_rate_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.channels_quantizer_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.channels_quantizer_0_0, 0), (self.blocks_float_to_complex_0_0, 0))
        self.connect((self.channels_quantizer_0_1, 0), (self.blocks_float_to_complex_0_1, 0))
        self.connect((self.channels_quantizer_0_2, 0), (self.blocks_float_to_complex_0_2, 0))
        self.connect((self.channels_quantizer_1, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.channels_quantizer_1_0, 0), (self.blocks_float_to_complex_0_0, 1))
        self.connect((self.channels_quantizer_1_1, 0), (self.blocks_float_to_complex_0_1, 1))
        self.connect((self.channels_quantizer_1_2, 0), (self.blocks_float_to_complex_0_2, 1))
        self.connect((self.low_pass_filter_0, 0), (self.low_pass_filter_1, 0))
        self.connect((self.low_pass_filter_0, 0), (self.low_pass_filter_1_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.low_pass_filter_1_1, 0))
        self.connect((self.low_pass_filter_0, 0), (self.low_pass_filter_1_2, 0))
        self.connect((self.low_pass_filter_1, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.low_pass_filter_1_0, 0), (self.rational_resampler_xxx_0_0, 0))
        self.connect((self.low_pass_filter_1_1, 0), (self.rational_resampler_xxx_0_1, 0))
        self.connect((self.low_pass_filter_1_2, 0), (self.rational_resampler_xxx_0_2, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.sdr_cst_pattern_0, 0))
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.sdr_cst_pattern_1, 0))
        self.connect((self.rational_resampler_xxx_0_1, 0), (self.sdr_cst_pattern_2, 0))
        self.connect((self.rational_resampler_xxx_0_2, 0), (self.sdr_cst_pattern_3, 0))
        self.connect((self.sdr_aoa_estimator_0, 2), (self.qtgui_time_sink_x_0_0_0, 0))
        self.connect((self.sdr_aoa_estimator_0, 1), (self.qtgui_time_sink_x_0_0_0_0, 0))
        self.connect((self.sdr_aoa_estimator_0, 0), (self.qtgui_time_sink_x_0_0_0_1, 0))
        self.connect((self.sdr_aoa_estimator_0, 1), (self.sdr_aoa_visualizer_3d_0, 1))
        self.connect((self.sdr_aoa_estimator_0, 0), (self.sdr_aoa_visualizer_3d_0, 0))
        self.connect((self.sdr_cst_pattern_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.sdr_cst_pattern_1, 0), (self.blocks_add_xx_1, 1))
        self.connect((self.sdr_cst_pattern_2, 0), (self.blocks_add_xx_2, 1))
        self.connect((self.sdr_cst_pattern_3, 0), (self.blocks_add_xx_3, 1))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "options_0")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 9.5e6, 0.5e6, window.WIN_HAMMING, 6.76))
        self.low_pass_filter_1.set_taps(firdes.low_pass(1, self.samp_rate, 1e6, 0.2e6, window.WIN_HAMMING, 6.76))
        self.low_pass_filter_1_0.set_taps(firdes.low_pass(1, self.samp_rate, 1e6, 0.2e6, window.WIN_HAMMING, 6.76))
        self.low_pass_filter_1_1.set_taps(firdes.low_pass(1, self.samp_rate, 1e6, 0.2e6, window.WIN_HAMMING, 6.76))
        self.low_pass_filter_1_2.set_taps(firdes.low_pass(1, self.samp_rate, 1e6, 0.2e6, window.WIN_HAMMING, 6.76))

    def get_polarization_angle(self):
        return self.polarization_angle

    def set_polarization_angle(self, polarization_angle):
        self.polarization_angle = polarization_angle
        self.sdr_cst_pattern_0.set_pol_angle_deg(self.polarization_angle)
        self.sdr_cst_pattern_1.set_pol_angle_deg(self.polarization_angle)
        self.sdr_cst_pattern_2.set_pol_angle_deg(self.polarization_angle)
        self.sdr_cst_pattern_3.set_pol_angle_deg(self.polarization_angle)

    def get_fc(self):
        return self.fc

    def set_fc(self, fc):
        self.fc = fc

    def get_elipticity_angle(self):
        return self.elipticity_angle

    def set_elipticity_angle(self, elipticity_angle):
        self.elipticity_angle = elipticity_angle
        self.sdr_cst_pattern_0.set_ellipticity_deg(self.elipticity_angle)
        self.sdr_cst_pattern_1.set_ellipticity_deg(self.elipticity_angle)
        self.sdr_cst_pattern_2.set_ellipticity_deg(self.elipticity_angle)
        self.sdr_cst_pattern_3.set_ellipticity_deg(self.elipticity_angle)

    def get_elevation_angle(self):
        return self.elevation_angle

    def set_elevation_angle(self, elevation_angle):
        self.elevation_angle = elevation_angle
        self.sdr_aoa_visualizer_3d_0.set_true_el_deg(self.elevation_angle)
        self.sdr_cst_pattern_0.set_elev_deg(self.elevation_angle)
        self.sdr_cst_pattern_1.set_elev_deg(self.elevation_angle)
        self.sdr_cst_pattern_2.set_elev_deg(self.elevation_angle)
        self.sdr_cst_pattern_3.set_elev_deg(self.elevation_angle)

    def get_c(self):
        return self.c

    def set_c(self, c):
        self.c = c

    def get_azimuth_angle(self):
        return self.azimuth_angle

    def set_azimuth_angle(self, azimuth_angle):
        self.azimuth_angle = azimuth_angle
        self.sdr_aoa_visualizer_3d_0.set_true_az_deg(self.azimuth_angle)
        self.sdr_cst_pattern_0.set_azm_deg(self.azimuth_angle)
        self.sdr_cst_pattern_1.set_azm_deg(self.azimuth_angle)
        self.sdr_cst_pattern_2.set_azm_deg(self.azimuth_angle)
        self.sdr_cst_pattern_3.set_azm_deg(self.azimuth_angle)




def main(top_block_cls=options_0, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()
    tb.flowgraph_started.set()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
