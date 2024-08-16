#-----------------------------------------------------------------
# Libraries
#-----------------------------------------------------------------
import time
start_time = time.time()
import os
import sys
import emcee
import corner
import numpy as np
import dsharp_opac as opacity
from scipy import interpolate
import matplotlib.pyplot as plt


exec(open('Utils.py').read())

#-----------------------------------------------------------------
#Constants
#-----------------------------------------------------------------

clight = 3.e10    #cm/s
kB = 1.38e-16     #erg/K
Ggrav = 6.672e-8  #cm**3/g/s**2
hP = 6.626e-27    #erg s
mH = 1.67e-24     #g
sigmaB = 5.67e-5  #erg/cm**2/K**4/s

AU = 1.496e13     #cm
pc = 3.086e18     #cm
Jy = 1.e-23       #erg/cm**2

Msun = 1.9891e33  #g
Rsun = 6.96e10    #cm
Lsun = 3.826e33   #erg/s
Tsun = 5780.      #K

Mearth = 5.972e27 #g
Mmoon  = 7.347e25 #g

arcsec2rad = np.pi / 180. / 3600.


#-----------------------------------------------------------------
#    Disk dictionary
#-----------------------------------------------------------------
if len(sys.argv) < 2:
    print(r'****************************************************************')
    print(r'Include a dictionary file: python main.py <dictionary_file_path>')
    print(r'****************************************************************')    
    sys.exit()
exec(open(sys.argv[1]).read())


#-----------------------------------------------------------------
#    Emcee Setup
#-----------------------------------------------------------------
print (r'MCMC properties')
labels = ['logTd','log10 sigma','log10 amax'] 
max_par  = np.log10([ params['maxTemp'],  params['maxSigma'],  params['maxAmax']]) #In Log10
min_par  = np.log10([ params['minTemp'],  params['minSigma'],  params['minAmax']]) #In Log10
nsteps   = 5000, 1000
nwalkers = 24 #8 times the number of free parameters
ndim     = len(labels)
last     = 1000 #discards the nsteps to compute the errors in the first emcee round


#-----------------------------------------------------------------    
#    Reading data
#-----------------------------------------------------------------
data = np.loadtxt(disk_properties['profiles'], comments='#', unpack=False,skiprows=0).T

disk_properties['wls'] = clight/disk_properties['nus']
disk_properties['mu'] = np.cos(disk_properties['inc'] *np.pi/180.)
disk_properties['radius'] = data[0]

#-----------------------------------------------------------------
#    Intensities and errors
#-----------------------------------------------------------------
if disk_properties['Units'] == 'Jy/sr':
    disk_properties['Int'] = data[1:len(disk_properties['nus'])+1]
    disk_properties['dInt'] = np.sqrt( (data[len(disk_properties['nus'])+1:2*len(disk_properties['nus'])+1])**2 +
                                       ((disk_properties['Int'].T*disk_properties['flux_error'])**2).T )

elif disk_properties['Units'] == 'Jy/beam':
    beam = disk_properties['beam']**2*np.pi/4./np.log(2.) *arcsec2rad**2
    disk_properties['Int'] = data[1:len(disk_properties['nus'])+1]/beam
    disk_properties['dInt'] = np.sqrt( (data[len(disk_properties['nus'])+1:2*len(disk_properties['nus'])+1]/beam)**2 +
                                       ((disk_properties['Int'].T*disk_properties['flux_error'])**2).T )
else:
    print(r'Units should be Jy/sr or Jy/beam')
    sys.exit()

if params['saveEmceePlots']:
    os.system('mkdir '+disk_properties['outputdir']+'/EmceePlots')

    
#-----------------------------------------------------------------
#    Plot data
#-----------------------------------------------------------------
fig, ax = plt.subplots(ncols=1, nrows=1)
for ik in range(len(disk_properties['nus'])):
    ax.errorbar(disk_properties['radius'], disk_properties['Int'][ik], disk_properties['dInt'][ik])
