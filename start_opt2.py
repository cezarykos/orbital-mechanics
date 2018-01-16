import pandas as pd
import math
from astropy import units as u
from poliastro.bodies import Earth, Jupiter, Uranus, Mars
from poliastro.twobody import Orbit


import transit_opt1

transit_minEM = 50 * u.day
transit_maxEM = 100 * u.day
transit_minMJ = 400 * u.day
transit_maxMJ = 700 * u.day
transit_minJU = 600 * u.day
transit_maxJU = 2100 * u.day

def start_date_optimal(H, date0, date1, m, Isp, step):

    delta_v = 0 * u.km / u.s
    v_out = 0 * u.km / u.s
    m_prop = 0 * u.kg
    date_in = date0
    date_out = date0

    step_one0 = True
    x1 =[]
    x2 =[]
    x3 =[]
    x4 =[]
    while date0 < date1:
        epoch0 = date0.jyear
        ss0 = Orbit.circular(Earth, H, epoch=epoch0)
        vsE = ss0.rv()[1]


        dvEM, date_arrivalM, vsM = transit_opt1.transit_optimal(date0, transit_minEM, transit_maxEM, Earth, Mars, vsE, step)

        dvMJ, date_arrivalJ, vsJ = transit_opt1.transit_optimal(date_arrivalM, transit_minMJ, transit_maxMJ, Mars, Jupiter, vsM, step)

        dvJU, date_arrivalU, vsU = transit_opt1.transit_optimal(date_arrivalJ, transit_minJU, transit_maxJU, Jupiter, Uranus, vsJ, step)

        #koszty paliwa:
        m_pJU = m * (math.exp((dvJU)/ Isp) - 1)
        m_pMJ = (m + m_pJU) * (math.exp((dvMJ) / Isp) - 1)
        m_pEM = (m + m_pJU + m_pMJ) * (math.exp((dvEM) / Isp) - 1)

        dv_total = (dvEM) + (dvMJ) + (dvJU)
        m_p = m_pEM + m_pMJ + m_pJU
        
        x1.append(date0.iso[0:10])
        x2.append(int((date_arrivalU - date0).jd))
        x3.append(float(dv_total / u.km * u.s))
        x4.append(int(m_p / u.kg))
        #print(x1)
        
        #x={'1': date0.iso[0:10],'2': int((date_arrivalU - date0).jd),'3': float(dv_total / u.km * u.s),'4': int(m_p / u.kg)}
        #lista = pd.DataFrame(,index=[i])
        print(date0.iso[0:10], ', %i days, %.3f km/s, %i kg' % (int((date_arrivalU - date0).jd),float(dv_total / u.km * u.s),int(m_p / u.kg)))
 
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
    lista = {'1': x1,'2': x2, '3': x3, '4': x4}
    lista = pd.DataFrame(lista)
        
    return delta_v, v_out, date_in, date_out, m_prop, lista
