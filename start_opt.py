import math
import numpy as np
from astropy import units as u
from astropy import time
from poliastro.bodies import Earth, Sun, Venus, Jupiter, Uranus
from poliastro.twobody import Orbit
from poliastro import iod
from poliastro import ephem  

import transit_opt

transit_minEV = 50 * u.day
transit_maxEV = 100 * u.day
transit_minVJ = 400 * u.day
transit_maxVJ = 700 * u.day
transit_minJU = 600 * u.day
transit_maxJU = 2100 * u.day

def start_date_optimal(H, date0, date1, m, Isp, step):
    
    delta_v = 0 * u.km / u.s
    v_out = 0 * u.km / u.s
    m_prop = 0 * u.kg
    date_in = date0
    date_out = date0

    step_one0 = True        

    print('Launch date, TOF [days], Delta V dV [km/s], Required propellant mass [kg]')

    while date0 < date1:        
        epoch0 = date0.jyear_str
        ss0 = Orbit.circular(Earth, H, epoch=epoch0)        
        vsE = ss0.rv()[1]       

        
        dvEV, date_arrivalV, vsV = transit_opt.transit_optimal(date0, transit_minEV, transit_maxEV, 
                                                   ephem.get_body_ephem(Earth, epoch0), ephem.get_body_ephem(Venus, epoch), vsE, step)

        dvVJ, date_arrivalJ, vsJ = transit_opt.transit_optimal(date_arrivalV, transit_minVJ, transit_maxVJ, 
                                                   ephem.get_body_ephem(Venus, epoch), ephem.get_body_ephem(Jupiter, epoch), vsV, step)

        dvJS, date_arrivalS, vsS = transit_opt.transit_optimal(date_arrivalJ, transit_minJU, transit_maxJU, 
                                                   ephem.get_body_ephem(Jupiter, epoch), ephem.get_body_ephem(Uranus, epoch), vsJ, step)

        #koszty paliwa:
        m_pJS = m * (math.exp((dvJS)/ Isp) - 1)
        m_pVJ = (m + m_pJS) * (math.exp((dvVJ) / Isp) - 1)
        m_pEV = (m + m_pJS + m_pVJ) * (math.exp((dvEV) / Isp) - 1)

        dv_total = (dvEV) + (dvVJ) + (dvJS)       
        m_p = m_pEV + m_pVJ + m_pJS     

        
        print(date0.iso[0:10], ', %i days, %.3f km/s, %i kg' % (int((date_arrivalS - date0).jd),
                                                               float(dv_total / u.km * u.s), 
                                                               int(m_p / u.kg)))

        if step_one0:       
            delta_v = dv_total
            m_prop = m_p
            v_out = vsS
            date_out = date_arrivalS

            step_one0 = False
        else:
            if dv_total < delta_v:      
                delta_v = dv_total
                m_prop = m_p
                v_out = vsS
                date_in = date0
                date_out = date_arrivalS

        date0 += step

    return delta_v, v_out, date_in, date_out, m_prop