# DustProperties
Inferring dust properties radial profiles (Dust temperature, Dust surface density, maximum grain size) from sub-millimeter and millimeter dust continuum observations.
Questions are welcome at: a.sierra@ucl.ac.uk

<h2>What do you need?</h2>
<ul>
<li> Python 3</li>
<li> Install the DSHARP opacity tools (See full DSHARP opacity documentation <a href='https://github.com/birnstiel/dsharp_opac/' target="_blank"> Here</a>) </li>
<li> Additional packages: <a href='https://pypi.org/project/numpy/'>numpy</a>, <a href='https://pypi.org/project/scipy/'>scipy</a>, <a href='https://pypi.org/project/emcee/'>emcee</a>, <a href='https://pypi.org/project/corner/'>corner</a> </li>
<li> Download the opacity files <b>ricci_compact.npz</b>, <b>default_opacities_smooth.npz</b>, available at the DSHARP opacity reposity <a href='https://github.com/birnstiel/dsharp_opac/tree/master/dsharp_opac/data' target="_blank"> Here</a> </li>
<li> Clone the main.py (main code), Utils.py (Useful functions), and properties_LkCa15.py (parameters file) in this repository and put them in the same directory as the opacity files. </li>
<li> The radial profiles in two or more bands. A single ascii file with the following columns: Radius, Intensity1, Intensity2, ...., IntensityN, Error Intensity1, Error Intensity2, ... Error Intensity N. Make sure that the intensities are arranged from the highest frequency Intensity1, to the lowest frequency Intensity N. For example, you can use the intensity radial profiles for LkCa15 in <a href="https://academic.oup.com/mnras/article/538/4/2358/8063580" target="_blank">Sierra et al. 2025</a>, directly from the LkCa15_multiwave.txt file</li>
  
</ul>

<h2>How it works?</h2>
All you need to do is modify the properties_LkCa15.py file using your disk properties (see each parameter description below), and run it:

<pre><code>ipython main.py properties_LkCa15.py</code></pre> 


<h2>What does the code do?</h2>

<ul>
  <li>The code uses your radial intensity profiles from ALMA or VLA and the formal solution to the radiative transfer equation in <a href='https://ui.adsabs.harvard.edu/abs/2020ApJ...892..136S/abstract' target='_blank'>Sierra & Lizano 2020</a> to fit the spectral energy distribution (SED) of your disk at each radius. The dust temperature, dust surface densiy, and maximum grain size radial profile are infered from the SED fit. </li>
  <li>The SED is initially independently fitted at each radius. This is called ''SED first round''. </li>
  <li>The SED is fitted again at each radius, using the median value of the best-fit values in the surrounding radius as a prior (within +/- rsmooth/2). This is called ''SED second round''.</li>
  <li>This procedure corrects for unrealistic best-fit values at individual radii, as shown in the Figure below. (The corrected final fit is that shown in the second row).</li>
</ul>

<img src='Example.png'>



<h2>Properties file</h2>
There are serveral parameters in the properties_LkCa15.py file. This is a description of each of them.<br/>
<br/>

<b>#Disk properties:</b> <br/>
<ul>
<li>'outputdir': Output directory to save your results </li>
<li>'label': Name of disk  </li>
<li>'distance': Distance to your disk in parsecs  </li>
<li>'pslope': Slope of the particle size distribution (recommended values: 2.5 < p < 3.5)  </li>
<li>'inc': Inclination of your disk. If your radial profiles are already deprojected, use 0!  </li>
<li>'nus': Central frequencies of your multi-wavelength data. Warning!: from highest to lowest frequency [GHz]  </li>
<li>'flux_error': flux calibrator error in each frequency (see e.g. ALMA Technical Handbook for reference)  </li>
<li>'weights': How important is each wavelength in the posterior distribution? Use a list of 1 if all of them are equally important. Use 0 to remove the effect of some walenght  </li>
<li>'profiles': path to your intensities profiles. You should provide a file with the following format: radius, Intensity1, Intensity2, ... , Error Intensity1, Error Intensity2, ...]  </li>
<li>'Units': What is your intensity units? Options available: 'Jy/sr' or 'Jy/beam'  </li>
<li>'rUnits': What is your radius units? Options: 'arcsec' or 'au'  </li>
<li>'beam': What is the beam size resolution of your radial profile? (This value is only used if your intensity units are Jy/beam)  </li>
</ul>

