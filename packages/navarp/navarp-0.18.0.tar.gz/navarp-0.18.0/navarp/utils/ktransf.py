#!/usr/bin/env python

##############################################################################
##
# This file is part of NavARP
##
# Copyright 2016 CELLS / ALBA Synchrotron, Cerdanyola del Vallès, Spain
##
# NavARP is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
##
# NavARP is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
##
# You should have received a copy of the GNU General Public License
# along with NavARP.  If not, see <http://www.gnu.org/licenses/>.
##
##############################################################################

"""This module is part of the Python NavARP library. It defines the functions
for transforming the angular coordinates into the k-space."""

__author__ = ["Federico Bisti"]
__license__ = "GPL"
__date__ = "08/06/2017"

import numpy as np
# from numba import jit                       # speed up the code

from scipy.optimize import newton_krylov


# @jit
def asarray(variable):
    """Transform variable as ndarray

    Args:
        variable (float, int, list, ndarray): variable to transform
    Returns:
        variable (ndarray): variable transformed
    """
    if not isinstance(variable, np.ndarray):  # if not ndarray, def from it
        if isinstance(variable, list):
            variable = np.array(variable)
        else:
            variable = np.array([variable])
    elif variable.shape == ():  # if scalar ndarray, def a array ndarray
        variable = np.array([variable])
    return variable


def get_p_hv_along_slit(hv, tht_ph):
    """Calculates photon momentum along the slit,
        i.e. the intersection between the plane of analyzer axis and slit,
        and the plane of the sample surface.

    Args:
        hv (ndarray): Photon energy;
        tht_ph (ndarray): tht angle between surface normal and photons.
    Returns:
        p_hv_along_slit (ndarray): Photon momentum in plane along theta.
    """
    hv = asarray(hv)
    tht_ph = asarray(tht_ph)

    const = 2*np.pi/12400
    kx_hv = const*hv[:, None]*np.sin(np.radians(tht_ph[None, :]))

    return kx_hv


def get_p_hv_perp_slit(hv, tht_ph, phi_ph):
    """Calculates photon momentum perpendicular to the slit,
        i.e. the intersection between plane of analyzer axis and the
        perpendicular to the slit, and the plane of the sample surface.

    Args:
        hv (ndarray): Photon energy;
        tht_ph (ndarray): tht angle between surface normal and photons.
        phi_ph (ndarray): phi angle between surface normal and photons.
    Returns:
        p_hv_along_slit (ndarray): Photon momentum in plane along phi.
    """
    hv = asarray(hv)
    phi_ph = asarray(phi_ph)
    tht_ph = asarray(tht_ph)

    if len(hv.shape) > 1:
        print("Value Error: hv cannot have a dimension > 1.")
        return None

    const = 2*np.pi/12400
    ky_hv = const*hv*(np.cos(np.radians(tht_ph[None, :])) *
                      np.sin(np.radians(phi_ph[:, None])))

    return ky_hv


def get_p_hv_perp_sample(hv, tht_ph, phi_ph):
    """Calculates photon momentum perpendicular to the sample surface

    Args:
        hv (ndarray): Photon energy;
        tht_ph (ndarray): tht angle between surface normal and photons.
        phi_ph (ndarray): phi angle between surface normal and photons.
    Returns:
        p_hv_perp_sample (ndarray): Photon momentum in plane along theta.
    """
    hv = asarray(hv)
    tht_ph = asarray(tht_ph)
    phi_ph = asarray(phi_ph)

    if len(phi_ph.shape) > 1:
        print("Value Error: phi_ph cannot have a dimension > 1.")
        return None

    const = 2*np.pi/12400
    kz_hv = -const*hv[:, None]*(np.cos(np.radians(tht_ph[None, :])) *
                                np.cos(np.radians(phi_ph)))
    return kz_hv


