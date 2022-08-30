# -*- coding: utf-8 -*-
"""
Originally created on Thu Jul 21 15:21:25 2022 by ajm226
Updated on Tue Aug 30 16:03:29 2022 by tma127
"""

import numpy as np
import streamlit as st


@st.cache
def Budyko_Sellers_model_temperature_initialisation(Temp,S0,relaxation_coefficient,CO2_concentration):
    # In this version of the model we use the last temperature configuration

    # CONSTANTS
    I0 = 204.0 # constant used in OLR parameterisation
    b = 2.17  # constant used in OLR parameterisation
    Temp0=263.0 # Temperature below which enviroment is fully ice or snow covered
    Temp1=273.0 # Temperature above which environment has no snow or ice ocver
    albedo0=0.62 # albedo of ice cover
    albedo1=0.25 # albedo of earth when not ice covered.
    beta1=relaxation_coefficient

    # setting latitude and time resolution - do not change this section!
    dimj =181
    tf =48
    dt=3600.0
    Gamma=0.003
    C = 10000000.0 #{Heat capacity of total atmospheric column per sq. metre: C=cp*ps/g}
    #If the model is used only to compute a steady state, the value of C is not important
    deltamin = 0.001  #Convergence criteria: max. global average difference [in K] between temperatures at consecutive timesteps

    # determines solar insolation at a particular latitude
    # and also setup latitude grid

    dx=2/(dimj-1)
    x=np.ones(dimj)
    phi=np.ones(dimj)
    s=np.ones(dimj)
    for j in range(0,dimj):
        x[j]=1.0-(j*dx)  #x runs from 1 (NPole) to -1 (SPole)
        phi[j]=np.arctan2(x[j],np.sqrt(1-(pow(x[j],2.0))))  #radians}
        phi[j]=phi[j]*180/np.pi
        P2=0.5*((3*(x[j]**2.0))-1)
        s[j]=1-(0.477*P2)

    tmax=24*300

    #{TIME LOOP}

    A=np.ones(dimj)
    albedo=np.ones(dimj)
    Tempplus=np.ones(dimj)
    Tempmin=np.ones(dimj)
    tplanet=np.ones(tmax)
    for t in range(0,tmax):
        #{The planetary mean temperature is a weighted average, weighted according to the area the zonal rings}
        #{mean temperature of the planet}
        Tp=0
        for j in range(1,dimj):
            Tp=Tp+0.5*0.5*(Temp[j-1]+Temp[j])*(x[j-1]-x[j])

        tplanet[t]=Tp

        #    {albedo at beginning of time step}
        #    basically assumes below some temperature fully snow or ice covered
        #     and therefore large albedo, partially ice or snow covered and thus
        #     a moderate albedo or no ice cover and thus low albedo based on
        #     temperature at particular latitude

        for j in range(0,dimj):
            if (Temp[j]<=Temp0):
                albedo[j]=albedo0
            if ((Temp[j]>Temp0) & (Temp[j]<=Temp1)):
                albedo[j]=albedo0+(Temp[j]-Temp0)*(albedo1-albedo0)/(Temp1-Temp0)
            if (Temp[j]>Temp1):
                albedo[j]=albedo1

        #    % this is the meridional heat transport due to circulation of
        #    % atmosphere or the ocean

        for j in range(0,dimj):
            A[j]=beta1*(Temp[j]-Tp)

        # the next 3 for loops solve the balance equation iteratively and
        #  eventually produce a steay-state solution
        #predictor step
        for j in range(0,dimj):
            # Tempplus[j]=Temp[j]+(dt/C)*((-A[j]-b*(Temp[j]-273.16))-I0+(5.397*np.log(CO2/280.0))+(0.25*S0*s[j]*(1-albedo[j])));
            Tempplus[j]=Temp[j]+(dt/C)*((-A[j]-b*(Temp[j]-273.16))-I0+(0.25*S0*s[j]*(1-albedo[j])+(5.397*np.log(CO2_concentration/280.0))))

        #mean temperature of the planet
        Tp=0
        for j in range(1,dimj):
            Tp=Tp+0.5*0.5*(Tempplus[j-1]+Tempplus[j])*(x[j-1]-x[j])

        for j in range(1,dimj-1):
            A[j]=beta1*(Tempplus[j]-Tp)

        #{corrector step}
        for j in range(0,dimj):
            Tempmin[j]=Temp[j]  #Tempmin is value of Temp at previous time
            # Temp[j]=Temp[j]+(dt/C)*((-A[j]-b*(Tempplus[j]-273.16))-I0+(5.397*np.log(CO2/280.0))+(0.25*S0*s[j]*(1-albedo[j])));
            Temp[j]=Temp[j]+(dt/C)*((-A[j]-b*(Tempplus[j]-273.16))-I0+(0.25*S0*s[j]*(1-albedo[j])+(5.397*np.log(CO2_concentration/280.0))))

        delta=0
        deltamax=0
        for j in range(0,dimj):
            delta=abs(Temp[j]-Tempmin[j])
            if (delta>deltamax):
                deltamax=delta

        #convergence to steady state?}
        if (deltamax<deltamin):
            break

    return phi,Temp,albedo,tplanet[t]


