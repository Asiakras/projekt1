from math import sin, cos, sqrt, atan, atan2, degrees, radians
import sys
import numpy*

o = object()

class Transformacje:
    def __init__(self, model: str = "wgs84"):
        """
        Parametry elipsoid:
            a - duża półoś elipsoidy - promień równikowy
            b - mała półoś elipsoidy - promień południkowy
            flat - spłaszczenie
            ecc2 - mimośród^2
        + WGS84: https://en.wikipedia.org/wiki/World_Geodetic_System#WGS84
        + Inne powierzchnie odniesienia: https://en.wikibooks.org/wiki/PROJ.4#Spheroid
        + Parametry planet: https://nssdc.gsfc.nasa.gov/planetary/factsheet/index.html
        """
        if model == "wgs84":
            self.a = 6378137.0 # semimajor_axis
            self.b = 6356752.31424518 # semiminor_axis
        elif model == "grs80":
            self.a = 6378137.0
            self.b = 6356752.31414036
        elif model == "mars":
            self.a = 3396900.0
            self.b = 3376097.80585952
        else:
            raise NotImplementedError(f"{model} model not implemented")
        self.flat = (self.a - self.b) / self.a
        self.ecc = sqrt(2 * self.flat - self.flat ** 2) # eccentricity  WGS84:0.0818191910428 
        self.ecc2 = (2 * self.flat - self.flat ** 2) # eccentricity**2


    
    def xyz2plh(self, X, Y, Z, output = 'dec_degree'):
        """
        Algorytm Hirvonena - algorytm transformacji współrzędnych ortokartezjańskich (x, y, z)
        na współrzędne geodezyjne długość szerokość i wysokośc elipsoidalna (phi, lam, h). Jest to proces iteracyjny. 
        W wyniku 3-4-krotneej iteracji wyznaczenia wsp. phi można przeliczyć współrzędne z dokładnoscią ok 1 cm.     
        Parameters
        ----------
        X, Y, Z : FLOAT
             współrzędne w układzie orto-kartezjańskim, 

        Returns
        -------
        lat
            [stopnie dziesiętne] - szerokość geodezyjna
        lon
            [stopnie dziesiętne] - długośc geodezyjna.
        h : TYPE
            [metry] - wysokość elipsoidalna
        output [STR] - optional, defoulf 
            dec_degree - decimal degree
            dms - degree, minutes, sec
        """
        r   = sqrt(X**2 + Y**2)           # promień
        lat_prev = atan(Z / (r * (1 - self.ecc2)))    # pierwsze przybliilizenie
        lat = 0
        while abs(lat_prev - lat) > 0.000001/206265:    
            lat_prev = lat
            N = self.a / sqrt(1 - self.ecc2 * sin(lat_prev)**2)
            h = r / cos(lat_prev) - N
            lat = atan((Z/r) * (((1 - self.ecc2 * N/(N + h))**(-1))))
        lon = atan(Y/X)
        N = self.a / sqrt(1 - self.ecc2 * (sin(lat))**2);
        h = r / cos(lat) - N       
        if output == "dec_degree":
            return degrees(lat), degrees(lon), h 
        elif output == "dms":
            lat = self.deg2dms(degrees(lat))
            lon = self.deg2dms(degrees(lon))
            return f"{lat[0]:02d}:{lat[1]:02d}:{lat[2]:.2f}", f"{lon[0]:02d}:{lon[1]:02d}:{lon[2]:.2f}", f"{h:.3f}"
        else:
            raise NotImplementedError(f"{output} - output format not defined")
            

