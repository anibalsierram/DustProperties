# DustProperties
Inferring dust properties (Dust temperature, Dust surface density, maximum grain size) from sub-millimeter and millimeter observations.


<h3>What do you need?</h3>
- Python 3 <br/>
- The radial profiles in two or more ALMA Bands or VLA band Q.<br/>
- Install the DSHARP opacity tools (See full DSHARP opacity documentation <a href='https://github.com/birnstiel/dsharp_opac/' target="_blank"> Here</a>)
- Additional packages: numpy, scipy, emcee, corner <br/>
- Download the opacity files ricci_compact.npz, default_opacities.npz, available at the DSHARP opacity reposity <a href='https://github.com/birnstiel/dsharp_opac/tree/master/dsharp_opac/data' target="_blank"> Here</a>.
- Clone the main.py, Utils.py, properties_LkCa15.py files in this repository and put them in the same directory as the opacity files. <br/>
- Anything else :)


<h3>How it works?</h3>
- All you need to do is modify the properties_LkCa15.py file using your disk properties (see each parameter description below), and run it:

<pre><code>ipython main.py properties_LkCa15.py</code></pre> 

<h3>Properties file</h3>
There are serveral parameters in the properties_LkCa15.py file. This is a description of each of them>

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
