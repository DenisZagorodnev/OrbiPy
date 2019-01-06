#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Содержимое: константы, объект integrator, правая часть уравнения, координаты точек либрации


import lagrange_pts_p as lpts
import numpy as np
#import orbi_data.csv

class model_tool:
    def __init__(self, system, integrator, crtbp, STM):
        
        data = self.prepare_file('orbi_data.csv')
        const = self.get_orbi(data, system)
        self.mu1 = const[0]
        self.ER = const[1]
        
        self.integrator = integrator
        
        if crtbp == None:
           self.equation = self.ode1
           if STM!= None:
               self.equation = self.ode1_STM
        else:
            self.equation = crtbp
        
        
        self.lagrange_points = lpts.lagrange_pts(self.equation, self.mu1)
        
 
    
    @staticmethod
    def ode1(t, s, mu):
        x, y, z, x1, y1, z1 = s
        mu2 = 1 - mu

        yz2 = y * y + z * z;
        r13 = ((x + mu2) * (x + mu2) + yz2) ** 1.5;
        r23 = ((x - mu ) * (x - mu ) + yz2) ** 1.5;

        yzcmn = (mu / r13 + mu2 / r23);

        dx1dt = 2 * y1 + x - (mu * (x + mu2) / r13 + mu2 * (x - mu) / r23);
        dy1dt = -2 * x1 + y - yzcmn * y;
        dz1dt = - yzcmn * z;
    
        ds = np.array([x1, y1, z1, dx1dt, dy1dt, dz1dt])
        return(ds)
        
    @staticmethod
    def ode1_STM(t, s, mu):
        x, y, z, x1, y1, z1 = s[:6]

        STM = np.ascontiguousarray(s[6:]).reshape(6, 6)
    
        #mu - примерно равно единице
        mu2 = 1 - mu
    
        yz2 = y * y + z * z;
        r1 = ((x + mu2) * (x + mu2) + yz2) ** 1.5
        r2 = ((x - mu ) * (x - mu ) + yz2) ** 1.5

        yzcmn = (mu / r1 + mu2 / r2);
    
        dx1dt =  2 * y1 + x - (mu * (x + mu2) / r1 + mu2 * (x - mu) / r2)
        dy1dt = -2 * x1 + y - yzcmn * y
        dz1dt =             - yzcmn * z
    
        #ds = np.array([x1, y1, z1, dx1dt, dy1dt, dz1dt])
        ds = np.empty_like(s)

        Uxx = 3.0*mu*(mu2 + x)**2*(y**2 + z**2 + (mu2 + x)**2)**(-2.5) - 1.0*mu*(y**2 + z**2 + (mu2 + x)**2)**(-1.5) + 3.0*mu2*(mu - x)**2*(y**2 + z**2 + (mu - x)**2)**(-2.5) - 1.0*mu2*(y**2 + z**2 + (mu - x)**2)**(-1.5) + 1.0
        Uxy = 3.0*y*(mu*(mu2 + x)*(y**2 + z**2 + (mu2 + x)**2)**(-2.5) - mu2*(mu - x)*(y**2 + z**2 + (mu - x)**2)**(-2.5))

        Uxz = 3.0*z*(mu*(mu2 + x)*(y**2 + z**2 + (mu2 + x)**2)**(-2.5) - mu2*(mu - x)*(y**2 + z**2 + (mu - x)**2)**(-2.5))
        Uyy = 3.0*mu*y**2*(y**2 + z**2 + (mu2 + x)**2)**(-2.5) - 1.0*mu*(y**2 + z**2 + (mu2 + x)**2)**(-1.5) + 3.0*mu2*y**2*(y**2 + z**2 + (mu - x)**2)**(-2.5) - 1.0*mu2*(y**2 + z**2 + (mu - x)**2)**(-1.5) + 1.0
        Uyz = 3.0*y*z*(mu*(y**2 + z**2 + (mu2 + x)**2)**(-2.5) + mu2*(y**2 + z**2 + (mu - x)**2)**(-2.5))
        Uzz = 3.0*mu*z**2*(y**2 + z**2 + (mu2 + x)**2)**(-2.5) - 1.0*mu*(y**2 + z**2 + (mu2 + x)**2)**(-1.5) + 3.0*mu2*z**2*(y**2 + z**2 + (mu - x)**2)**(-2.5) - 1.0*mu2*(y**2 + z**2 + (mu - x)**2)**(-1.5)
    
        A=np.array(((0,0,0,1,0,0),(0,0,0,0,1,0),(0,0,0,0,0,1),(Uxx,Uxy,Uxz,0,2,0),(Uxy,Uyy,Uyz,-2,0,0),(Uxz,Uyz,Uzz,0,0,0)))

        STM = np.dot(A, STM)
        ds[0], ds[1], ds[2], ds[3], ds[4], ds[5] = x1, y1, z1, dx1dt, dy1dt, dz1dt
        ds[6:] = STM.ravel()
        return (ds)





 
    @staticmethod
    def prepare_file(filename):
     import csv
     a = {}
     with open(filename, 'r') as csvfile:
        next(csvfile)
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            a[row[0]] = [float(row[1].replace(',', '.')), float(row[2].replace(',', '.'))]
     return(a)   
    @staticmethod
    def get_orbi(data, system):
        return(data.get(system))
        
        
        