def get_k_along_slit(e_kins, tht, tht_an, p_hv=False, hv=None, tht_ap=None):
    """Calculates k vector along the slit, i.e. the intersection between the
        plane of analyzer axis and slit, and the plane of the sample surface.

    Args:
        e_kins (ndarray): Kinetic energies (usually it is the energy axis of
            the analyzer data);
        tht (ndarray): Angular axis of the analyzer data;
        tht_an (float): angle between analyzer axis (a) and normal (n) to the
            surface along the plane of the slit (theta, so the name "tht_an");
        p_hv (boolean, optional): If True, add photon momentum;
        hv (ndarray): Photon energies;
        tht_ap (float): angle between analyzer axis (a) and photons (p) along
            the plane of the slit (theta, so the name "tht_ap").
    Returns:
        kx (ndarray): k vector along the slit
    """
    # Transform possible input (ndarray, list or value) into ndarray
    e_kins = asarray(e_kins)
    tht = asarray(tht)
    hv = asarray(hv)

    # Angle from normal of emitted electrons in radians
    tht_en = np.radians(tht-tht_an)

    # Calculate the electron momentum without photon one
    # "None" is for broadcasting
    # kx shape is (e_kins.shape[0], tht_en.shape[0], e_kins.shape[1]) or
    # (tht_en.shape[0], e_kins.shape[0])
    C_0 = 0.5124
    if len(e_kins.shape) == 2:
        kx = C_0*np.sqrt(e_kins[:, None, :])*np.sin(tht_en[None, :, None])
    else:
        kx = C_0*np.sqrt(e_kins[None, :])*np.sin(tht_en[:, None])

    # Substract the photon momentum if p_hv=True
    if p_hv:
        kx_hv = get_p_hv_along_slit(hv, -tht_ap + tht_an)
        if len(kx.shape) == 3:
            kx -= kx_hv[:, :, None]
        elif kx.shape[1] == kx_hv.shape[0]:
            kx -= kx_hv[None, :, 0]
        else:
            kx -= kx_hv

    kx = np.squeeze(kx)
    return kx


def get_k_perp_slit(e_kins, tht, tht_an, phi, phi_an,
                    p_hv=False, hv=None, tht_ap=None, phi_ap=None):
    """Calculates k vector perpendicular to the slit, i.e. the intersection
        between plane of analyzer axis and the perpendicular to the slit, and
        the plane of the sample surface.

    Args:
        e_kins (ndarray): Kinetic energies (usually it is the energy axis of
            the analyzer data);
        tht (ndarray): Angular axis of the analyzer data;
        tht_an (float): angle between analyzer axis (a) and normal (n) to the
            surface along the plane of the slit (theta, so the name "tht_an");
        phi (ndarray): angle perpendicular to the slit, this is the axis of
            the scan in the case of the deflector;
        phi_an (float): angle between analyzer axis (a) and normal (n) along
            the plane perpendicular to the slit (phi, so the name "phi_an"),
            this is the axis of the scan in the case of tilt rotation;
        p_hv (boolean, optional): If True, add photon momentum.
        hv (ndarray): Photon energies;
        tht_ap (float): angle between analyzer axis (a) and photons (p) along
            the plane of the slit (theta, so the name "tht_ap");
        phi_ap (float): angle between analyzer axis (a) and photons (p) along
            the plane perpendicular to the slit (phi, so the name "phi_ap");
    Returns:
        ky (ndarray): k vector perpendicular to the slit
    """
    # Transforming possible input (ndarray, list or value) into ndarray
    e_kins = asarray(e_kins)
    tht = asarray(tht)
    phi = asarray(phi)
    phi_an = asarray(phi_an)

    # Angles from normal of emitted electrons in radians
    phi_en = np.radians(phi-phi_an)
    tht_en = np.radians(tht-tht_an)

    if len(e_kins.shape) > 1:
        print("Value Error: e_kins cannot have a dimension > 1.")
        return None
    if len(phi.shape) > 1 and len(phi_an.shape) > 1:
        print("Value Error: both phi and phi_an cannot have a dimension > 1.")
        return None

    # Calculate the electron momentum without photon one
    # "None" is for broadcasting
    # ky shape is (phi_en.shape[0], tht_en.shape[0], e_kins.shape[0])
    C_0 = 0.5124
    if len(phi_en.ravel()) > 1:
        ky = C_0*np.sqrt(e_kins[None, None, :])*(
                np.cos(tht_en[None, :, None])*np.sin(phi_en[:, None, None]))
    else:
        ky = C_0*np.sqrt(e_kins[None, :])*(
                np.cos(tht_en[:, None])*np.sin(phi_en[0]))

    # Substract the photon momentum if p_hv=True
    if p_hv:
        ky_hv = get_p_hv_perp_slit(hv, -tht_ap+tht_an, -phi_ap+phi_an)
        if len(phi_en.ravel()) > 1:
            ky -= ky_hv[:, None]
        else:
            ky -= ky_hv

    ky = np.squeeze(ky)
    return ky


