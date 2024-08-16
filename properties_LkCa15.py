#-------------------------------
# Disk properies
#-------------------------------
disk_properties = {'outputdir': 'LkCa15_B3',
                  'label': r'$\mathrm{LkCa15}$',
                  'distance': 157.2,
                  'pslope': 3.0,
                  'inc': 0.,
                  'nus': np.array([340.8, 228.0, 97.5])*1.e9, #Frequency list should decrease [GHz]
                  'flux_error': np.array([0.1,0.1,0.05]),
                  'weights': np.array([1,1,1]),     #This has not been included ...             
                  'profiles': '/Users/as/Documents/Research/LkCa15/LkCa15_multiwave.txt',#[format: rad, I1, I2, ... , dI1, dI2, ...]
                  'Units': 'Jy/sr',
                  'rUnits': 'arcsec', #arcsec or au                  
                  'beam': 0., #arcsec, only used if units are Jy/beam
                  }

#-------------------------------
# Space parameter
#-------------------------------
params = {      'minRad': 0.0, #arcsec
                'maxRad': 1.0, #arcsec
                'smooth': 0.05, #arcsec
                'minAmax' : 0.03,
                'maxAmax' : 30.,
                'minTemp' : 1.0,
                'maxTemp' : 300.,
                'minSigma': 1e-6,
                'maxSigma': 1e1,
                
                'Opacities': 'default_opacities_smooth.npz',
                'saveEmceePlots': False,
                }
#--------------------    
#Opacity options:
#default_opacities_smooth.npz
#ricci_compact.npz

Lstar = 1.3 * Lsun
def lnTprior(rad, temp): #rad in AU, temp in K
    if(disk_properties['rUnits'] == 'arcsec'):
        rad *= disk_properties['distance']
    Tdust = (0.02 *  Lstar / 8./np.pi / sigmaB / (rad * AU)**2) **0.25
    return -0.5 * (Tdust-temp)**2/25.**2
