"""
Parameter file
"""
import numpy as np
#import eddy_functions as eddy


lon1 = 140 #was 90
lon2 = 180
lat1 = -55
lat2 = 0


cut_lon = 20. # cutoff wavelenth in longitudinal direction (for filtering) [degrees]
cut_lat = 10. # cutoff wavelenth in latitudinal direction (for filtering) [degrees]

ssh_crit_max = 1.
dssh_crit = 0.01
ssh_crits = np.arange(-ssh_crit_max, ssh_crit_max+dssh_crit, dssh_crit)
ssh_crits = np.flipud(ssh_crits)

amp_thresh = 0.01 # minimum eddy amplitude [m]
d_thresh = 400. # max linear dimension of eddy [km] ; Only valid outside Tropics (see Chelton et al. (2011), pp. 207)

dt_aviso = 7. # Sample rate used in Chelton et al. (2011) [days]
dE_aviso = 150. # Length of search ellipse to East of eddy used in Chelton et al. (2011) [km]

#This is only used in eddy_tracking so, has been called explictly there. This removes the circular dependency so we can import params into eddy_functions!
#rossrad = eddy.load_rossrad() # Atlas of Rossby radius of deformation and first baroclinic wave speed (Chelton et al. 1998)

eddy_scale_min = 0.25 # min ratio of amplitude of new and old eddies
eddy_scale_max = 2.5 # max ratio of amplidude of new and old eddies

dt_save = 100 # Step increments at which to save data while tracking eddies
