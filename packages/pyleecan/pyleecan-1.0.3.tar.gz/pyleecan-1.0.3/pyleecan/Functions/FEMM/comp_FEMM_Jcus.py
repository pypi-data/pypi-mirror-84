from numpy import linalg as LA, sign

from ...Functions.Winding.find_wind_phase_color import get_phase_id


def comp_FEMM_Jcus(lam, cname, I, j_t0, is_mmf):
    """Compute the current density for FEMM [A/mm2]"""

    Npcpp = lam.winding.Npcpp  # number of parallel circuits  per phase (maximum 2p)
    (Nrad, Ntan) = lam.winding.get_dim_wind()
    Nwpc = Nrad * Ntan  # total number of wires / strands in parallel per coil
    Ksfill = lam.comp_fill_factor()
    Swire = lam.winding.conductor.comp_surface_active()
    if I is not None:
        I = I.values
    # Decode the label
    q_id = int(cname[2:-1])
    if cname[-1] == "-":
        s = -1
    else:
        s = 1
    if I is None or LA.norm(I) == 0:
        Jcus = 0
    else:
        Jcus = s * 1e-6 * Ksfill * (I[q_id, j_t0] / Npcpp) * is_mmf / Swire / Nwpc
    return Jcus
