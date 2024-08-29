import matplotlib.pyplot as plt
import numpy as np

def Novel_Techs_Fig_1():
    x = [2023,2025,2030,2035,2040,2045,2050]
    t_flow = [0,0,5,30,80,112.4,112.4] # tidal flow
    n_flow = [0,0,0,0,0,0,0]

    plt.plot(x,t_flow,label='Tidal', marker='o',color='#006994')
    plt.plot(x,n_flow,label='Nuclear', marker='s',color='#39ff14')

    plt.title('Total Flow Capacity for Novel Techs (all profiles)')
    plt.xlabel('Investsteps')
    plt.ylabel('Total Flow Capacity /MW')
    plt.grid(True)
    plt.legend()
    plt.show()
def Bio_Fig_1():
    x = np.array([2023,2025,2030,2035,2040,2045,2050])
    bio_es_h_lc = [0.871,0.828,2.21,3.04,3.04,3.04,3.04]
    bio_es_h_mc = [0,0,0.557,0.589,0.402,0.653,2.39]
    bau_h = [0.874,0.735,2.142,3.178,3.155,3.204,5.062]

    bio_es_m_lc = [0.871,0.718,2.21,3.04,3.04,3.04,3.04]
    bio_es_m_mc = [0,0,0.909,0.628,0.435,0.685,2.39]
    bau_m = [0.874,0.735,2.142,3.178,3.155,3.204,5.062]

    bio_es_l_lc = [0.871,0.718,2.21,3.04,3.04,3.04,3.04]
    bio_es_l_mc = [0,0,1.13,1,1.24,1.63,4.72]
    bau_l = [0.874,0.735,2.2,3.3,3.808,4.19,7.46]

    bar_width = 1.5

    fig, (ax1, ax2, ax3) = plt.subplots(3,1, figsize=(8,10))

    ax1.bar(x,bio_es_h_lc,label='low cost',color='#5AA24D',edgecolor='grey',width=bar_width)
    ax1.bar(x,bio_es_h_mc,bottom=bio_es_h_lc,label='medium cost',color='#519447',edgecolor='grey',width=bar_width)
    ax1.plot(x,bau_h,marker='o',color='#63B24F',label='BAU Total Bioenergy')
    ax1.set_title('Bioenergy Annual Outflow (High Offshore Wind Deployment Profile)')
    #ax1.set_xlabel('Investsteps')
    ax1.set_ylabel('Annual Outflow /TWh')
    ax1.grid(True)
    ax1.set_axisbelow(True)

    ax2.bar(x,bio_es_m_lc,label='low cost',color='#5AA24D',edgecolor='grey',width=bar_width)
    ax2.bar(x,bio_es_m_mc,bottom=bio_es_m_lc,label='medium cost',color='#519447',edgecolor='grey',width=bar_width)
    ax2.plot(x,bau_m,marker='o',color='#63B24F',label='BAU Total Bioenergy')
    ax2.set_title('Bioenergy Annual Outflow (Medium Offshore Wind Deployment Profile)')
    #ax2.set_xlabel('Investsteps')
    ax2.set_ylabel('Annual Outflow /TWh')
    ax2.grid(True)
    ax2.set_axisbelow(True)

    ax3.bar(x,bio_es_l_lc,label='low cost',color='#5AA24D',edgecolor='grey',width=bar_width)
    ax3.bar(x,bio_es_l_mc,bottom=bio_es_l_lc,label='medium cost',color='#519447',edgecolor='grey',width=bar_width)
    ax3.plot(x,bau_l,marker='o',color='#63B24F',label='BAU Total Bioenergy')
    ax3.set_title('Bioenergy Annual Outflow (Low Offshore Wind Deployment Profile)')
    ax3.set_xlabel('Investsteps')
    ax3.set_ylabel('Annual Outflow /TWh')
    ax3.grid(True)
    ax3.set_axisbelow(True)
    #ax1.grid(True)

    plt.tight_layout()
    plt.legend()
    plt.show()
def Planned_Development_Fig_1():
    x = [2025,2030,2035]
    onwind = np.array([55,871,0])
    offwind = np.array([0,3350,3780])
    pv = np.array([0,1552,0])
    imports = np.array([500,2200,0])

    li_storage = np.array([0,4230,1440])
    phs_storage = np.array([0,3581,0])

    bar_width = 1.5

    fig, (ax1, ax2) = plt.subplots(1,2, figsize=(8,10))

    ax1.bar(x,onwind,label='Onshore Wind',color='#A3E8A9',edgecolor='grey',width=bar_width)
    ax1.bar(x,offwind,label='Offshore Wind',bottom=onwind,color='#47D154',edgecolor='grey',width=bar_width)
    ax1.bar(x,pv,label='Solar PV',color='#DDCC77',bottom=offwind+onwind,edgecolor='grey',width=bar_width)
    ax1.bar(x,imports,label='Import/Exports',bottom=pv+offwind+onwind,color='#E68A31',edgecolor='grey',width=bar_width)
    ax1.set_ylabel('Planned Capacity /MW')
    ax1.grid(True)
    ax1.set_axisbelow(True)
    ax1.set_title('Planned Capacity Deployment')

    ax2.bar(x,li_storage,label='Lithium Ion Storage',color='#882255',edgecolor='grey',width=bar_width)
    ax2.bar(x,phs_storage,bottom=li_storage,label='Pumped Storage',color='#332288',edgecolor='grey',width=bar_width)
    ax2.set_ylabel('Planned Storage Deployment /MWh')
    ax2.grid(True)
    ax2.set_axisbelow(True)
    ax2.set_title('Planned Storage Deployment')

    plt.tight_layout()
    ax1.legend()
    ax2.legend()
    plt.show()
def FF_Decomission():
    x = [2023,2025,2030,2035,2040]
    o_flow = [324,324,0,0,0] # tidal flow
    c_flow = [750,0,0,0,0]
    g_flow = [3812,3344,2022,464,0]
    all_flow = [4886,3668,2022,464,0]

    plt.plot(x,o_flow,label='Oil',color='#000000')
    plt.plot(x,c_flow,label='Coal',color='#5A5A5A')
    plt.plot(x,g_flow,label='Gas',color='#A5A5A5')
    plt.plot(x,all_flow,label='All FF',color='#6A0241')

    plt.title('Assumed Phase Out of Fossil Fuel Capacity')
    plt.xlabel('Investsteps')
    plt.ylabel('Total Flow Capacity /MW')
    plt.grid(True)
    plt.legend()
    plt.show()

Planned_Development_Fig_1()