def get_k_perp_sample(e_kins, inn_pot, k_along_slit, k_perp_slit,
                      p_hv=False, hv=None, tht_ap=None, phi_ap=None,
                      tht_an=None, phi_an=None):
    """Calculates k vector perpendicular to sample surface.

    Args:
        e_kins (ndarray): Kinetic energies (usually it is the energy axis of
            the analyzer data);
        inn_pot (float): Inner potential, corresponding to the energy of the
            bottom of the valence band referenced to vacuum level;
        k_along_slit (ndarray): k vector along the slit
        k_perp_slit (ndarray): k vector perpendicular to the slit
        p_hv (boolean, optional): If True, add photon momentum.
        hv (ndarray): Photon energies;
        tht_ap (float): angle between analyzer axis (a) and photons (p) along
            the plane of the slit (theta, so the name "tht_ap");
        phi_ap (float): angle between analyzer axis (a) and photons (p) along
            the plane perpendicular to the slit (phi, so the name "phi_ap");
        tht_an (float): angle between analyzer axis (a) and normal (n) to the
            surface along the plane of the slit (theta, so the name "tht_an");
        phi_an (float): angle between analyzer axis (a) and normal (n) along
            the plane perpendicular to the slit (phi, so the name "phi_an"),
            this is the axis of the scan in the case of tilt rotation.
    Returns:
        kz (ndarray): k vector perpendicular to sample surface.
    """
    # Transforming possible input (ndarray, list or value) into ndarray
    tht_an = asarray(tht_an)
    phi_an = asarray(phi_an)
    e_kins = asarray(e_kins)
    k_along_slit = asarray(k_along_slit)
    k_perp_slit = asarray(k_perp_slit)

    if len(phi_an.shape) > 1:
        print("Value Error: phi_an cannot have a dimension > 1.")
        return None
    if len(k_perp_slit.shape) > 1:
        print("Value Error: phi_an cannot have a dimension > 1.")
        return None

    ekin_xy = (np.power(k_along_slit, 2) + np.power(k_perp_slit, 2))

    C_2 = 0.5124**2
    if len(e_kins.shape) == 2:
        kz = np.sqrt(C_2*(e_kins[:, None, :] + inn_pot) - ekin_xy)
    else:
        kz = np.sqrt(C_2*(e_kins[None, :] + inn_pot) - ekin_xy)

    # Substract the photon momentum if p_hv=True
    if p_hv:
        kz_hv = get_p_hv_perp_sample(hv, -tht_ap+tht_an, -phi_ap+phi_an)
        if len(kz.shape) == 3:
            kz -= kz_hv[:, :, None]
        elif kz.shape[1] == kz_hv.shape[0]:
            kz -= kz_hv[None, :, 0]
        else:
            kz -= kz_hv

    kz = np.squeeze(kz)
    return kz


def get_tht_an(e_kin_p, tht_p, k_along_slit_p, tht_an_init=0,
               p_hv=False, hv_p=None, tht_ap=None):
    """Calculates angle between analyzer axis (a) and normal (n) to the
            surface along the plane of the slit (theta, so the name "tht_an").

    Args:
        e_kin_p (float): Kinetic energy value of the reference point;
        tht_p (float): Angular value of the reference point along the angular
            axis of the analyzer data;
        k_along_slit_p (float): k vector value of the reference point, along
            the slit direction;
        tht_an_init (float, optional): Initial guess for the tht_an;
        p_hv (boolean, optional): If True, add photon momentum;
        hv_p (float, optional): Photon energy for the reference point,
            requested if p_hv==True;
        tht_ap (float, optional): angle between analyzer axis (a) and
            photons (p) along the plane of the slit (theta, so the name
            "tht_ap"), requested if p_hv==True.
    Returns:
        tht_an (float): angle between analyzer axis (a) and normal (n) to the
            surface along the plane of the slit (theta, so the name "tht_an").
    """
    return newton_krylov(lambda tht_an_x:
        get_k_along_slit(e_kin_p, tht_p, tht_an_x,
                         p_hv=p_hv, hv=hv_p, tht_ap=tht_ap) - k_along_slit_p,
                         tht_an_init)


def get_phi_an(e_kin_p, tht_p, tht_an, phi_p, k_perp_slit_p, phi_an_init=0,
               p_hv=False, hv_p=None, tht_ap=None, phi_ap=None):
    """Calculates angle between analyzer axis (a) and normal (n) along
            the plane perpendicular to the slit (phi, so the name "phi_an"),
            this is the axis of the scan in the case of tilt rotation;

    Args:
        e_kin_p (float): Kinetic energy value of the reference point;
        tht_p (float): Angular value of the reference point along the angular
            axis of the analyzer data;
        tht_an (float): angle between analyzer axis (a) and normal (n) to the
            surface along the plane of the slit (theta, so the name "tht_an");
        phi_p (float): Angular value of the reference point along the angle
            perpendicular to the slit;
        k_perp_slit_p (float): k vector value of the reference point,
            perpendicular to the slit;
        phi_an_init (float, optional): Initial guess for the phi_an;
        p_hv (boolean, optional): If True, add photon momentum;
        hv_p (float, optional): Photon energy for the reference point,
            requested if p_hv==True;
        tht_ap (float, optional): angle between analyzer axis (a) and
            photons (p) along the plane of the slit (theta, so the name
            "tht_ap"), requested if p_hv==True;
        phi_ap (float): angle between analyzer axis (a) and photons (p) along
            the plane perpendicular to the slit (phi, so the name "phi_ap");
    Returns:
        phi_an (float): angle between analyzer axis (a) and normal (n) along
            the plane perpendicular to the slit (phi, so the name "phi_an"),
            this is the axis of the scan in the case of tilt rotation.
    """
    return newton_krylov(lambda phi_an_x:
        get_k_perp_slit(e_kin_p, tht_p, tht_an, phi_p, phi_an_x,
                        p_hv=p_hv, hv=hv_p,
                        tht_ap=tht_ap, phi_ap=phi_ap) - k_perp_slit_p,
                        phi_an_init)


