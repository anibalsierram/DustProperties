#-----------------------
#Opacities
#-----------------------
def Opas(pslope, wls):
    with np.load(params['Opacities']) as d:
        a_w     = d['a'].T
        gsca_w  = d['g'].T
        lam_w   = d['lam'].T
        k_abs_w = d['k_abs'].T
        k_sca_w = d['k_sca'].T
        
    lam_avgs = wls
    # We split the opacities within the range of frequency to make the calculations faster
    k_abs_w = k_abs_w[(0.9*lam_avgs[0]<lam_w) & (1.1*lam_avgs[-1]>lam_w),:]
    k_sca_w = k_sca_w[(0.9*lam_avgs[0]<lam_w) & (1.1*lam_avgs[-1]>lam_w),:]
    k_sca_w = k_sca_w*(1. -  gsca_w[(0.9*lam_avgs[0]<lam_w) & (1.1*lam_avgs[-1]>lam_w),:])
    lam_w = lam_w[(0.9*lam_avgs[0]<lam_w) & (1.1*lam_avgs[-1]>lam_w)]

    opac_grid = opacity.size_average_opacity(lam_avgs, a_w, lam_w, k_abs_w.T, k_sca_w.T,
                                                 q=pslope, plot=False)

    kappa = interpolate.interp1d(a_w, np.squeeze(opac_grid['ka']), kind='linear',bounds_error=True)
    sigma = interpolate.interp1d(a_w, np.squeeze(opac_grid['ks']), kind='linear',bounds_error=True)
    return kappa, sigma


#-----------------------
# Intensity
#-----------------------
def FScattering(nus, Td, sigma, amax, mu):
    tau = sigma*(opa_abs(amax) + opa_sca(amax))
    albedo = opa_sca(amax)/(opa_sca(amax) + opa_abs(amax))
    epsilon = 1.0 - albedo
    a = np.sqrt(3.*epsilon)
    inte = ( 1.-np.exp( -( a+1./mu )*tau) ) / ( a*mu+1. ) + (np.exp(-tau/mu) - np.exp(-a*tau)  )/ (a*mu-1.)
    inte = inte / ( np.exp( -a*tau)*(np.sqrt(epsilon)-1.) - (np.sqrt(epsilon)+1.) )
    mod = 1.-np.exp(-tau/mu) +albedo*inte

    return ( 2.*hP*nus**3/clight**2/( np.exp( hP*nus/( kB*Td ) )-1. ) )*mod /Jy #[Jy/sr]

#-----------------------
# Posterior
#-----------------------
def lnpostfn(params, min_par, max_par, Flux, EFlux, Weights, mu, nus, guess, Eguess, radius):

    #Check parameters are within range
    for i in range(len(params)):
        if((params[i] > max_par[i]) or (params[i]< min_par[i])):
            return -np.inf
    Temp, sigma, amax = 10**params
    
    Model = FScattering(nus, Temp, sigma, amax, mu)
    Chi2 = np.sum( Weights * (Flux - Model)**2/EFlux**2)
    return -0.5*Chi2 + lnpriorfn((Temp, sigma, amax), guess, Eguess) + lnTprior(radius, Temp)

def lnpriorfn(params, guess, Eguess):   
    return -0.5* np.sum( (params - guess)**2/Eguess**2    )