ax.set_yscale('log')
ax.set_xlabel(r'$\mathrm{Radius \ ['+disk_properties['rUnits']+']}$')
ax.set_ylabel(r'$\mathrm{Brigthness \ [Jy/sr]}$')
ax.set_xlim(params['minRad'], params['maxRad'])
index = np.where( (disk_properties['radius'] > params['minRad']) & (disk_properties['radius']< params['maxRad']))
ax.set_ylim(0.9*np.min(disk_properties['Int'][-1][index]), 1.1*np.max(disk_properties['Int'][0][index]))
plt.savefig(disk_properties['outputdir']+'/Data.pdf', bbox_inches='tight')
plt.close()

#-----------------------------------------------------------------
#    Best-fit vectors
#-----------------------------------------------------------------
disk_properties['best_model'] = np.ones((len(disk_properties['radius']),len(disk_properties['nus']))) * np.nan
disk_properties['amax'] = np.ones((len(disk_properties['radius']))) * np.nan
disk_properties['sigm'] = np.ones((len(disk_properties['radius']))) * np.nan
disk_properties['temp'] = np.ones((len(disk_properties['radius']))) * np.nan

disk_properties['Eamax'] = np.ones((len(disk_properties['radius']),2)) * np.nan
disk_properties['Esigm'] = np.ones((len(disk_properties['radius']),2)) * np.nan
disk_properties['Etemp'] = np.ones((len(disk_properties['radius']),2)) * np.nan

disk_properties['best_model_smooth'] = np.ones((len(disk_properties['radius']),len(disk_properties['nus']))) * np.nan
disk_properties['amax_smooth'] = np.ones((len(disk_properties['radius']))) * np.nan
disk_properties['sigm_smooth'] = np.ones((len(disk_properties['radius']))) * np.nan
disk_properties['temp_smooth'] = np.ones((len(disk_properties['radius']))) * np.nan

disk_properties['Eamax_smooth'] = np.ones((len(disk_properties['radius']),2)) * np.nan
disk_properties['Esigm_smooth'] = np.ones((len(disk_properties['radius']),2)) * np.nan
disk_properties['Etemp_smooth'] = np.ones((len(disk_properties['radius']),2)) * np.nan

disk_properties['tau_k']  = np.ones(( len(disk_properties['radius']), len(disk_properties['nus']))) * np.nan
disk_properties['Etau_k'] = np.ones(( len(disk_properties['radius']), len(disk_properties['nus']), 2)) * np.nan
disk_properties['tau_s']  = np.ones(( len(disk_properties['radius']), len(disk_properties['nus']))) * np.nan
disk_properties['Etau_s'] = np.ones(( len(disk_properties['radius']), len(disk_properties['nus']), 2)) * np.nan



#-----------------------------------------------------------------
#    Read opacities
#-----------------------------------------------------------------
#Opacities (kappa(amax), sigma(amax))
opa_abs, opa_sca  = Opas(disk_properties['pslope'], disk_properties['wls'])


#-----------------------------------------------------------------
#    Fit the SED at each radius for the 1st time
#-----------------------------------------------------------------
print(r' SED first round' )
for ir in range(len(disk_properties['radius'])):
    if( (disk_properties['radius'][ir] > params['minRad']) and  (disk_properties['radius'][ir] < params['maxRad']) ):
        
        #---------------------
        # Initializate walkers
        p0 = [ np.zeros(ndim) for i in range(nwalkers)]
        for i in range(nwalkers):
            for k in range(ndim):
                p0[i][k] = np.random.uniform(min_par[k], max_par[k])

        #---------------------
        #Fit
        sampler = emcee.EnsembleSampler(nwalkers, ndim, lnpostfn,
                                            args=[min_par, max_par, disk_properties['Int'].T[ir],
                                                      disk_properties['dInt'].T[ir], disk_properties['weights'],
                                                      disk_properties['mu'],  disk_properties['nus'],
                                                      np.zeros(3),
                                                      np.ones(3)*np.inf,
                                                      disk_properties['radius'][ir]*disk_properties['distance']])
        pos, prob, state = sampler.run_mcmc(p0, nsteps[0], progress=False)

        #---------------------        
        #percentiles
        samples = sampler.chain[:,-last:,:].reshape((-1,ndim))
        best_parms = 10**np.array([np.percentile(samples[-last:,i], 50) for i in range(ndim)])
        p68_params = 10**np.array([np.percentile(samples[-last:,i], 68) for i in range(ndim)])
        p32_params = 10**np.array([np.percentile(samples[-last:,i], 32) for i in range(ndim)])

        disk_properties['best_model'][ir] = FScattering(disk_properties['nus'],
                                                            best_parms[0], best_parms[1], best_parms[2],
                                                            disk_properties['mu'])
        
        disk_properties['temp'][ir] = best_parms[0]
        disk_properties['sigm'][ir] = best_parms[1]
        disk_properties['amax'][ir] = best_parms[2]

        disk_properties['Etemp'][ir] = p32_params[0], p68_params[0]
        disk_properties['Esigm'][ir] = p32_params[1], p68_params[1]
        disk_properties['Eamax'][ir] = p32_params[2], p68_params[2]        