def get_hv_from_kxyz(e_bin_p, work_fun, inn_pot,
                     k_along_slit_p, k_perp_slit_p, k_perp_sample_p,
                     hv_p_init=30,
                     p_hv=False, tht_ap=0, phi_ap=0,
                     tht_an=None, phi_an=None):
    """Calculates photon energy of a point from k-space coordinates

    Args:
        e_bin_p (float): Binding energy value of the point;
        work_fun (float): analyzer work function;
        inn_pot (float): Inner potential, corresponding to the energy of the
            bottom of the valence band referenced to vacuum level;
        k_along_slit_p (float): k vector value of the reference point, along
            the slit direction;
        k_perp_slit_p (float): k vector value of the reference point,
            perpendicular to the slit;
        k_perp_sample_p (float): k vector perpendicular to sample surface
        hv_p_init (float): Initial guess for the photon energy of the
            reference point;
        p_hv (boolean, optional): If True, add photon momentum;
        tht_ap (float, optional): angle between analyzer axis (a) and
            photons (p) along the plane of the slit (theta, so the name
            "tht_ap"), requested if p_hv==True;
        phi_ap (float): angle between analyzer axis (a) and photons (p) along
            the plane perpendicular to the slit (phi, so the name "phi_ap");
        tht_an (float): angle between analyzer axis (a) and normal (n) to the
            surface along the plane of the slit (theta, so the name "tht_an");
        phi_an (float): angle between analyzer axis (a) and normal (n) along
            the plane perpendicular to the slit (phi, so the name "phi_an"),
            this is the axis of the scan in the case of tilt rotation.
    Returns:
        hv_p (float): Photon energy of the point;
    """
    return newton_krylov(lambda x_hv_p:
        get_k_perp_sample((x_hv_p - work_fun + e_bin_p),
                          inn_pot, k_along_slit_p, k_perp_slit_p,
                          p_hv=p_hv, hv=x_hv_p, tht_ap=tht_ap, phi_ap=phi_ap,
                          tht_an=tht_an, phi_an=phi_an) - k_perp_sample_p,
                         hv_p_init)


def get_inn_pot_from_kxyz(e_kin_p,
                          k_along_slit_p, k_perp_slit_p, k_perp_sample_p,
                          inn_pot_init=10,
                          p_hv=False, hv_p=None, tht_ap=0, phi_ap=0,
                          tht_an=None, phi_an=None):
    """Calculates photon energy of a point from k-space coordinates

    Args:
        e_kin_p (float): Kinetic energy value of the reference point;
        inn_pot_init (float): Initial guess for the inner potential,
            corresponding to the energy of the bottom of the valence band
            referenced to vacuum level;
        k_along_slit_p (float): k vector value of the reference point, along
            the slit direction;
        k_perp_slit_p (float): k vector value of the reference point,
            perpendicular to the slit;
        k_perp_sample_p (float): k vector perpendicular to sample surface
        hv (ndarray): Photon energies;
        p_hv (boolean, optional): If True, add photon momentum;
        hv_p (float, optional): Photon energy for the reference point,
            requested if p_hv==True;
        tht_ap (float, optional): angle between analyzer axis (a) and
            photons (p) along the plane of the slit (theta, so the name
            "tht_ap"), requested if p_hv==True;
        phi_ap (float): angle between analyzer axis (a) and photons (p) along
            the plane perpendicular to the slit (phi, so the name "phi_ap");
        tht_an (float): angle between analyzer axis (a) and normal (n) to the
            surface along the plane of the slit (theta, so the name "tht_an");
        phi_an (float): angle between analyzer axis (a) and normal (n) along
            the plane perpendicular to the slit (phi, so the name "phi_an"),
            this is the axis of the scan in the case of tilt rotation.
    Returns:
        inn_pot (float): Inner potential, corresponding to the energy of the
            bottom of the valence band referenced to vacuum level.
    """
    return newton_krylov(lambda x_inn_pot:
        get_k_perp_sample(e_kin_p,
                          x_inn_pot, k_along_slit_p, k_perp_slit_p,
                          p_hv=p_hv, hv=hv_p, tht_ap=tht_ap, phi_ap=phi_ap,
                          tht_an=tht_an, phi_an=phi_an) - k_perp_sample_p,
                         inn_pot_init)


