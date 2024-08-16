# DustProperties
Inferring dust properties (Dust temperature, Dust surface density, maximum grain size) from sub-millimeter and millimeter observations.


<h3>What do you need?</h3>
- Python 3 <br/>
- The radial profiles in two or more ALMA Bands or VLA band Q.<br/>
- Install the DSHARP opacity tools (See full DSHARP opacity documentation <a href='https://github.com/birnstiel/dsharp_opac/' target="_blank"> Here</a>)
<pre><code>pip install dsharp_opac</code></pre> 
- Additional packages: numpy, scipy, emcee, corner <br/>
- Download the opacity files ricci_compact.npz, default_opacities.npz, available <a href='https://github.com/birnstiel/dsharp_opac/tree/master/dsharp_opac/data' target="_blank"> Here</a>

<h3>How it works?</h3>
Clone 