#-----------------------------------------------------------------
#    Fit the SED at each radius for the 2nd time
#-----------------------------------------------------------------
print(r' SED second round' )
for ir in range(len(disk_properties['radius'])):
    if( (disk_properties['radius'][ir] > params['minRad']) and  (disk_properties['radius'][ir] < params['maxRad']) ):

        #---------------------
        # Define a narrow min and max params
        # Based on the neighboorhood
        index = np.where( ( disk_properties['radius'] < disk_properties['radius'][ir] + params['smooth']) &
                          ( disk_properties['radius'] > disk_properties['radius'][ir] - params['smooth']) )
        #index = ir-5:ir+6
        narrow_max_par  = np.array([np.nanmedian( disk_properties['Etemp'].T[1][index]),
                                    np.nanmedian( disk_properties['Esigm'].T[1][index]),
                                    np.nanmedian( disk_properties['Eamax'].T[1][index]) ])
        
        narrow_min_par  = np.array([np.nanmedian( disk_properties['Etemp'].T[0][index]),
                                    np.nanmedian( disk_properties['Esigm'].T[0][index]),
                                    np.nanmedian( disk_properties['Eamax'].T[0][index]) ])

        guess = np.array([np.nanmedian( disk_properties['temp'][index]),
                            np.nanmedian( disk_properties['sigm'][index]),
                            np.nanmedian( disk_properties['amax'][index]) ])

        Eguess = np.fmax( abs(guess - narrow_min_par), abs(guess-narrow_max_par))
        
        #---------------------        
        # Initializate walkers
        p0 = [ np.zeros(ndim) for i in range(nwalkers)]
        for i in range(nwalkers):
            for k in range(ndim):
                p0[i][k] = np.random.uniform(min_par[k], max_par[k])

        #---------------------                
        #Fit
        sampler = emcee.EnsembleSampler(nwalkers, ndim, lnpostfn,
                                            args=[min_par, max_par, disk_properties['Int'].T[ir],
                                                      disk_properties['dInt'].T[ir], disk_properties['weights'],
                                                      disk_properties['mu'],  disk_properties['nus'],
                                                      guess, Eguess,
                                                      disk_properties['radius'][ir]*disk_properties['distance']])
        pos, prob, state = sampler.run_mcmc(p0, nsteps[1], progress=False)

        #---------------------        
        #percentiles
        samples = sampler.chain[:,:,:].reshape((-1,ndim))
        best_parms = 10**np.array([np.percentile(samples[-last:,i], 50) for i in range(ndim)])
        p68_params = 10**np.array([np.percentile(samples[-last:,i], 68) for i in range(ndim)])
        p32_params = 10**np.array([np.percentile(samples[-last:,i], 32) for i in range(ndim)])

        disk_properties['best_model_smooth'][ir] = FScattering(disk_properties['nus'],
                                                                   best_parms[0], best_parms[1], best_parms[2],
                                                                   disk_properties['mu'])
        
        disk_properties['temp_smooth'][ir] = best_parms[0]
        disk_properties['sigm_smooth'][ir] = best_parms[1]
        disk_properties['amax_smooth'][ir] = best_parms[2]

        disk_properties['Etemp_smooth'][ir] = p32_params[0], p68_params[0]
        disk_properties['Esigm_smooth'][ir] = p32_params[1], p68_params[1]
        disk_properties['Eamax_smooth'][ir] = p32_params[2], p68_params[2]        

        #---------------------
        # Optical depths
        #tau = sigma * kappa(amax)
        disk_properties['tau_k'][ir] = np.percentile( 10**samples[-last:,1] * opa_abs(10**samples[-last:,2]), 50, axis=1)
        disk_properties['Etau_k'][ir,:,0] = np.percentile( 10**samples[-last:,1] * opa_abs(10**samples[-last:,2]), 32, axis=1)
        disk_properties['Etau_k'][ir,:,1] = np.percentile( 10**samples[-last:,1] * opa_abs(10**samples[-last:,2]), 68, axis=1)

        disk_properties['tau_s'][ir] = np.percentile( 10**samples[-last:,1] * opa_sca(10**samples[-last:,2]), 50, axis=1)
        disk_properties['Etau_s'][ir,:,0] = np.percentile( 10**samples[-last:,1] * opa_sca(10**samples[-last:,2]), 32, axis=1)
        disk_properties['Etau_s'][ir,:,1] = np.percentile( 10**samples[-last:,1] * opa_sca(10**samples[-last:,2]), 68, axis=1)

        
        #========================================
        # Plots
        #========================================
        if params['saveEmceePlots']:
            
            #========================================
            # Corner Plots
            fig = corner.corner(samples, labels=labels,
                                    show_titles=True, quantiles=[0.16, 0.50, 0.84],
                                    label_kwargs={'labelpad':20, 'fontsize': 0}, fontsize=8)
            fig.savefig(disk_properties['outputdir']+'/EmceePlots/r'+str(ir)+'_Corner.pdf', bbox_inches='tight')
            plt.close()

            #========================================
            # Plot the walkers
            fig, ax = plt.subplots(ndim,1)
            for j in range(ndim):
                for k in range(nwalkers):
                    ax[j].plot(sampler.chain[k,:,j])
                ax[j].set_xlabel('nsteps')
                ax[j].set_ylabel(labels[j])
            ax[0].set_title(r'$\mathrm{Radius = %.i \ mas}$'%(disk_properties['radius'][ir]*1.e3))                
            plt.savefig(disk_properties['outputdir']+'/EmceePlots/r'+str(ir)+'_Walker.pdf', bbox_inches='tight')
            plt.close()
            
            #========================================
            # Plots
            fig, ax = plt.subplots(1,1)
            ax.errorbar(disk_properties['nus'], disk_properties['Int'].T[ir], disk_properties['dInt'].T[ir],
                            marker='.', color='b', label=r'Data')
            ax.plot(disk_properties['nus'], disk_properties['best_model'][ir],
                        color='r', label=r'Model')
            ax.plot(disk_properties['nus'], disk_properties['best_model_smooth'][ir],
                        color='g', label=r'Model \ smooth')            
            ax.set_xscale('log')
            ax.set_yscale('log')
            ax.set_xlabel(r'$\nu \ [GHz]$')
            ax.set_ylabel(r'$Intensity \ [Jy/sr]$')
            ax.set_title(r'$\mathrm{Radius = %i \ mas}$'%(disk_properties['radius'][ir]*1.e3))
            ax.legend(loc='best')
            plt.savefig(disk_properties['outputdir']+'/EmceePlots/r'+str(ir)+'_SED.pdf', bbox_inches='tight')
            plt.close()