def get_surface_normal(entry, refs_p):
    """Calculates tht_an, phi_an, scans_0 and phi.

    Args:
        entry (NavEntry class): the class for the data explored by NavARP;
        refs_p (dict): dictionary of the reference point in angle and k space.
    Returns:
        hv_p (float): Photon energy of the point;
    """

    tht_p = refs_p["tht_p"]
    hv_p = refs_p["hv_p"]
    e_kin_p = refs_p["e_kin_p"]
    k_along_slit_p = refs_p["k_along_slit_p"]
    p_hv = refs_p["p_hv"]

    tht_ap = entry.analyzer.tht_ap
    phi_ap = entry.analyzer.phi_ap

    # The photon momentum shifts the G point from (Kx, Ky) = (0, 0)
    # In the following code-line the real angle value is calculated
    # from the G point by removing the photon momentum contribution
    # in this way G point remains fixed for all the photon energies
    # because the photon momentum is taken into account
    tht_an = get_tht_an(e_kin_p, tht_p, k_along_slit_p, tht_an_init=tht_p,
                        p_hv=p_hv, hv_p=hv_p, tht_ap=tht_ap)
    print("tht_an = {:0.3f}".format(tht_an))

    if entry.scan_type == "hv":
        phi_an = 0
        scans_0 = 0
    elif (entry.scan_type == "polar" or entry.scan_type == "tilt"):
        tilt_p = refs_p["scan_p"]
        phi_p = entry.defl_angles
        phi_an_p = get_phi_an(e_kin_p, tht_p, tht_an, phi_p, refs_p["ks_p"],
                              phi_an_init=0,
                              p_hv=p_hv, hv_p=hv_p,
                              tht_ap=tht_ap, phi_ap=phi_ap)
        print("phi_an_p = {:0.3f}".format(phi_an_p))
        scans_0 = tilt_p - phi_an_p
        print("scans_0 = {:0.3f}".format(scans_0))
        phi_an = entry.scans - scans_0
    elif entry.scan_type == "deflector":
        phi_p = refs_p["scan_p"]
        phi_an_p = get_phi_an(e_kin_p, tht_p, tht_an, phi_p, refs_p["ks_p"],
                              phi_an_init=0,
                              p_hv=p_hv, hv_p=hv_p,
                              tht_ap=tht_ap, phi_ap=phi_ap)
        print("phi_an_p = {:0.3f}".format(phi_an_p))
        scans_0 = phi_an_p
        print("scans_0 = {:0.3f}".format(scans_0))
        phi_an = phi_an_p
    else:
        phi_an = 0
        scans_0 = 0

    return tht_an, phi_an, scans_0


def get_k_isoen(entry, e_kin_val, tht_an, phi_an,
                k_perp_slit_for_kz=0, inn_pot=14, p_hv=False):
    """Calculates k vectors of the iso-energy cut.

    Args:
        entry (NavEntry class): the class for the data explored by NavARP;
        e_kin_val (float or ndarray): Kinetic energy/ies of iso-energy cut;
        tht_an (float): angle between analyzer axis (a) and normal (n) to the
            surface along the plane of the slit (theta, so the name "tht_an");
        phi_an (float): angle between analyzer axis (a) and normal (n) along
            the plane perpendicular to the slit (phi, so the name "phi_an"),
            this is the axis of the scan in the case of tilt rotation;
        k_perp_slit_p (float): k vector value perpendicular to the slit, in the
            case of scan_type=='hv' (usually = 0);
        inn_pot (float): Inner potential, corresponding to the energy of the
            bottom of the valence band referenced to vacuum level;
        p_hv (boolean, optional): If True, add photon momentum.
    """

    tht_ap = entry.analyzer.tht_ap
    phi_ap = entry.analyzer.phi_ap

    kx_isoen = get_k_along_slit(e_kin_val, entry.angles, tht_an,
                                p_hv=p_hv, hv=entry.hv, tht_ap=tht_ap)

    if entry.scan_type == "hv":
        ks_isoen = get_k_perp_sample(
                e_kin_val, inn_pot, kx_isoen, k_perp_slit_for_kz,
                p_hv=p_hv, hv=entry.hv,
                tht_ap=tht_ap, phi_ap=phi_ap,
                tht_an=tht_an, phi_an=phi_an)
    elif (entry.scan_type == "polar" or entry.scan_type == "tilt"):
        ks_isoen = get_k_perp_slit(
                e_kin_val, entry.angles, tht_an,
                entry.defl_angles, phi_an,
                p_hv=p_hv, hv=entry.hv,
                tht_ap=tht_ap, phi_ap=phi_ap)
    elif entry.scan_type == "deflector":
        ks_isoen = get_k_perp_slit(
                e_kin_val, entry.angles, tht_an,
                entry.scans, phi_an,
                p_hv=p_hv, hv=entry.hv,
                tht_ap=tht_ap, phi_ap=phi_ap)
    elif entry.scan_type == "azimuth":
        scans_rad = np.radians(entry.scans)
        krho = kx_isoen
        kx_isoen = np.squeeze(krho * np.cos(scans_rad)[:, None, None])
        ks_isoen = np.squeeze(krho * np.sin(scans_rad)[:, None, None])
    else:
        ks_isoen = entry.scans

    return kx_isoen, ks_isoen


