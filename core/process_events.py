"""
Module containing the process_events() function.
"""

__author__ = "Brett Duncan"
__email__ = "dunca384@umn.edu"


from typing import List, Optional, Tuple

from core.events import StageStop, ControlStop, StartOfDay, EndOfDay, StartGridCharge, EndGridCharge
from core.objects import RaceActions, State


# It would be better to split this up into RaceState and RaceActions
# RaceActions would be determined from the RaceState


def process_events(distance_queue: List,
                   time_queue: List,
                   state: State,
                   race_state: RaceActions,
                   checkpoint_time_remaining: float) -> Optional[Tuple[RaceActions, float]]:
    """
    Handle events that have happened in the past or at the current distance/time.

    :param distance_queue: List containing distance based events.
    :param time_queue: List containing time based events.
    :param state: Current state.
    :param race_state: Current race actions.
    :param checkpoint_time_remaining: Time remaining at the current checkpoint.

    :return: Optional tuple of race actions and checkpoint time remaining.
    """

    while len(distance_queue) > 0 and state.distance >= distance_queue[0].distance:
        event = distance_queue.pop(0)
        if isinstance(event, StageStop):
            if state.time <= event.target_arrival:
                race_state = RaceActions(clock_running=False,
                                         charging=True,
                                         driving=False,
                                         normalized=True,
                                         grid_charging=False,
                                         race_hours=False)
            elif state.time <= event.latest_arrival:
                # TODO: add lateness to stats for scoring
                race_state = RaceActions(clock_running=False,
                                         charging=True,
                                         driving=False,
                                         normalized=True,
                                         grid_charging=False,
                                         race_hours=False)
            else:
                # Too late to the stage stop
                print('Too late to stage stop')
                return None
        elif isinstance(event, ControlStop):
            if state.time <= event.latest_arrival:
                checkpoint_time_remaining = event.duration
                race_state = RaceActions(clock_running=False,
                                         charging=True,
                                         driving=False,
                                         normalized=True,
                                         grid_charging=False,
                                         race_hours=True)
            else:
                # Too late to checkpoint -> TODO: change this for ASC
                print('Too late to checkpoint')
                return None
        else:
            raise NotImplementedError()

    while len(time_queue) > 0 and state.time >= time_queue[0].time:
        event = time_queue.pop(0)
        if isinstance(event, StartOfDay):
            # Waiting at the checkpoint at the beginning of the day is handle external to this
            # should we handle this here?
            race_state = RaceActions(clock_running=True,
                                     charging=True,
                                     driving=True,
                                     normalized=False,
                                     grid_charging=False,
                                     race_hours=True)
        elif isinstance(event, EndOfDay):
            race_state = RaceActions(clock_running=False,
                                     charging=True,
                                     driving=False,
                                     normalized=True,
                                     grid_charging=False,
                                     race_hours=False)
        elif isinstance(event, StartGridCharge):
            race_state = RaceActions(clock_running=race_state.clock_running,
                                     charging=race_state.charging,
                                     driving=race_state.driving,
                                     normalized=race_state.normalized,
                                     grid_charging=True,
                                     race_hours=race_state.race_hours)
        elif isinstance(event, EndGridCharge):
            race_state = RaceActions(clock_running=race_state.clock_running,
                                     charging=race_state.charging,
                                     driving=race_state.driving,
                                     normalized=race_state.normalized,
                                     grid_charging=False,
                                     race_hours=race_state.race_hours)
        else:
            raise NotImplementedError()

    return race_state, checkpoint_time_remaining