#####definicje transformacji z pliku GW - trzeba będzie je zmienić pod selfy by wpisywały się w model

    def XYZ2neu(X,Y,Z):
        '''
        Funkcja zwracająca macierz ij w ukladzie neu wykorzystując macierz w ukladzie XYZ.
    
        Parameters
        ----------
        X, Y, Z : FLOAT
             współrzędne w układzie orto-kartezjańskim,
   
    
        Returns
        -------
        dx : numpy.ndarray
            Macierz ij w ukladzie neu
    
        '''
        f, l, h = geo.xyz2plh(X, Y, Z)
        phi = f*pi/180
        lam = l*pi/180
        dX = np.array([X,Y,Z])
        R = np.array([[-sin(phi)*cos(lam), -sin(phi)*sin(lam), cos(phi)],
                      [-sin(lam), cos(lam), 0],
                      [cos(phi)*cos(lam), cos(phi)*sin(lam), sin(phi)]])
        dx = R @ dX
        return dx

    def pl21992(self, lat, lon):
        '''
        Funkcja zwracająca współrzędne w układzie 1992
    
        Parameters
        ----------
        lat
            [stopnie dziesiętne] - szerokość geodezyjna
        lon
            [stopnie dziesiętne] - długośc geodezyjna.
   
    
        Returns
        -------
        X92, Y92 współrzędne w układzie 1992
    
        '''
        phi = lat*pi/180
        lam = lon*pi/180
        A0 = 1 - self.ecc2/4 - (3 * (self.ecc2**2))/64 - (5 * (self.ecc2**3))/256
        A2 = 3/8 *(self.ecc2 + (self.ecc2**2)/4 + 15 * (self.ecc2**3)/ 128)
        A4 = 15/256 * (self.ecc2**2 + 3 * (self.ecc2**3)/4)
        A6 = 35 * (self.ecc2**3)/ 3072
        sigma = self.a * (A0 * phi - A2 * sin(2*phi) + A4 * sin(4*phi) - A6 * sin(6*phi))
        l0 = 19*pi/180
        b2 = self.a**2 * (1 - self.ecc2)
        e2prim = (self.a**2 - b2)/b2
        dl = lam - l0
        t = tan(phi)
        n2 = e2prim * (cos(phi))**2
        N = self.a/sqrt(1 - (self.ecc2 * sin(phi)**2))
        xgk = sigma + (dl**2/2) * N * sin(phi) * cos(phi) * (1 + ((dl**2/12) * cos(phi)**2 * (5 - t**2 + 9*n2 + 4*(n2**2))) + ((dl**4/360) * cos(phi)**4 * (61 - 58 * t**2 + t**4 + 270 * n2 - 330 * n2 * t**2)))
        ygk = dl * N * cos(phi) * (1 + (dl**2/6) * cos(phi)**2 * (1 - t**2 + n2) + (dl**4/120) * cos(phi)**4 * (5 - 18 * t**2 + t**4 + 14*n2 - 58 * n2 * t**2))
        m92 = 0.9993
        X92 = xgk * m92 - 5300000
        Y92 = ygk * m92 + 500000
        return X92, Y92
    
