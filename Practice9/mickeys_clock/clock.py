import datetime

def get_angles():
    now = datetime.datetime.now()
    h = now.hour % 12
    m = now.minute
    s = now.second
    minutes_angle = -(m * 6 + s * 0.1)
    hours_angle = -(h * 30 + m * 0.5)
    return minutes_angle, hours_angle