<b>#Space parameter:</b> <br/>
<ul>
<li>'minRad': minimum radius where you want to fit the properties  </li>
<li>'maxRad': maximum radius where you want to fit the properties </li>
<li>'smooth': radius where you want to smooth your data (recommended value:  resolution/3)  </li>
<li>'minAmax': minimum maximum grain size to explore [centimeters]  </li>
<li>'maxAmax': maximum maximum grain size to explore [centimeters]  </li>
<li>'minTemp' : minimum dust temperature to explore [Kelvins]  </li>
<li>'maxTemp': maximum dust temperature to explore [Kelvins]  </li>
<li>'minSigma': minimum dust surface density to explore [g/cm^2]  </li>
<li>'maxSigma': maximum dust surface density to explore [g/cm^2]  </li>
<li>'Opacities': Opacity properties model. Options: 'default_opacities_smooth.npz' or 'ricci_compact.npz'  </li>
<li>'saveEmceePlots': Do you want to save the results from the Emcee? True or False.  </li>
</ul>


<b>#Finally, you can include a prior to your fit using the function lnTprior:</b>  <br/>

Lstar: Luminosity of the central star.  <br/>
The Tdust radial profile is taken from the dust temperature of an passively irradiated disk, but you can modify it and use your own temperature definition.


<h2>Citation</h2>
If you use this code, you can cite the formal solution to the radiative transfer equation with scattering described in <a href='https://ui.adsabs.harvard.edu/abs/2020ApJ...892..136S/abstract' target='_blank'>Sierra & Lizano 2020</a>, and/or and example where this code has been implemented <a href='https://ui.adsabs.harvard.edu/abs/2024arXiv240815407S/abstract' target='_blank'>Sierra et al. 2024b</a>.

<br> <br>
Sierra & Lizano 2020
<pre><code>
@ARTICLE{2020ApJ...892..136S,
       author = {{Sierra}, Anibal and {Lizano}, Susana},
        title = "{Effects of Scattering, Temperature Gradients, and Settling on the Derived Dust Properties of Observed Protoplanetary Disks}",
      journal = {\apj},
     keywords = {Circumstellar dust, Interstellar scattering, Radiative transfer, Radio continuum emission, Protoplanetary disks, 236, 854, 1335, 1340, 1300, Astrophysics - Earth and Planetary Astrophysics, Astrophysics - Solar and Stellar Astrophysics},
         year = 2020,
        month = apr,
       volume = {892},
       number = {2},
          eid = {136},
        pages = {136},
          doi = {10.3847/1538-4357/ab7d32},
archivePrefix = {arXiv},
       eprint = {2003.02982},
 primaryClass = {astro-ph.EP},
       adsurl = {https://ui.adsabs.harvard.edu/abs/2020ApJ...892..136S},
      adsnote = {Provided by the SAO/NASA Astrophysics Data System}
}
</code></pre>

  
Sierra et al. 2024b
<pre><code>
  @ARTICLE{2024arXiv240815407S,
       author = {{Sierra}, Anibal and {P{\'e}rez}, Laura M. and {Sotomayor}, Benjam{\'\i}n and {Benisty}, Myriam and {Chandler}, Claire J. and {Andrews}, Sean and {Carpenter}, John and {Henning}, Thomas and {Testi}, Leonardo and {Ricci}, Luca and {Wilner}, David},
        title = "{Constraints on the physical origin of large cavities in transition disks from multi-wavelength dust continuum emission}",
      journal = {arXiv e-prints},
     keywords = {Astrophysics - Earth and Planetary Astrophysics, Astrophysics - Solar and Stellar Astrophysics},
         year = 2024,
        month = aug,
          eid = {arXiv:2408.15407},
        pages = {arXiv:2408.15407},
          doi = {10.48550/arXiv.2408.15407},
archivePrefix = {arXiv},
       eprint = {2408.15407},
 primaryClass = {astro-ph.EP},
       adsurl = {https://ui.adsabs.harvard.edu/abs/2024arXiv240815407S},
      adsnote = {Provided by the SAO/NASA Astrophysics Data System}
}

</code></pre>