if __name__ == "__main__":
    # utworzenie obiektu
    geo = Transformacje(model = "wgs84")
    # dane XYZ geocentryczne
    X = 3664940.500; Y = 1409153.590; Z = 5009571.170
    phi, lam, h = geo.xyz2plh(X, Y, Z)
    print(phi, lam, h)
    # phi, lam, h = geo.xyz2plh2(X, Y, Z)
    # print(phi, lam, h)
        
 #na lekcji   
    def xyz2neu(self, x,y,z,x0,y0,z0):
        phi, lam, _ = [radians(coord) for coord in self.xyz2plh(x0,y0,z0)]
        
        R = np.array([[-sin(lam), -sin(phi)*cos(lam), cos(phi)*cos(lam)],
                      [cos(lam), -sin(phi)*sin(lam), cos(phi)*sin(lam)],
                      [0, cos(phi), sin(phi)]])
        xyz_t = np.array([[x -x0],
                         [ y -y0],
                         [ z -z0]])
        [[E],[N],[U]] = R.T @ xyz_t
        
        return N, E, U
    
    x,y,z = 1, 1, 5009571.170
    x0, y0,z0 = 1, 1, 5009571.170   
    enu = geo.xyz2neu(x,y,z,x0,y0,z0)
    print('enu=', enu)
    
    elif '--xyz2neu' in sys.argv:
        coords_neu = []
        with open(inp_file_path) as f:
            lines - f.readlines()
            lines = lines[4:]
            for line in lines:
                line = line.strip()
                x,y,z = line.split(',')
                x,y,z = (float(x), float(y), float(z))
                x0,y0,z0 = [float(coord) for coord in sys.argv[-4:-1]
                n,e,u = geo.xyz2neu(x,y,z,x0,y0,z0)
                coords_neu.append([n,e,u])
                
                
        with open('result_xyz2neu.txt', 'w') as f:
            f.write('x[m], y[m], z[m]\n')
            for coords in coords_xyz:
                line = ','.join([f'{coord:11.3f}' for coord in coords])
                f.write(line + '\n')
                
#z poprzedniej lekcji
        with open('result_xyz2plh.txt', 'w') as f:
            for coords in coords_plh:
                line = ','.join([str(coord) for coord in coords])
                f.write(line + '\n')
                
        coords_plh = []
        with open(wsp_inp.txt) as f:
            lines = f.readlines()
            lines = lines[4:]
            for line in lines:
                line = line.strip()
                x_str ,y_str ,z_str = line.split(',')
                x,y,z = (float(x_str), float(y_str), float(z_str))
                p,l,h =geo.xyz2plh(x,y,z)
               
                
        if '--header_lines' in sys.argv:
            header_lines = int(sys.argv)
            
        elif '--xyz2plh' in sys.argv:
            coords_plh = []
            with open('wsp_inp.txt','r') as f:
                lines = f.readlines()
                lines = lines[4:]
                for line in lines:
                    line = line.strip()
                    x_str, y_str, z_str = line.split(',')
                    x,y,z = (float(x_str), float(y_str), float(z_str))
                    phi, lam,h  = geo.xyz2plh(x,y,z)
                    coords_plh.append([phi, lam ,h])
                    
                    
            with open('result_xyz2plh.txt', 'w') as f:
                f.write('phi[stopnie], lam[stopnie], h[m]\n')
                for coords in coords_plh:
                    line = ','.join([f'{coord:11.3f}' for coord in coords])
                    f.write(line + '\n')
                    
        elif '--xyz2plh' in sys.argv:
            coords_plh = []
            with open('wsp_inp.txt','r') as f:
                lines = f.readlines()
                lines = lines[4:]
                for line in lines:
                    line = line.strip()
                    x_str, y_str, z_str = line.split(',')
                    x,y,z = (float(x_str), float(y_str), float(z_str))
                    phi, lam,h  = geo.xyz2plh(x,y,z)
                    coords_plh.append([phi, lam ,h])
                    
                    
            with open('result_xyz2plh.txt', 'w') as f:
                f.write('phi[stopnie], lam[stopnie], h[m]\n')
                for coords in coords_plh:
                    line = ','.join([f'{coord:11.3f}' for coord in coords])
                    f.write(line + '\n')
        
        elif '--xyz2neu' in sys.argv:
            coords_neu = []
            with open(inp_file_path,'r') as f:
                lines = f.readlines()
                lines = lines[4:]
                for line in lines:
                    line = line.strip()
                    x,y,z = line.split(',')
                    x,y,z = (float(x), float(y), float(z))
                    x0,y0,z0 = [float(coord) for coord in sys.argv[-4:-1]
                    n,e,u = geo.xyz2neu(x,y,z,x0,y0,z0)
                    coords_neu.append([n,e,u])
                    
                    
            with open('result_xyz2neu.txt', 'w') as f:
                f.write('n, e, u\n')
                for coords in coords_neu:
                    line = ','.join([f'{coord:11.3f}' for coord in coords])
                    f.write(line + '\n')
                
                
        elif '--pl21992' in sys.argv:
            coords_pl1992 = []
            with open(inp_file_path,'r') as f:
                lines - f.readlines()
                lines = lines[4:]
                for line in lines:
                    line = line.strip()
                    phi_str, lam_str ,h_str = line.split(',')
                    phi,lam,h = (float(phi_str), float(lam_str), float(h_str))
                    f92, l92 = geo.pl2pl1992(phi, lam)
                    coords_pl1992.append([f92, l92])
                    
                    
            with open('result_pl21992z.txt', 'w') as f:
                f.write('phi92, lam92\n')
                for coords in coords_pl1992:
                    line = ','.join([f'{coord:11.3f}' for coord in coords])
                    f.write(line + '\n')
                