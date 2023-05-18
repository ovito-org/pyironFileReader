from pyiron_atomistics import Project

pr = Project("example_01")
structure = pr.create.structure.ase.bulk("Al", cubic=True)
structure.set_repeat([9, 9, 9])
job = pr.create.job.Lammps("lmp")
job.structure = structure
job.calc_md(n_ionic_steps=1000, n_print=10, temperature=500.0)
job.run()
