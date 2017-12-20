import math
import numpy as np
from astropy import units as u
from astropy import time
from poliastro.bodies import Earth, Sun, Venus, Jupiter, Uranus
from poliastro.twobody import Orbit
from poliastro import iod 

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

    print('data startu, TOF [days], Delta V dV [km/s], potrzebna masa paliwa [kg]')

    while date0 < date1:        
        epoch0 = date0.jyear
        ss0 = Orbit.circular(Earth, H, epoch=epoch0)        
        vsE = ss0.rv()[1]       

        
        dvEV, date_arrivalV, vsV = transit_opt.transit_optimal(date0, transit_minEV, transit_maxEV, 
                                                   Earth, Venus, vsE, step)

        dvVJ, date_arrivalJ, vsJ = transit_opt.transit_optimal(date_arrivalV, transit_minVJ, transit_maxVJ, 
                                                   Venus, Jupiter, vsV, step)

        dvJU, date_arrivalU, vsU = transit_opt.transit_optimal(date_arrivalJ, transit_minJU, transit_maxJU, 
                                                   Jupiter, Uranus, vsJ, step)

        #koszty paliwa:
        m_pJU = m * (math.exp((dvJU)/ Isp) - 1)
        m_pVJ = (m + m_pJS) * (math.exp((dvVJ) / Isp) - 1)
        m_pEV = (m + m_pJU + m_pVJ) * (math.exp((dvEV) / Isp) - 1)

        dv_total = (dvEV) + (dvVJ) + (dvJU)       
        m_p = m_pEV + m_pVJ + m_pJU     

        
        print(date0.iso[0:10], ', %i days, %.3f km/s, %i kg' % (int((date_arrivalU - date0).jd),
                                                               float(dv_total / u.km * u.s), 
                                                               int(m_p / u.kg)))

        if step_one0:       
            delta_v = dv_total
            m_prop = m_p
            v_out = vsU
            date_out = date_arrivalU

            step_one0 = False
        else:
            if dv_total < delta_v:      
                delta_v = dv_total
                m_prop = m_p
                v_out = vsU
                date_in = date0
                date_out = date_arrivalU

        date0 += step * u.day

    return delta_v, v_out, date_in, date_out, m_prop
