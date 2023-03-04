#!/usr/bin/env python3

import math
import random
import subprocess
import threading
from datetime import datetime
from typing import List, Union

from eviltransform import gcj2wgs_exact
from geopy import Point
from geopy.distance import distance


def log(*args: str):
    print(f"{datetime.now().strftime('[%T]')} {' '.join(args)}")


class IDeviceError(Exception):
    def __init__(self, code: int):
        super().__init__()
        self.code = code

    def __repr__(self):
        return f"{self.__class__.__name__}({self.code})"

    def __str__(self):
        return repr(self)


class Runner:
    def __init__(self,
                 routes: List[Point],
                 walk_speed: float = 1.414,
                 position_errors: float = 8.0,
                 is_network=True,
                 auto_start=True):
        self.is_network = is_network
        # 单位为米
        self.walk_speed = walk_speed
        self.position_errors = position_errors

        # 第一个路径为起点，后面为路径点
        self.curr: Point = routes[0]
        self.dest: Point = self.curr
        self.routes = routes[1:]

        self.timer: threading.Timer = threading.Timer(0.1, self.run)
        if auto_start:
            self.timer.start()

    def set_location(self, arg: Union[str, Point]):
        args = ["idevicesetlocation"]
        if self.is_network:
            args.append("-n")
        if isinstance(arg, Point):
            args.extend([
                str(arg.latitude),
                str(arg.longitude),
            ])
        else:
            args.append(arg)
        exec_st = datetime.now()
        process = subprocess.run(args, check=False)
        if process.returncode != 0:
            raise IDeviceError(process.returncode)
        exec_et = datetime.now()
        return exec_et - exec_st

    def run(self):
        if len(self.routes) >= 1 and \
                distance(self.curr, self.dest).meters <= self.position_errors:
            self.dest = self.routes.pop(0)
            log(f"ROUTE next={self.dest}")

        full_distance = distance(self.curr, self.dest).meters
        move_distance = self.walk_speed * self.timer.interval
        if full_distance < 1e-10 or move_distance > full_distance:
            move_distance = full_distance
        move_angle = math.degrees(math.atan2(
            self.dest.longitude - self.curr.longitude,
            self.dest.latitude - self.curr.latitude,
        ))
        next_point = distance(meters=move_distance).destination(self.curr, move_angle)

        error_meter = random.uniform(0, self.position_errors)
        error_angle = random.uniform(0, 360)
        next_point = distance(meters=error_meter).destination(next_point, error_angle)

        exec_time = self.set_location(next_point)
        move_meters = distance(self.curr, next_point).meters
        move_time = self.timer.interval + exec_time.total_seconds()
        log("MOVE",
            f"distance={move_meters:05.2f}",
            f"seconds={move_time:05.2f}",
            f"speed={move_meters / move_time:05.2f}",
            f"remaining={distance(next_point, self.dest).meters:.2f}")

        self.curr = next_point
        self.timer = threading.Timer(random.uniform(4, 10), self.run)
        self.timer.start()

    def stop(self):
        self.timer.cancel()

    def reset(self):
        self.timer.cancel()
        self.set_location("reset")

    def d(self, dlat, dlng):
        lat = dlat * 0.00001 + self.curr.latitude
        lng = dlng * 0.00001 + self.curr.longitude
        self.dest = self.curr
        self.routes = [Point(lat, lng)]
    
    def w(self, lat, lng):
        self.routes.append(Point(lat, lng))
    
    def g(self, lat, lng):
        t.routes.append(*gcj2wgs_exact(lat, lng))


route_1 = [     # 大厦-cocopark-皇庭广场-市民公园-大厦
    Point(22.543342468029227, 114.04765957173028),
    Point(22.53558157203738 , 114.04803322216428),
    Point(22.53558643704284 , 114.0535374515977 ),
    Point(22.539395687463674, 114.05345317631784),
    Point(22.539668120273856, 114.05147797437459),
    Point(22.542261069692422, 114.05145690555162),
    Point(22.542192962828736, 114.04781199954613),
    Point(22.543342468029227, 114.04765957173028),
]
route_2 = [     # 大厦-儿童医院-少年宫-市民广场-基金大厦-大厦
    Point(22.543448601507688, 114.04760541432175),
    Point(22.55117743283224 , 114.04761614314447),
    Point(22.55167285602734 , 114.05742229923264),
    Point(22.545618663225568, 114.05772270663684),
    Point(22.547540972505242, 114.05131759161401),
    Point(22.543438692460967, 114.05073823442572),
    Point(22.543448601507688, 114.04760541432175),
]
route_ds = [    # 大厦
    Point(22.54346852223365, 114.0475112247368),
]
route_mj = [    # 名居
    Point(22.54706748688649, 114.12931812266417),
]
route_ng = [    # 泥岗
    Point(22.57021189198253, 114.09167472401523)
]

if __name__ == "__main__":
    t = Runner(route_mj, is_network=False)
