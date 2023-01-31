
from core.events import *
from core.units import date, distance, duration, speed
from core.race import Race


__author__ = "Brett Duncan"
__email__ = "dunca384@umn.edu"


distance_events = [
    ControlStop(name='Control Stop Katherine',
                distance=distance(316.0, unit='km'),
                duration=duration(30.0, unit='min'),
                latest_arrival=date('2021-10-18T14:30:00+09:30')
                ),
    ControlStop(name='Control Stop Dunmarra',
                distance=distance(631.0, unit='km'),
                duration=duration(30.0, unit='min'),
                latest_arrival=date('2021-10-18T14:30:00+09:30')
                ),
    StageStop(name='Stage 1 End - Tennant Creek',
              distance=distance(988.0, unit='km'),
              target_arrival=date('2021-10-18T14:30:00+09:30'),
              latest_arrival=date('2021-10-18T14:30:00+09:30')
              ),
    ControlStop(name='Control Stop Barrow Creek',
                distance=distance(1211.0, unit='km'),
                duration=duration(30.0, unit='min'),
                latest_arrival=date('2021-10-18T14:30:00+09:30')
                ),
    ControlStop(name='Control Stop Alice Springs',
                distance=distance(1495.0, unit='km'),
                duration=duration(30.0, unit='min'),
                latest_arrival=date('2021-10-18T14:30:00+09:30')
                ),
    ControlStop(name='Control Stop Kulgera',
                distance=distance(1769.0, unit='km'),
                duration=duration(30.0, unit='min'),
                latest_arrival=date('2021-10-18T14:30:00+09:30')
                ),
    StageStop(name='Stage 2 End - Coober Pedy',
              distance=distance(2182.0, unit='km'),
              target_arrival=date('2021-10-18T14:30:00+09:30'),
              latest_arrival=date('2021-10-18T14:30:00+09:30')
              ),
    ControlStop(name='Control Stop Glendambo',
                distance=distance(2436.0, unit='km'),
                duration=duration(30.0, unit='min'),
                latest_arrival=date('2021-10-18T14:30:00+09:30')
                ),
    ControlStop(name='Control Stop Port Augusta',
                distance=distance(2722.0, unit='km'),
                duration=duration(30.0, unit='min'),
                latest_arrival=date('2021-10-18T14:30:00+09:30')
                ),
    StageStop(name='Stage 3 End - Adelaide',
              distance=distance(3022.0, unit='km'),
              target_arrival=date('2021-10-18T14:30:00+09:30'),
              latest_arrival=date('2021-10-18T14:30:00+09:30')
              ),
]


time_events = [
    StartOfDay(name='Day 1 Start',
               time=date('2021-10-13T08:30:00+09:30')
               ),
    EndOfDay(name='Day 1 End',
             time=date('2021-10-13T17:00:00+09:30')
             ),
    StartOfDay(name='Day 2 Start',
               time=date('2021-10-14T08:00:00+09:30')
               ),
    EndOfDay(name='Day 2 End',
             time=date('2021-10-14T17:00:00+09:30')
             ),
    StartGridCharge(time=date('2021-10-14T18:39:00+09:30')),
    EndGridCharge(time=date('2021-10-14T23:00:00+09:30')),
    StartOfDay(name='Day 3 Start',
               time=date('2021-10-15T08:00:00+09:30')
               ),
    EndOfDay(name='Day 3 End',
             time=date('2021-10-15T17:00:00+09:30')
             ),
    StartOfDay(name='Day 4 Start',
               time=date('2021-10-16T08:00:00+09:30')
               ),
    EndOfDay(name='Day 4 End',
             time=date('2021-10-16T17:00:00+09:30')
             ),
    StartGridCharge(time=date('2021-10-16T18:45:00+09:30')),
    EndGridCharge(time=date('2021-10-16T23:00:00+09:30')),
    StartOfDay(name='Day 5 Start',
               time=date('2021-10-17T08:00:00+09:30')
               ),
    EndOfDay(name='Day 5 End',
             time=date('2021-10-17T17:00:00+09:30')
             ),
    StartOfDay(name='Day 6 Start',
               time=date('2021-10-18T08:00:00+09:30')
               ),
    EndOfDay(name='Day 6 End',
             time=date('2021-10-18T23:59:59+09:30')
             ),
]


speed_limits = [
    SpeedLimit(distance=0.0, speed_limit=speed(100.0, unit='km/h'))
]


wsc_2023 = Race(distance_events=distance_events,
                time_events=time_events, speed_limits=speed_limits, route=None)