#-----------------------------------------------------------------
# Total mass
#-----------------------------------------------------------------
disk_properties['Mdust'] = 2. * np.pi * np.nansum( disk_properties['sigm_smooth'] * disk_properties['radius']  ) * (disk_properties['radius'][3] - disk_properties['radius'][2]) * AU**2 / Msun
if (disk_properties['rUnits'] ==  'arcsec'):
    disk_properties['Mdust'] *= disk_properties['distance'] **2
print('Dust mass: ', disk_properties['Mdust']/1e-3, 'E-3 Msun')


            
#-----------------------------------------------------------------
# Plot results Properties
#-----------------------------------------------------------------
param = ['temp', 'sigm', 'amax']
label_prop = [r'$\mathrm{Temperature \ [K]}$', r'$\mathrm{\Sigma_{d} \ [g \ cm^{-2}]}$', r'$\mathrm{a_{max} \ [cm]}$']
scale = ['linear', 'log', 'log']


fig, ax = plt.subplots(nrows=2, ncols=3, figsize=(15,4))

for ik in range(3):
    ax[0,ik].errorbar(disk_properties['radius'], disk_properties[param[ik]],
                        yerr=[2*(disk_properties[param[ik]]-disk_properties['E'+param[ik]].T[0]),
                              2*(disk_properties['E'+param[ik]].T[1]-disk_properties[param[ik]])], alpha=0.5)

    ax[1,ik].errorbar(disk_properties['radius'], disk_properties[param[ik]+'_smooth'],
                        yerr=[2*(disk_properties[param[ik]+'_smooth']-disk_properties['E'+param[ik]+'_smooth'].T[0]),
                              2*(disk_properties['E'+param[ik]+'_smooth'].T[1]-disk_properties[param[ik]+'_smooth'])], alpha=0.5)

    
    ax[0,ik].plot(disk_properties['radius'], disk_properties[param[ik]], 'k-', zorder=10)
    ax[1,ik].plot(disk_properties['radius'], disk_properties[param[ik]+'_smooth'], 'k-', zorder=10)
    #ax[1,ik].plot(disk_properties['radius'], disk_properties[param[ik]], 'r-', zorder=9, alpha=0.5)    
    
    ax[1,ik].set_xlabel(r'$\mathrm{Radius \ ['+disk_properties['rUnits']+']}$')
    for il in range(2):
        ax[il,ik].set_yscale(scale[ik])
        ax[il,ik].set_ylabel(label_prop[ik])