# ----------------------------------------------------------------------------
# -------------------- WRONG ky ----------------------------------------------
# if kx = constant * sin(theta),
# then ky = constant * cos(theta) sin(phi)
# @jit
def get_kxy_el_no_hv_depr(ekin, angle):
    """Calculates in plane k vector for given kinetic energy and angle

    Args:
        ekin (ndarray): Kinetic energies;
        angle (ndarray): Angles of emission;
    Returns:
        kxy (ndarray): In plane k vector.
    """
    return 0.5124*np.sqrt(ekin) * np.sin(np.radians(angle))


# @jit
def get_kx_hv_depr(hv, tht_to_normal):
    """Calculates photon momentum along the intersection between the plane of
        photons and analyzer axis, and the plane of the sample surface.

    Args:
        hv (ndarray): Photon energy;
        tht_to_normal (ndarray): tht angle between surface and photon.
    Returns:
        kx_hv (ndarray): Photon momentum in plane along theta.
    """
    hv = asarray(hv)
    tht_to_normal = asarray(tht_to_normal)

    kx_hv = np.zeros((hv.shape[0], tht_to_normal.shape[0]))
    for i, hv_i in enumerate(hv):
        kx_hv[i, :] = 2*np.pi*hv_i*np.cos(np.radians(tht_to_normal))/12400

    return kx_hv


# @jit
def get_ky_hv_depr(hv, tht_to_normal, phi_to_normal):
    """Calculates photon momentum along the intersection between the plane
        perpendicular to photons and the sample surface.

    Args:
        hv (ndarray): Photon energy;
        tht_to_normal (ndarray): tht angle between surface and photon;
        phi_to_normal (ndarray): phi angle between surface and photon.
    Returns:
        ky_hv (ndarray): photon momentum in plane along phi.
    """
    hv = asarray(hv)
    tht_to_normal = asarray(tht_to_normal)
    phi_to_normal = asarray(phi_to_normal)

    ky_hv = np.zeros((hv.shape[0], phi_to_normal.shape[0]))
    for i, hv_i in enumerate(hv):
        ky_hv[i, :] = (2*np.pi*hv_i*np.sin(np.radians(tht_to_normal)) *
                       np.sin(np.radians(phi_to_normal))/12400)

    return ky_hv


# @jit
def get_kz_hv_depr(hv, tht_to_normal, phi_to_normal):
    """Calculates photon momentum perpendicular to the sample surface.

    Args:
        hv (ndarray): Photon energy;
        tht_to_normal (ndarray): tht angle between surface and photon;
        phi_to_normal (ndarray): phi angle between surface and photon.
    Returns:
        kz_hv (ndarray): photon momentum out of plane.
    """
    hv = asarray(hv)
    tht_to_normal = asarray(tht_to_normal)
    phi_to_normal = asarray(phi_to_normal)

    kz_hv = np.zeros((hv.shape[0], phi_to_normal.shape[0]))
    for i, hv_i in enumerate(hv):
        kz_hv[i, :] = (2*np.pi*hv_i*np.sin(np.radians(tht_to_normal)) *
                       np.cos(np.radians(phi_to_normal))/12400)

    return kz_hv


# @jit
def get_kx_depr(tht, energies, hv, wfa, alpha, tht_anlz, p_hv=True, defl=True):
    """Calculates k vector along the intersection between the plane of
        photons and analyzer axis, and the plane of the sample surface.

    Args:
        tht (ndarray): Angular axis of the analyzer data;
        energies (ndarray): Energy axis of the analyzer data;
        hv (ndarray): Photon energies;
        wfa (float): Work function of the analyzer;
        alpha (float): Complementary angle to the one between analyzer axis
            and photons;
        tht_anlz (float): Angle between normal to the surface and analyzer
            axis;
        p_hv (boolean, optional): If True, add photon momentum;
        defl (boolean, optional): if True, the manipulator is fixed while
            scanning along tht, so no modification in the photon momentum.
    Returns:
        kx (ndarray): k vector in plane along photon direction
    """
    # Transforming possible input (ndarray, list or value) into ndarray
    tht = asarray(tht)
    energies = asarray(energies)
    hv = asarray(hv)

    kx = np.zeros((hv.shape[0], tht.shape[0], energies.shape[0]))
    for i, hv_i in enumerate(hv):
        for j, energies_j in enumerate(energies):
            kx[i, :, j] = get_kxy_el_no_hv(hv_i-wfa+energies_j, tht+tht_anlz)

    if p_hv:
        if defl:
            kx_hv = get_kx_hv(hv, alpha+tht_anlz)
        else:
            kx_hv = get_kx_hv(hv, alpha+tht+tht_anlz)
        kx_hv = np.transpose(np.tile(kx_hv, (energies.shape[0], 1, 1)),
                             (1, 2, 0))
        kx -= kx_hv

    kx = np.squeeze(kx)
    return kx


