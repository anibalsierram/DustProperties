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

#Disk properties:
'outputdir': Output directory to save your results
'label': Name of disk 
'distance': Distance to your disk in parsecs
'pslope': Slope of the particle size distribution (recommended values: 2.5 < p < 3.5)
'inc': Inclination of your disk. If your radial profiles are already deprojected, use 0!
'nus': Central frequencies of your multi-wavelength data. Warning!: from highest to lowest frequency [GHz]
'flux_error': flux calibrator error in each frequency (see e.g. ALMA Technical Handbook for reference),
'weights': How important is each wavelength in the posterior distribution? Use a list of 1 if all of them are equally important. Use 0 to remove the effect of some walenght.
'profiles': path to your intensities profiles. You should provide a file with the following format: radius, Intensity1, Intensity2, ... , Error Intensity1, Error Intensity2, ...]
'Units': What is your intensity units? Options available: 'Jy/sr' or 'Jy/beam'
'rUnits': What is your radius units? Options: 'arcsec' or 'au'
'beam': What is the beam size resolution of your radial profile? (This value is only used if your intensity units are Jy/beam)


#Space parameter:
'minRad': minimum radius where you want to fit the properties
'maxRad': maximum radius where you want to fit the properties
'smooth': radius where you want to smooth your data (recommended value:  resolution/3)
'minAmax': minimum maximum grain size to explore [centimeters]
'maxAmax': maximum maximum grain size to explore [centimeters]
'minTemp' : minimum dust temperature to explore [Kelvins]
'maxTemp': maximum dust temperature to explore [Kelvins]
'minSigma': minimum dust surface density to explore [g/cm^2]
'maxSigma': maximum dust surface density to explore [g/cm^2]
'Opacities': Opacity properties model. Options: 'default_opacities_smooth.npz' or 'ricci_compact.npz'
'saveEmceePlots': Do you want to save the results from the Emcee? True or False.

#Finally, you can include a prior to your fit using the function lnTprior, which is defined below:
Lstar: Luminosity of the central star.
The Tdust radial profile is taken from the dust temperature of an passively irradiated disk, but you can modify it and use your own temperature definition.
