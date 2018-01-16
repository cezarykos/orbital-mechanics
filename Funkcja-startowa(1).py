import matplotlib
import matplotlib.pyplot as plt
from astropy import units as u
from astropy import time
import warnings
from matplotlib.dates import DateFormatter
import datetime
import start_opt1
import start_opt2
import check_func


def fxn():
    warnings.warn("deprecated", DeprecationWarning)

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    fxn()
    #ZALOZENIA 
    date_0 = '2030-01-01 12:00'        # ISO 
    date_1 = '2045-01-01 12:00'
    date_0 = time.Time(date_0,  scale='utc')       #ISO
    date_1 = time.Time(date_1, scale='utc')
    date_0 = time.Time(date_0.jd, format='jd', scale='utc')     #Data Julianska
    date_1 = time.Time(date_1.jd, format='jd', scale='utc')
    m_ship = 1500 * u.kg
    I_sp = 4400 /1000 * u.km / u.s
    H = 300 * u.km
    
    # OBLICZENIA
    step = 10 # deklaracja kroku czasowego (co ile dni)
    
    # Asysta grawitacyjna Wenus i Jowisza 
    delta_v_V, v_out_V, date_in_V, date_out_V, m_prop_V, lista_V = start_opt1.start_date_optimal(H, date_0, date_1, m_ship, I_sp, step)
    print (delta_v_V, v_out_V, date_in_V.iso, date_out_V.iso, m_prop_V)
    check_func.check_uran_orbit(date_out_V, v_out_V, m_ship, I_sp)
    
    fig1, ax1 = plt.subplots()
    fig2, ax2 = plt.subplots()
    daty_lista = lista_V.get('1')
    dv_lista = lista_V.get('3')
    mp_lista = lista_V.get('4')
    #Wykres 1
    ax1.grid(True)
    ax1.plot([datetime.datetime.strptime(val, '%Y-%m-%d') for val in daty_lista], dv_lista, color='blue')
    
    fig1.autofmt_xdate()
    myFmt = DateFormatter("%Y-%m-%d")
    ax1.xaxis.set_major_formatter(myFmt)
    
    ax1.set_title('Wykres potrzebnej zmiany prędkosc od daty startu')
    ax1.set_xlabel('Data startu misji')
    ax1.set_ylabel('Całkowita zmiana prędkosci [km/s]')
    fig1.savefig("obraz1.png")
    #Wykres 2
    ax2.grid(True)
    ax2.plot([datetime.datetime.strptime(val, '%Y-%m-%d') for val in daty_lista], mp_lista, color='green')
    
    fig2.autofmt_xdate()
    ax2.xaxis.set_major_formatter(myFmt)
    
    ax2.set_title('Ilosc paliwa potrzebna do realizacji misji')
    ax2.set_xlabel('Data startu misji')
    ax2.set_ylabel('Masa paliwa [kg]')
    fig2.savefig("obraz2.png")
    
    
    # Asysta grawitacyjna Marsa i Jowisza
    delta_v_M, v_out_M, date_in_M, date_out_M, m_prop_M, lista_M  = start_opt2.start_date_optimal(H, date_0, date_1, m_ship, I_sp, step)
    print (delta_v_M, v_out_M, date_in_M.iso, date_out_M.iso, m_prop_M)
    check_func.check_uran_orbit(date_out_M, v_out_M, m_ship, I_sp)
    
    fig3, ax3 = plt.subplots()
    fig4, ax4 = plt.subplots()
    
    daty_lista2 = lista_M.get('1')
    dv_lista2 = lista_M.get('3')
    mp_lista2 = lista_M.get('4')
    # Wykres 3
    ax3.grid(True)
    ax3.plot([datetime.datetime.strptime(val, '%Y-%m-%d') for val in daty_lista2], dv_lista2, color='blue')
    
    fig3.autofmt_xdate()
    myFmt = DateFormatter("%Y-%m-%d")
    ax3.xaxis.set_major_formatter(myFmt)
    
    ax3.set_title('Wykres potrzebnej zmiany prędkosc od daty startu')
    ax3.set_xlabel('Data startu mijsi')
    ax3.set_ylabel('Całkowita zmiana prędkosc [km/s]')
    fig3.savefig("obraz3.png")
    # wykres 4
    ax4.grid(True)
    ax4.plot([datetime.datetime.strptime(val, '%Y-%m-%d') for val in daty_lista2], mp_lista2, color='green')
    
    fig4.autofmt_xdate()
    myFmt = DateFormatter("%Y-%m-%d")
    ax4.xaxis.set_major_formatter(myFmt)
    
    ax4.set_title('Ilosc paliwa potrzebna do realizacji misji')
    ax4.set_xlabel('Data startu misji')
    ax4.set_ylabel('Masa paliwa [kg]')
    fig4.savefig("obraz4.png")
    