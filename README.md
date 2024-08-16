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