# @jit
def get_ky_depr(phi, energies, hv, wfa, alpha, tht_anlz, phi_anlz,
           p_hv=True, defl=False):
    """Calculates k vector along the intersection between the plane
        perpendicular to photons and the sample surface.

    Args:
        phi (ndarray): Angular axis of the scan;
        energies (ndarray): Energy axis of the analyzer data;
        hv (ndarray): Photon energies;
        wfa (float): Work function of the analyzer;
        alpha (float): Complementary angle to the one between analyzer axis
            and photons;
        tht_anlz (float): tht angle between normal to the surface and analyzer
            axis;
        phi_anlz (float): phi angle between normal to the surface and analyzer
            axis;
        p_hv (boolean, optional): If True, add photon momentum;
        defl (boolean, optional): if True, the manipulator is fixed while
            scanning along phi, so no modification in the photon momentum.
    Returns:
        ky (ndarray): k vector in plane perpendicular to photon direction
    """
    # Checking the input between the possible ones: np.ndarray, list or value
    phi = asarray(phi)
    energies = asarray(energies)
    hv = asarray(hv)

    ky = np.zeros((hv.shape[0], phi.shape[0], energies.shape[0]))
    for i, hv_i in enumerate(hv):
        for j, energies_j in enumerate(energies):
            ky[i, :, j] = get_kxy_el_no_hv(hv_i-wfa+energies_j, phi-phi_anlz)

    if p_hv:
        if defl:
            ky_hv = get_ky_hv(hv, alpha+tht_anlz, phi_anlz)
        else:
            ky_hv = get_ky_hv(hv, alpha+tht_anlz, phi-phi_anlz)
        ky_hv = np.transpose(np.tile(ky_hv, (energies.shape[0], 1, 1)),
                             (1, 2, 0))
        ky += ky_hv

    ky = np.squeeze(ky)
    return ky


