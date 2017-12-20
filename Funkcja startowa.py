import math
import numpy as np
from astropy import units as u
from astropy import time
from poliastro.bodies import Earth, Sun
from poliastro.twobody import Orbit
from poliastro import iod
from poliastro import ephem  
import warnings 

def fxn():
    warnings.warn("deprecated", DeprecationWarning)

def input_func():
    # Input parameters:
    print (' ')
    print ('Dane statku oraz misji')
    
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    fxn()
    
'''
    check = True
    while check:
        m_ship = int(eval(input('Masa statku [kg]: ')))

        if 0 < m_ship < 100000:
            check = False
        else:
            print ('Masa poza skalą (0-100000)kg.')

    check = True
    while check:
        I_sp = int(eval(input('Impuls własciwy silnika [m/s]: ')))

        if 0 < I_sp < 100000:
            check = False
        else:
            print ('Impuls poza skala (0 - 100 000)m/s.')

    print (' ')
    print ('Orbita wstępna (kolowa):')

    check = True
    while check:
        H = int(eval(input('Wysokosc orbtity [km]: ')))

        if 100 < H < 1000000:
            check = False
        else:
            print ('Poza skalą (1000 - 1 000 000)km.')

    print (' ')
    print ('Data rozpoczęcia misji:')

    check = True
    while check:
        date_0y = int(eval(input('Rok [rrrr]: ')))

        if 2017 < date_0y < 2200:
            check = False
        else:
            print ('Poza skala (2017 - 2200).')

    check = True
    while check:
        date_0m = int(eval(input('Miesiac [mm]: ')))

        if 0 < date_0m < 13:
            check = False
        else:
            print ('Miesiac nieprawidlowy (1 -12).')

    print (' ')
    print ('Planowana data zakończenia misji:')

    check = True
    while check:
        date_1y = int(eval(input('Rok [rrrr]: ')))

        if 1800 < date_1y < 2200:
            if date_1y > date_0y:
                check = False
            else:
                print ('Data nieprawidlowa, koniec przed startem?')
        else:
            print ('Poza skala (2018 - 2200).')

    check = True
    while check:
        date_1m = int(eval(input('Miesiac[mm]: ')))

        if 0 < date_1m < 13:
            check = False
        else:
            print ('Miesiac nieprawidlowy (1 -12)')

    date_0 = str(date_0y) + '-' + str(date_0m) + '-01 12:00'        # date in ISO
    date_1 = str(date_1y) + '-' + str(date_1m) + '-01 12:00'

    date_0 = time.Time(date_0, format='iso', scale='utc')       # Time class in ISO
    date_1 = time.Time(date_1, format='iso', scale='utc')
    

    m_ship = m_ship * u.kg
    I_sp = I_sp /1000 * u.km / u.s
    H = H * u.km

    return m_ship, I_sp, H, date_0, date_1
   '''
    date_0 = '2030-01-01 12:00'        # date in ISO
    date_1 = '2045-01-01 12:00'
    date_0 = time.Time(date_0, format='iso', scale='utc')       # Time class in ISO
    date_1 = time.Time(date_1, format='iso', scale='utc')
    date_0 = time.Time(date_0.jd, format='jd', scale='utc')    
    date_1 = time.Time(date_1.jd, format='jd', scale='utc')
    m_ship = 1000 * u.kg
    I_sp = 4600 /1000 * u.km / u.s
    H = 300 * u.km



    import start_opt
    step = 10
    delta_v, v_out, date_in, date_out, m_prop = start_opt.start_date_optimal(H, date_0, date_1, m_ship, I_sp, step)

    print (delta_v, v_out, date_in, date_out, m_prop)
    import check_func
    check_func.check_uran_orbit(date_out, v_out, m_ship, I_sp)