plt.savefig(disk_properties['outputdir']+'/DustProperties_'+params['Opacities'][:-4]+'.pdf', bbox_inches='tight')
plt.close()


#-----------------------------------------------------------------
# Plot results Optical Depths
#-----------------------------------------------------------------
fig, ax = plt.subplots(nrows=1, ncols=len(disk_properties['nus']), figsize=(2.5*len(disk_properties['nus']),2))

for ik in range(len(disk_properties['nus'])):
    ax[ik].set_title(r'$ %i \ \mathrm{GHz}$'%(disk_properties['nus'][ik]/1.e9))
    ax[ik].plot(disk_properties['radius'], disk_properties['tau_k'][:,ik], color='k')
    ax[ik].errorbar(disk_properties['radius'], disk_properties['tau_k'][:,ik],
                        yerr = [(disk_properties['tau_k'][:,ik]-disk_properties['Etau_k'][:,ik,0]),
                                (disk_properties['Etau_k'][:,ik,1]-disk_properties['tau_k'][:,ik])], alpha=0.5)

    ax[ik].plot(disk_properties['radius'], disk_properties['tau_s'][:,ik], color='k')
    ax[ik].errorbar(disk_properties['radius'], disk_properties['tau_s'][:,ik],
                        yerr = [(disk_properties['tau_s'][:,ik]-disk_properties['Etau_s'][:,ik,0]),
                                (disk_properties['Etau_s'][:,ik,1]-disk_properties['tau_s'][:,ik])], alpha=0.5)
    
    ax[ik].set_yscale('log')

ax[0].set_ylabel(r'$\tau$')
ax[0].set_xlabel(r'$\mathrm{Radius \ ['+disk_properties['rUnits']+']}$')
plt.savefig(disk_properties['outputdir']+'/DustProperties_OptDepths'+params['Opacities'][:-4]+'.pdf', bbox_inches='tight')
plt.close()




#-----------------------------------------------------------------
# Saving results

#Save Results
output=[disk_properties, params]
outfile= disk_properties['outputdir']+'/Results_'+params['Opacities'][:-4]+'.csv'
print ('Saving input parameters and results to file -> ', outfile)
np.save(open(outfile,'wb'),[output])




#-----------------------------------------------------------------
final_time = time.time()
print (r'- Total execution time =', (final_time - start_time)/60., 'minutes')
