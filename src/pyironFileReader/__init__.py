from ovito.data import DataCollection
from ovito.io import FileReaderInterface
import numpy as np
from typing import Callable, Any
from traits.api import Bool
import h5py


class PyironFileReader(FileReaderInterface):
    roundCell = Bool(False, label="Round cell to orthogonal")
    roundCellBy = 1e-8
    strict = Bool(False, label="Strict mode")

    particle_props_dict = {
        "output/generic/forces": "Force",
        "output/generic/velocities": "Velocity",
    }

    attributes_dict = {
        "output/generic/steps": "Timestep",
        "output/generic/natoms": "Number of atoms",
        "output/generic/temperature": "Temperature",
        "output/generic/energy_tot": "Total energy",
    }

    @staticmethod
    def detect(filename: str):
        try:
            with h5py.File(filename, "r") as f:
                for k in f.keys():
                    # Check if all jobs in the h5 container have status "finished" -> (encoded as ascii array)
                    if not np.all(
                        f[k]["status"][:] == [102, 105, 110, 105, 115, 104, 101, 100]
                    ):
                        break
                else:
                    return True
        except Exception:
            pass
        return False

    def scan(self, filename: str, register_frame: Callable[..., None]):
        with h5py.File(filename, "r") as f:
            for k in f.keys():
                for i in range(len(f[k]["output/generic/natoms"])):
                    register_frame(
                        parser_data=i,
                        label=f"{k}: {f[k]['output/generic/steps'][i]}",
                    )

    def parse(
        self, data: DataCollection, filename: str, parser_data: tuple, **kwargs: Any
    ):
        with h5py.File(filename, "r") as f:
            # Map from global frame index (parser_data) to local run in the h5 file
            keys = list(f.keys())
            if len(keys) > 1:
                total = [len(f[key]["output/generic/natoms"]) for key in keys]
                total = np.cumsum(total)
                keyIdx = np.argmin(total <= parser_data)
                key = keys[keyIdx]
                localIdx = parser_data - total[keyIdx - 1]
            else:
                key = keys[0]
                localIdx = parser_data

            # Create particles
            particles = data.create_particles(
                count=int(f[key]["output/generic/natoms"][localIdx])
            )
            # Particle type
            typeProperty = particles.create_property("Particle Type")
            typeList = eval(
                "".join([chr(item) for item in f[key]["output/structure/species"][:]])
            )
            uTypesH5 = np.unique(f[key]["output/generic/indices"][localIdx])
            uTypesOvito = np.zeros(uTypesH5[-1] + 1, dtype=int)
            for u in uTypesH5:
                uTypesOvito[u] = typeProperty.add_type_name(typeList[u], particles).id
            types = np.array(f[key]["output/generic/indices"][localIdx])
            for u in uTypesH5:
                typeProperty[types == u] = uTypesOvito[u]

            # Positions -> preference for unwrapped positions
            try:
                particles.create_property(
                    "Position",
                    data=f[key]["output/generic/unwrapped_positions"][localIdx],
                )
            except KeyError:
                particles.create_property(
                    "Position",
                    data=f[key]["output/generic/positions"][localIdx],
                )

            # Optional particle properties
            for h5Key, ovitoKey in self.particle_props_dict.items():
                try:
                    particles.create_property(
                        ovitoKey,
                        data=f[key][h5Key][localIdx],
                    )
                except KeyError:
                    if self.strict:
                        raise KeyError(
                            f"{key}/{h5Key} requested but not found in pyirion data container. Consider not running in strict mode."
                        )

            # Cell
            cellMatrix = np.zeros((3, 4))
            cellMatrix[:3, :3] = f[key]["output/generic/cells"][localIdx]
            if self.roundCell:
                for idx in ((0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)):
                    cellMatrix[idx] = (
                        0 if cellMatrix[idx] <= self.roundCellBy else cellMatrix[idx]
                    )
            data.create_cell(cellMatrix, pbc=f[key]["output/structure/cell/pbc"][:])

            # Attributes
            for h5Key, ovitoKey in self.attributes_dict.items():
                try:
                    data.attributes[ovitoKey] = f[key][h5Key][localIdx]
                except KeyError:
                    if self.strict:
                        raise KeyError(
                            f"{key}/{h5Key} requested but not found in pyirion data container. Consider not running in strict mode."
                        )
