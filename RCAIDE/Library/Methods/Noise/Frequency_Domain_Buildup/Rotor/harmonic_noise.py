## @ingroup Methods-Noise-Frequency_Domain_Buildup-Rotor 
# RCAIDE/Methods/Noise/Frequency_Domain_Buildup/Rotor/harmonic_noise.py
# 
# 
# Created:  Jul 2023, M. Clarke  

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE    
from RCAIDE.Library.Methods.Noise.Common                         import convert_to_third_octave_band

# Python Package imports  
import numpy as np
from scipy.special import jv 
import scipy as sp

# ----------------------------------------------------------------------------------------------------------------------
# Compute Harmonic Noise 
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Methods-Noise-Frequency_Domain_Buildup-Rotor 
def harmonic_noise(harmonics,freestream,angle_of_attack,coordinates,
                           velocity_vector,rotor,aeroacoustic_data,settings,res):
    '''This computes the  harmonic noise (i.e. thickness and loading noise) of a rotor or rotor
    in the frequency domain

    Assumptions:
    Compactness of thrust and torque along blade radius from root to tip

    Source:
    1) Hanson, Donald B. "Helicoidal surface theory for harmonic noise of rotors in the far field."
    AIAA Journal 18.10 (1980): 1213-1220.

    2) Hubbard, Harvey H., ed. Aeroacoustics of flight vehicles: theory and practice. Vol. 1.
    NASA Office of Management, Scientific and Technical Information Program, 1991.


    Inputs: 
        harmonics                     - harmomics                                                                  [Unitless]
        freestream                    - freestream data structure                                                  [m/s]
        angle_of_attack               - aircraft angle of attack                                                   [rad]
        position_vector               - position vector of aircraft                                                [m]
        velocity_vector               - velocity vector of aircraft                                                [m/s] 
        rotors                        - data structure of rotors                                                   [None]
        aeroacoustic_data             - data structure of acoustic data                                            [None]
        settings                      - accoustic settings                                                         [None] 
        res                           - results data structure                                                     [None] 

    Outputs 
        res.                                    *acoustic data is stored and passed in data structures*                                                                            
            SPL_prop_harmonic_bpf_spectrum       - harmonic noise in blade passing frequency spectrum              [dB]
            SPL_prop_harmonic_bpf_spectrum_dBA   - dBA-Weighted harmonic noise in blade passing frequency spectrum [dbA]                  
            SPL_prop_harmonic_1_3_spectrum       - harmonic noise in 1/3 octave spectrum                           [dB]
            SPL_prop_harmonic_1_3_spectrum_dBA   - dBA-Weighted harmonic noise in 1/3 octave spectrum              [dBA] 
            p_pref_harmonic                      - pressure ratio of harmonic noise                                [Unitless]
            p_pref_harmonic_dBA                  - pressure ratio of dBA-weighted harmonic noise                   [Unitless]


    Properties Used:
        N/A   
    '''     
    num_h        = len(harmonics)     
    num_cpt      = len(angle_of_attack) 
    num_mic      = len(coordinates.X_hub[0,:,0,0,0,0])
    num_rot      = len(coordinates.X_hub[0,0,:,0,0,0]) 
    phi_0        = np.array([rotor.phase_offset_angle])  # phase angle offset  
    num_sec      = len(rotor.radius_distribution) 
    orientation  = np.array(rotor.orientation_euler_angles) * 1 
    body2thrust  = sp.spatial.transform.Rotation.from_rotvec(orientation).as_matrix()
    
    # ----------------------------------------------------------------------------------
    # Rotational Noise  Thickness and Loading Noise
    # ----------------------------------------------------------------------------------  
    # [control point ,microphones, rotors, radial distribution, harmonics]  
    m              = np.tile(harmonics[None,None,None,None,:],(num_cpt,num_mic,num_rot,num_sec,1))                 # harmonic number 
    m_1d           = harmonics                                                                                         
    p_ref          = 2E-5                                                                                        # referece atmospheric pressure
    a              = np.tile(freestream.speed_of_sound[:,:,None,None,None],(1,num_mic,num_rot,num_sec,num_h))      # speed of sound
    rho            = np.tile(freestream.density[:,:,None,None,None],(1,num_mic,num_rot,num_sec,num_h))             # air density   
    alpha          = np.tile((angle_of_attack + np.arccos(body2thrust[0,0]))[:,:,None,None,None],(1,num_mic,num_rot,num_sec,num_h))          
    B              = rotor.number_of_blades                                                                      # number of rotor blades
    omega          = np.tile(aeroacoustic_data.omega[:,:,None,None,None],(1,num_mic,num_rot,num_sec,num_h))        # angular velocity       
    dT_dr          = np.tile(aeroacoustic_data.blade_dT_dr[:,None,None,:,None],(1,num_mic,num_rot,1,num_h))      # nondimensionalized differential thrust distribution 
    dQ_dr          = np.tile(aeroacoustic_data.blade_dQ_dr[:,None,None,:,None],(1,num_mic,num_rot,1,num_h))      # nondimensionalized differential torque distribution
    R              = np.tile(rotor.radius_distribution[None,None,None,:,None],(num_cpt,num_mic,num_rot,1,num_h)) # radial location     
    c              = np.tile(rotor.chord_distribution[None,None,None,:,None],(num_cpt,num_mic,num_rot,1,num_h))  # blade chord    
    R_tip          = rotor.tip_radius                                                     
    t_c            = np.tile(rotor.thickness_to_chord[None,None,None,:,None],(num_cpt,num_mic,num_rot,1,num_h))  # thickness to chord ratio
    MCA            = np.tile(rotor.mid_chord_alignment[None,None,None,:,None],(num_cpt,num_mic,num_rot,1,num_h)) # Mid Chord Alighment  
    phi_0_vec      = np.tile(phi_0[None,None,:,None,None],(num_cpt,num_mic,1,num_sec,num_h))
    res.f          = B*omega*m/(2*np.pi) 
    D              = 2*R[0,0,0,-1,:]                                                                             # rotor diameter    
    r              = R/R[0,0,0,-1,:]                                                                             # non dimensional radius distribution   
    Y              = np.tile(np.sqrt(coordinates.X_hub[:,:,:,0,:,1]**2 +  coordinates.X_hub[:,:,:,0,:,2] **2)[:,:,:,:,None],(1,1,1,1,num_h))                        # observer distance from rotor axis          
    V              = np.tile(np.linalg.norm(velocity_vector,axis =1) [:,None,None,None,None],(1,num_mic,num_rot,num_sec,num_h))                                                     # velocity magnitude
    M_x            = V/a                                                                                         
    V_tip          = R_tip*omega                                                                                 # blade_tip_speed 
    M_t            = V_tip/a                                                                                     # tip Mach number 
    M_r            = np.sqrt(M_x**2 + (r**2)*(M_t**2))                                                           # section relative Mach number     
    B_D            = c/D     
     
    phi            = np.tile(coordinates.phi_hub_r[:,:,:,0,:,None],(1,1,1,1,num_h)) + phi_0_vec 

    # retarted theta angle in the retarded reference frame
    theta_r        = np.tile(coordinates.theta_hub_r[:,:,:,0,:,None],(1,1,1,1,num_h))  
    theta_r_prime  = np.arccos(np.cos(theta_r)*np.cos(alpha) + np.sin(theta_r)*np.sin(phi)*np.sin(alpha) )
    S_r            = np.tile(np.linalg.norm(coordinates.X_hub_r[:,:,:,0,:,:], axis = 4)[:,:,:,:,None],(1,1,1,1,num_h))  

    # initialize thickness and loading noise matrices
    psi_L          = np.zeros((num_cpt,num_mic,num_rot,num_sec,num_h))
    psi_V          = np.zeros((num_cpt,num_mic,num_rot,num_sec,num_h))

    # normalized thickness  and loading shape functions                
    k_x               = ((2*m*B*B_D*M_t)/(M_r*(1 - M_x*np.cos(theta_r))))      # wave number 
    psi_V[:,:,:,0,:]  = 2/3   
    psi_L[:,:,:,0,:]  = 1     
    psi_V[:,:,:,1:,:] = (8/(k_x[:,:,:,1:,:]**2))*((2/k_x[:,:,:,1:,:])*np.sin(0.5*k_x[:,:,:,1:,:]) - np.cos(0.5*k_x[:,:,:,1:,:]))    
    psi_L[:,:,:,1:,:] = (2/k_x[:,:,:,1:,:])*np.sin(0.5*k_x[:,:,:,1:,:])                  

    # sound pressure for thickness noise   
    Jmb               = jv(m*B,((m*B*r*M_t*np.sin(theta_r_prime))/(1 - M_x*np.cos(theta_r))))  
    phi_s             = ((2*m*B*M_t)/(M_r*(1 - M_x*np.cos(theta_r))))*(MCA/D)
    phi_prime_var     = (np.sin(theta_r)/np.sin(theta_r_prime))*np.cos(phi)
    phi_prime_var[phi_prime_var>1.0] = 1.0
    phi_prime         = np.arccos(phi_prime_var)                                                                                
    exponent_fraction = np.exp(1j*m_1d*B*((omega*S_r/a) +  phi_prime - np.pi/2))/(1 - M_x*np.cos(theta_r))
    p_mT_H_integral   = -((M_r**2)*(t_c)*np.exp(1j*phi_s)*Jmb*(k_x**2)*psi_V ) * ((rho*(a**2)*B*np.sin(theta_r))/(4*np.sqrt(2)*np.pi*(Y/D)))* exponent_fraction
    p_mT_H            = np.trapz(p_mT_H_integral,x = r[0,0,0,:,0], axis =3) 

    p_mT_H_abs        = abs(p_mT_H)             
    p_mL_H_integral   = (((np.cos(theta_r_prime)/(1 - M_x*np.cos(theta_r)))*dT_dr - (1/((r**2)*M_t*R_tip))*dQ_dr)
                         * np.exp(1j*phi_s)*Jmb * psi_L)*(m_1d*B*M_t*np.sin(theta_r)/ (2*np.sqrt(2)*np.pi*Y*R_tip)) *exponent_fraction
    p_mL_H            = np.trapz(p_mL_H_integral,x = r[0,0,0,:,0], axis = 3 ) 
    p_mL_H_abs        =  abs(p_mL_H)  

    # sound pressure levels  
    res.SPL_prop_harmonic_bpf_spectrum     = 20*np.log10((abs(p_mL_H_abs + p_mT_H_abs))/p_ref)  
    res.SPL_prop_harmonic_1_3_spectrum     = convert_to_third_octave_band(res.SPL_prop_harmonic_bpf_spectrum,res.f[:,0,0,0,:],settings)          
    res.SPL_prop_harmonic_1_3_spectrum[np.isinf(res.SPL_prop_harmonic_1_3_spectrum)]         = 0 

    return