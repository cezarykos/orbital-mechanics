import numpy as np
from astropy import units as u
from astropy import time
from poliastro.bodies import Sun
from poliastro.twobody import Orbit
from poliastro import iod


def transit_optimal(date, transit_min, transit_max, planet1, planet2, vs0, step):

    date_arrival = date + transit_min
    date_max = date + transit_max
    date_arrival_final = date_arrival

    vs22 = 0 * u.km / u.s
    dv_final = 0 * u.km / u.s
    step_one = True

    while date_arrival < date_max:
        tof = date_arrival - date
        date_iso = time.Time(str(date.iso), scale='utc')
        date_arrival_iso = time.Time(str(date_arrival.iso), scale='utc')

        r1= Orbit.from_body_ephem(planet1, date_iso)
        r2= Orbit.from_body_ephem(planet2, date_arrival_iso)
        r_1, v_1 = r1.rv()
        r_2, v_2 = r2.rv()
        (vs1, vs2), = iod.lambert(Sun.k, r_1, r_2, tof)

        dv_vector = vs1 - (vs0 + (v_1 / (24*3600) * u.day / u.s))
        dv = np.linalg.norm(dv_vector/10) * u.km / u.s

        if step_one:
            dv_final = dv
            vs22 = vs2

            step_one = False
        else:
            if dv < dv_final:
                dv_final = dv
                date_arrival_final = date_arrival
                vs22 = vs2

        date_arrival += step * u.day

    return dv_final, date_arrival_final, vs22
