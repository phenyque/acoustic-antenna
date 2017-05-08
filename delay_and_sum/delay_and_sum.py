import numpy as np
from copy import deepcopy

from .signal_processing import SignalProcessor
from ._helper import SPEED_OF_SOUND, TO_RAD

class DelayAndSumPlane:
    """
    Offers methods for the delay and sum algorithm to realise
    an acoustical antenna. This implementation assumes plane waves.
    """

    def __init__(self, delta_x, num_mics, signal_processor=None):
        self._delta_x = delta_x
        self._num_mics = num_mics
        if signal_processor is None:
            self._sp = SignalProcessor()


    def __repr__(self):
        desc = "<DelayAndSum Object with {nm} mics with distance of {dx}>"
        return desc.format(nm=self._num_mics, dx=self._delta_x)


    def delta_t_for_angle(self, angle):
        """
        Computes time delay between two adjacent microphones

        angle: angle of incoming wave in degrees
        delta_x: distance between the microphones in meters
        """
        return self._delta_x * np.sin(TO_RAD * angle) / SPEED_OF_SOUND


    def make_rms_list(signals, start_angle=-90, stop_angle=90, angle_steps=1):
        """
        Perform delay & sum algorithm for a given set of microphone signals
        to compute an array of rms values for the angles from -90 to 90 degrees
        """
        # TODO: error checking and stuff

        rms_values = []
        delay_if_pos = lambda n: self._num_mics - n
        delay_if_neg = lambda n: n - 1

        # go through all angles and delay and sum
        for angle in range(start_angle, stop_angle + 1, angle_steps):
            signals_tmp = deepcopy(signals)
            delta_t = self.delta_t_for_angle(angle)

            # set up things for signal delaying
            do_delay = True
            if delta_t > 0:
                delay_for_mic = delay_if_pos
            elif delta_t < 0:
                delay_for_mic = delay_if_neg
            else:
                do_delay = False

            if do_delay:
                for n in range(1, self._num_mics + 1):
                    # compute delay in samples
                    delay = (int) (np.round(delay_for_mic(n) * delta_t))
                    self._sp.delay_signals(signals_tmp[:,n], delay)

            # sum up everything and add rms value of sum to the list
            rms_values.append(self._sp.get_rms(signals_tmp.sum(1)))

        return rms_list