# @jit
def get_kz_depr(kx, ky, energies, hv, alpha, tht_anlz, inn_pot,
           phi_anlz=0, p_hv=True):
    """Calculates k vector perpendicular to sample surface.

    Args:
        kx (ndarray): k vector in plane along photon direction
        ky (ndarray): k vector in plane perpendicular to photon direction
        energies (ndarray): Energy axis of the analyzer data;
        hv (ndarray): Photon energies;
        alpha (float): Complementary angle to the one between analyzer axis
            and photons;
        tht_anlz (float): tht angle between normal to the surface and analyzer
            axis;
        inn_pot (float): Inner potential, corresponding to the energy of the
            bottom of the valence band referenced to vacuum level;
        phi_anlz (float): phi angle between normal to the surface and analyzer
            axis;
        p_hv (boolean, optional): If True, add photon momentum.
    Returns:
        kz (ndarray): k vector perpendicular to sample surface
    """
    # Transforming possible input (ndarray, list or value) into ndarray
    kx = asarray(kx)
    ky = asarray(ky)
    energies = asarray(energies)
    hv = asarray(hv)

    # only kx or ky can be an array, the other one must be a single value
    if len(kx.ravel()) > 1 and len(ky.ravel()) == 1:
        karr = kx
        kfix = ky
    elif len(ky.ravel()) > 1 and len(kx.ravel()) == 1:
        karr = ky
        kfix = kx
    elif len(kx.ravel()) == 1 and len(ky.ravel()) == 1:
        karr = np.tile(kx, (1, 1, 1))
        kfix = ky
    else:
        print("Value Error: only one k variable (kx or ky) can be an array," +
              " the other one must be a single value.")

    # karr can be 1-dimensional, and it can be:
    #     karr[hv] or karr[energies] or karr[angles]
    # For these 3 different cases, it must be transformed as:
    #     karr[hv, angles, energies]
    if len(karr.shape) == 1:
        if karr.shape[0] == hv.shape[0]:  # karr[hv]
            karr = np.transpose(np.tile(karr, (energies.shape[0], 1, 1)),
                                (2, 1, 0))
        elif karr.shape[0] == energies.shape[0]:  # karr[energies]
            karr = np.tile(karr, (hv.shape[0], 1, 1))

        else:  # karr[angles]
            karr = np.transpose(np.tile(karr,
                                        (hv.shape[0], energies.shape[0], 1)),
                                (0, 2, 1))

    # karr can be 2-dimensional, and it can be:
    #     karr[hv, energies] or karr[hv, angles] or karr[angles, energies]
    # For these 3 different cases, it must be transformed as:
    #     karr[hv, angles, energies]
    elif len(karr.shape) == 2:
        if karr.shape[0] == hv.shape[0]:  # karr[hv, :]
            if karr.shape[1] == energies.shape[0]:  # karr[hv, energies]
                karr = np.transpose(np.tile(karr, (1, 1, 1)), (1, 0, 2))
            else:  # karr[hv, angles]
                karr = np.transpose(np.tile(karr, (energies.shape[0], 1, 1)),
                                    (1, 2, 0))
        elif karr.shape[1] == energies.shape[0]:  # karr[:, energies]
            karr = np.tile(karr, (hv.shape[0], 1, 1))

    # karr can be 3-dimensional, but has to be karr[hv, angles, energies]:
    elif len(karr.shape) == 3:
        if karr.shape[0] != hv.shape[0] or karr.shape[2] != energies.shape[0]:
            print("Value Error: kx (or ky) must have the following size: " +
                  "karr[hv, angles, energies], instead it is:" +
                  "\n karr.shape = ", karr.shape,
                  "\n hv.shape = ", hv.shape,
                  "\n energies.shape = ", energies.shape)

    # karr cannot be more than 3-dimensional:
    else:
        print("Value Error: kx (or ky) cannot have a dimension > 3.")

    C_0 = 0.5124
    C_1 = 1/C_0**2
    kz = np.zeros((hv.shape[0], karr.shape[1], energies.shape[0]))
    for i, hv_i in enumerate(hv):
        for j, energies_j in enumerate(energies):
            ekin_xy = C_1*(np.power(karr[i, :, j], 2) + np.power(kfix, 2))
            kz[i, :, j] = (C_0*np.sqrt(hv_i + energies_j +
                                          inn_pot - ekin_xy))
    if p_hv:
        kz_hv = get_kz_hv(hv, alpha+tht_anlz, phi_anlz)
        kz_hv = np.transpose(np.tile(kz_hv, (energies.shape[0], 1, 1)),
                             (1, 2, 0))
        kz += kz_hv

    kz = np.squeeze(kz)
    return kz


def get_tht_manip_depr(tht_p, en_p, hv_p, kx_p, wfa, alpha, tht_anlz_init):
    """Calculates angle between normal to the surface and analyzer axis

    Args:
        tht_p (float): Angular value of the reference point along the angular
            axis of the analyzer data;
        en_p (float): Energy value of the reference point;
        hv_p (float): Photon energy for the reference point;
        kx_p (float): k vector value of the reference point, in plane along
            photon direction
        wfa (float): Work function of the analyzer;
        alpha (float): Complementary angle to the one between analyzer axis
            and photons;
        tht_anlz_init (float): Initial guess for the angle between normal to
            the surface and analyzer axis (tht_manip);
    Returns:
        tht_manip (float): tht angle between normal to the surface and analyzer
            axis;
    """
    return newton_krylov(lambda x_tht_anlz:
                         get_kx(tht_p, en_p, hv_p, wfa, alpha, x_tht_anlz) -
                         kx_p, tht_anlz_init)


def get_hv_p_depr(kx_p, ky_p, kz_p, en_p, hv_p_init, alpha, tht_anlz, inn_pot):
    """Calculates photon energy of a point from k-space coordinates

    Args:
        kx_p (float): k vector value of the point along the intersection
            between the plane of photons and analyzer axis, and the plane of
            the sample surface;
        ky_p (float): k vector value of the point along the intersection
            between the plane perpendicular to photons and the sample surface;
        kz_p (float): k vector value of the point, perpendicular to sample
            surface;
        en_p (float): Energy value of the point;
        hv_p_init (float): Initial guess for the photon energy of the
            reference point;
        alpha (float): Complementary angle to the one between analyzer axis
            and photons;
        tht_anlz (float): tht angle between normal to the surface and analyzer
            axis;
        inn_pot (float): Inner potential, corresponding to the energy of the
            bottom of the valence band referenced to vacuum level;
    Returns:
        hv_p (float): Photon energy of the point;
    """
    return newton_krylov(
        lambda x_hv_p:
        0.5124**2*(x_hv_p + en_p + inn_pot - 3.81*(kx_p**2 + ky_p**2)) -
        (kz_p - 2*np.pi*x_hv_p*np.sin(np.radians(alpha+tht_anlz)) /
         12400)**2, hv_p_init)