@st.cache
def Budyko_Sellers_model(phiedgeIC,S0,relaxation_coefficient,CO2_concentration):
    # CONSTANTS

    I0 = 204.0 # constant used in OLR parameterisation
    b = 2.17  # constant used in OLR parameterisation
    Temp0=263.0 # Temperature below which enviroment is fully ice or snow covered
    Temp1=273.0 # Temperature above which environment has no snow or ice ocver
    albedo0=0.62 # albedo of ice cover
    albedo1=0.25 # albedo of earth when not ice covered.
    beta1=relaxation_coefficient

    # setting latitude and time resolution - do not change this section!
    dimj =181
    tf =48
    dt=3600.0
    Gamma=0.003
    C = 10000000.0 #{Heat capacity of total atmospheric column per sq. metre: C=cp*ps/g}
    #If the model is used only to compute a steady state, the value of C is not important
    deltamin = 0.001  #Convergence criteria: max. global average difference [in K] between temperatures at consecutive timesteps

    # determines solar insolation at a particular latitude
    # and also setup latitude grid

    dx=2/(dimj-1)
    x=np.ones(dimj)
    phi=np.ones(dimj)
    s=np.ones(dimj)
    for j in range(0,dimj):
        x[j]=1.0-(j*dx)  #x runs from 1 (NPole) to -1 (SPole)
        phi[j]=np.arctan2(x[j],np.sqrt(1-(pow(x[j],2.0))))  #radians}
        phi[j]=phi[j]*180/np.pi
        P2=0.5*((3*(x[j]**2.0))-1)
        s[j]=1-(0.477*P2)


    Temp=np.ones(dimj)
    #INITIALIZATION OF TEMPERATURE which is dependent on position of polar ice edge in this configuration
    for j in range(0,dimj):
        if (np.abs(phi[j])>phiedgeIC):
            Temp[j]=243.0
        elif (np.abs(phi[j])<=phiedgeIC):
            Temp[j]=310.8

    tmax=24*300

    A=np.ones(dimj)
    albedo=np.ones(dimj)
    Tempplus=np.ones(dimj)
    Tempmin=np.ones(dimj)
    tplanet=np.ones(tmax)
    for t in range(0,tmax):
        #{The planetary mean temperature is a weighted average, weighted according to the area the zonal rings}
        #{mean temperature of the planet}
        Tp=0
        for j in range(1,dimj):
            Tp=Tp+0.5*0.5*(Temp[j-1]+Temp[j])*(x[j-1]-x[j])

        tplanet[t]=Tp

        #    {albedo at beginning of time step}
        #    basically assumes below some temperature fully snow or ice covered
        #     and therefore large albedo, partially ice or snow covered and thus
        #     a moderate albedo or no ice cover and thus low albedo based on
        #     temperature at particular latitude

        for j in range(0,dimj):
            if (Temp[j]<=Temp0):
                albedo[j]=albedo0
            if ((Temp[j]>Temp0) & (Temp[j]<=Temp1)):
                albedo[j]=albedo0+(Temp[j]-Temp0)*(albedo1-albedo0)/(Temp1-Temp0)
            if (Temp[j]>Temp1):
                albedo[j]=albedo1

        #    % this is the meridional heat transport due to circulation of
        #    % atmosphere or the ocean

        for j in range(0,dimj):
            A[j]=beta1*(Temp[j]-Tp)

        # the next 3 for loops solve the balance equation iteratively and
        #  eventually produce a steay-state solution using a prredictor-corrector algorithm
        #predictor step
        for j in range(0,dimj):
            # Tempplus[j]=Temp[j]+(dt/C)*((-A[j]-b*(Temp[j]-273.16))-I0+(5.397*np.log(CO2/280.0))+(0.25*S0*s[j]*(1-albedo[j])));
            Tempplus[j]=Temp[j]+(dt/C)*((-A[j]-b*(Temp[j]-273.16))-I0+(0.25*S0*s[j]*(1-albedo[j])+(5.397*np.log(CO2_concentration/280.0))))

        #mean temperature of the planet
        Tp=0
        for j in range(1,dimj):
            Tp=Tp+0.5*0.5*(Tempplus[j-1]+Tempplus[j])*(x[j-1]-x[j])

        for j in range(1,dimj-1):
            A[j]=beta1*(Tempplus[j]-Tp)

        #{corrector step}
        for j in range(0,dimj):
            Tempmin[j]=Temp[j]  #Tempmin is value of Temp at previous time
            # Temp[j]=Temp[j]+(dt/C)*((-A[j]-b*(Tempplus[j]-273.16))-I0+(5.397*np.log(CO2/280.0))+(0.25*S0*s[j]*(1-albedo[j])));
            Temp[j]=Temp[j]+(dt/C)*((-A[j]-b*(Tempplus[j]-273.16))-I0+(0.25*S0*s[j]*(1-albedo[j])+(5.397*np.log(CO2_concentration/280.0))))

        delta=0
        deltamax=0
        for j in range(0,dimj):
            delta=abs(Temp[j]-Tempmin[j])
            if (delta>deltamax):
                deltamax=delta

        #convergence to steady state?}
        if (deltamax<deltamin):
            break

    return phi,Temp,albedo,tplanet[t]

