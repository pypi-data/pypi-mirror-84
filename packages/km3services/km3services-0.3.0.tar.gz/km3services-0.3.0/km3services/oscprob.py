import json
import requests
import numpy as np
import random

from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


from km3services._tools import NumpyEncoder, _zipequalize


def oscillationprobabilities(
    flavour_in, flavour_out, energies, cos_zeniths, params=None
):
    """
    Calculate the neutrino oscillation properties.

    Parameters
    ----------
    flavour_in: float or array(float)
      PDG ID of the initial neutrino.
    flavour_out: float or array(float)
      PDG ID of the output neutrino.
    energies: float or array(float)
      The neutrino energies in GeV
    cos_zenith: float [-1; 0] or array(float)
      The cosine of the zenith (-1 is upgoing)
    params: dict(str: float)
      Oscillation parameters (dm_21, dm_31, theta_12, theta_13, dcp)

    Returns
    -------
    array(float)

    """
    if params is None:
        params = {
            "dm_21": 7.40e-5,
            "dm_31": 2.494e-3,
            "theta_12": 5.868e-1,
            "theta_23": 8.238e-1,
            "theta_13": 1.491e-1,
            "dcp": 4.084070449666731,
        }

    data = {
        "params": params,
        "nus": {
            "flavour_in": np.atleast_1d(flavour_in),
            "flavour_out": np.atleast_1d(flavour_out),
            "energies": np.atleast_1d(energies),
            "cos_zeniths": np.atleast_1d(cos_zeniths),
        },
    }
    r = requests.post(
        "http://131.188.167.67:30000/probabilities",
        data=json.dumps(data, cls=NumpyEncoder),
    )
    if r.ok:
        return np.array(json.loads(r.text))
    else:
        if r.status_code == 460:  # TODO: standardise this magic number
            raise ValueError(json.loads(r.text)["detail"])
        print(f"Error: {r.reason}")
        print(r.text)


# Server part

app = FastAPI()


class OscillationParameters(BaseModel):
    dm_21: float
    dm_31: float
    theta_12: float
    theta_23: float
    theta_13: float
    dcp: float


class _NumpyArray(BaseModel):
    dtype: str
    data: str


def tonumpy(arr: _NumpyArray):
    return np.frombuffer(arr.data)


class _Neutrinos(BaseModel):
    flavour_in: List[int]
    flavour_out: List[int]
    energies: List[float]
    cos_zeniths: List[float]


# @app.post("/numpy")
# async def _numpy(array: _NumpyArray):
#     return tonumpy(array)


@app.post("/probabilities")
async def _probability(params: OscillationParameters, nus: _Neutrinos):
    import ROOT

    ROOT.gSystem.Load("libOscProb.so")
    pmns = ROOT.OscProb.PMNS_Fast()
    prem = ROOT.OscProb.PremModel()

    pmns.SetDm(2, params.dm_21)  # set delta_m21 in eV^2
    pmns.SetDm(3, params.dm_31)  # set delta_m31 in eV^2
    pmns.SetAngle(1, 2, params.theta_12)  # set Theta12 in radians
    pmns.SetAngle(1, 3, params.theta_13)  # set Theta13 in radians
    pmns.SetAngle(2, 3, params.theta_23)  # set Theta23 in radians
    pmns.SetDelta(1, 3, params.dcp)  # set Delta13 in radians

    try:
        p = _osc_prob(
            pmns,
            prem,
            nus.flavour_in,
            nus.flavour_out,
            nus.energies,
            nus.cos_zeniths,
        )
    except ValueError as e:
        raise HTTPException(status_code=460, detail=str(e))

    return p


def _osc_prob(pmns, prem, flav_in, flav_out, energies, cos_zenith):
    params = _zipequalize(flav_in, flav_out, energies, cos_zenith)

    # use a PremModel to make the paths through the earth
    # with the class PremModel
    # chose an angle for the neutrino and fill the paths with cosTheta,
    # e.g. cosTheta = -1 (vertical up-going)
    P = []
    for fl_in, fl_out, E, cosZ in zip(*params):
        if fl_in < 0:
            pmns.SetIsNuBar(True)
        else:
            pmns.SetIsNuBar(False)
        prem.FillPath(cosZ)
        pmns.SetPath(prem.GetNuPath())
        P.append(pmns.Prob(_pdgid2flavor(fl_in), _pdgid2flavor(fl_out), E))
    return P


def _pdgid2flavor(pdgid):
    """Converts PDG ID to OscProb flavor"""
    if abs(pdgid) == 12:
        return 0
    if abs(pdgid) == 14:
        return 1
    if abs(pdgid) == 16:
        return 2
    raise ValueError("Unsupported PDG ID, please use neutrinos")
