# DustProperties (In construction ... )
Inferring dust properties (Dust temperature, Dust surface density, maximum grain size) from sub-millimeter and millimeter observations.


<h3>What do you need?</h3>
<ul>
<li> Python 3</li>
<li> Install the DSHARP opacity tools (See full DSHARP opacity documentation <a href='https://github.com/birnstiel/dsharp_opac/' target="_blank"> Here</a>) </li>
<li> Additional packages: <a href='https://pypi.org/project/numpy/'>numpy</a>, <a href='https://pypi.org/project/scipy/'>scipy</a>, <a href='https://pypi.org/project/emcee/'>emcee</a>, <a href='https://pypi.org/project/corner/'>corner</a> </li>
<li> Download the opacity files <b>ricci_compact.npz</b>, <b>default_opacities_smooth.npz</b>, available at the DSHARP opacity reposity <a href='https://github.com/birnstiel/dsharp_opac/tree/master/dsharp_opac/data' target="_blank"> Here</a> </li>
<li> Clone the main.py, Utils.py, properties_LkCa15.py files in this repository and put them in the same directory as the opacity files. </li>
<li> The radial profiles in two or more bands. A single ascii file with the following columns: Radius, Intensity1, Intensity2, ...., IntensityN, Error Intensity1, Error Intensity2, ... Error Intensity N. Make sure that the intensities are arranged from the highest frequency Intensity1, to the lowest frequency Intensity N</li>
</ul>

<h3>How it works?</h3>
All you need to do is modify the properties_LkCa15.py file using your disk properties (see each parameter description below), and run it:

<pre><code>ipython main.py properties_LkCa15.py</code></pre> 

<h3>Properties file</h3>
There are serveral parameters in the properties_LkCa15.py file. This is a description of each of them>

<b>#Disk properties:</b> <br/>
'outputdir': Output directory to save your results <br/>
'label': Name of disk  <br/>
'distance': Distance to your disk in parsecs  <br/>
'pslope': Slope of the particle size distribution (recommended values: 2.5 < p < 3.5)  <br/>
'inc': Inclination of your disk. If your radial profiles are already deprojected, use 0!  <br/>
'nus': Central frequencies of your multi-wavelength data. Warning!: from highest to lowest frequency [GHz]  <br/>
'flux_error': flux calibrator error in each frequency (see e.g. ALMA Technical Handbook for reference)  <br/>
'weights': How important is each wavelength in the posterior distribution? Use a list of 1 if all of them are equally important. Use 0 to remove the effect of some walenght  <br/>
'profiles': path to your intensities profiles. You should provide a file with the following format: radius, Intensity1, Intensity2, ... , Error Intensity1, Error Intensity2, ...]  <br/>
'Units': What is your intensity units? Options available: 'Jy/sr' or 'Jy/beam'  <br/>
'rUnits': What is your radius units? Options: 'arcsec' or 'au'  <br/>
'beam': What is the beam size resolution of your radial profile? (This value is only used if your intensity units are Jy/beam)  <br/>


<b>#Space parameter:</b> <br/>
'minRad': minimum radius where you want to fit the properties  <br/>
'maxRad': maximum radius where you want to fit the properties <br/>
'smooth': radius where you want to smooth your data (recommended value:  resolution/3)  <br/>
'minAmax': minimum maximum grain size to explore [centimeters]  <br/>
'maxAmax': maximum maximum grain size to explore [centimeters]  <br/>
'minTemp' : minimum dust temperature to explore [Kelvins]  <br/>
'maxTemp': maximum dust temperature to explore [Kelvins]  <br/>
'minSigma': minimum dust surface density to explore [g/cm^2]  <br/>
'maxSigma': maximum dust surface density to explore [g/cm^2]  <br/>
'Opacities': Opacity properties model. Options: 'default_opacities_smooth.npz' or 'ricci_compact.npz'  <br/>
'saveEmceePlots': Do you want to save the results from the Emcee? True or False.  <br/>

</b>#Finally, you can include a prior to your fit using the function lnTprior:</b>  <br/>
Lstar: Luminosity of the central star.  <br/>
The Tdust radial profile is taken from the dust temperature of an passively irradiated disk, but you can modify it and use your own temperature definition.
