from DobotRPC import DobotlinkAdapter, RPCClient


class MagicianGoApi(object):
    def __init__(self):
        self.__dobotlink = DobotlinkAdapter(RPCClient(), is_sync=True)

    def set_running_mode(self, port_name, mode):
        return self.__dobotlink.MagicianGo.SetRunningMode(portName=port_name,
                                                          runningMode=mode)

    def set_direction_speed(self, port_name, direction, speed):
        return self.__dobotlink.MagicianGo.SetDirectionSpeed(
            portName=port_name, dir=direction, speed=speed)

    def set_move_speed(self, port_name, x, y, r):
        return self.__dobotlink.MagicianGo.SetMoveSpeed(portName=port_name,
                                                        x=x,
                                                        y=y,
                                                        r=r)

    def set_rotate_deg_speed(self, port_name, r, vr):
        return self.__dobotlink.MagicianGo.SetMoveDistance(portName=port_name,
                                                           r=r,
                                                           vr=vr)

    def set_xy_speed_distance(self, port_name, x, y, vx, vy):
        return self.__dobotlink.MagicianGo.SetFixedOrientationMoveDistance(
            portName=port_name, x=x, y=y, vx=vx, vy=vy)

    def moveto_destination(self, port_name, x, y, s):
        return self.__dobotlink.MagicianGo.SetWorldCoordinateMovePoint(
            portName=port_name, x=x, y=y, s=s)

    def move_radius_arc(self, port_name, velocity, radius, angle, mode):
        return self.__dobotlink.MagicianGo.SetTraceRadiusARC(
            portName=port_name,
            velocity=velocity,
            radius=radius,
            angle=angle,
            mode=mode)

    def move_circular_arc(self, port_name, velocity, radius, angle, mode):
        return self.__dobotlink.MagicianGo.SetTraceCenterARC(
            portName=port_name,
            velocity=velocity,
            radius=radius,
            angle=angle,
            mode=mode)

    def set_coord_closed_loop(self, port_name, enable, angle):
        return self.__dobotlink.MagicianGo.SetCoordClosedLoop(
            portName=port_name, enable=enable, angle=angle)

    def set_increment_closed_loop(self, port_name, x, y, angle):
        return self.__dobotlink.MagicianGo.SetIncrementClosedLoop(
            portName=port_name, x=x, y=y, angle=angle)

    def set_rgb_light(self, port_name, number, effect, r, g, b, cycle, counts):
        return self.__dobotlink.MagicianGo.SetLightRGB(portName=port_name,
                                                       number=number,
                                                       effect=effect,
                                                       r=r,
                                                       g=g,
                                                       b=b,
                                                       cycle=cycle,
                                                       counts=counts)

    def set_buzzer_sound(self, port_name, index, tone, beat):
        return self.__dobotlink.MagicianGo.SetBuzzerSound(portName=port_name,
                                                          index=index,
                                                          tone=tone,
                                                          beat=beat)

    def get_ultrasonic_data(self, port_name):
        return self.__dobotlink.MagicianGo.GetUltrasoundData(
            portName=port_name)

    def get_odometer_data(self, port_name):
        return self.__dobotlink.MagicianGo.GetSpeedometer(portName=port_name)

    def get_power_voltage(self, port_name):
        return self.__dobotlink.MagicianGo.GetBatteryVoltage(
            portName=port_name)

    def get_imu_angle(self, port_name):
        return self.__dobotlink.MagicianGo.GetTraceAngle(portName=port_name)

    def get_imu_acce_anglespeed(self, port_name):
        return self.__dobotlink.MagicianGo.GetImuAcceAnglespeed(
            portName=port_name)

    def set_auto_trace(self, port_name, trace):
        return self.__dobotlink.MagicianGo.SetTraceAuto(portName=port_name,
                                                        isTrace=trace)

    def set_trace_speed(self, port_name, speed):
        return self.__dobotlink.MagicianGo.SetTraceSpeed(portName=port_name,
                                                         speed=speed)

    def set_trace_pid(self, port_name, p, i, d):
        return self.__dobotlink.MagicianGo.SetTracePid(portName=port_name,
                                                       p=p,
                                                       i=i,
                                                       d=d)


# k210

    def get_k210_angle(self, port_name):
        return self.__dobotlink.MagicianGo.GetK210ArmAngleData(
            portName=port_name)

    def get_k210_deeplearning(self, port_name):
        return self.__dobotlink.MagicianGo.GetK210ArmDeepLearningObj(
            portName=port_name)

    def get_k210_apriltag(self, port_name):
        return self.__dobotlink.MagicianGo.GetK210ArmAprilTag(
            portName=port_name)
