# Copyright 2021 The NetKet Authors - All rights reserved.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import netket as nk

# 1D Lattice
L = 20  # 10

g = nk.graph.Hypercube(length=L, n_dim=1, pbc=True)

# Hilbert space of spins on the graph
hi = nk.hilbert.Spin(s=1 / 2, N=g.n_nodes)

# Ising spin hamiltonian
ha = nk.operator.Ising(hilbert=hi, graph=g, h=1.0)

# RBM Spin Machine
ma = nk.models.RBM(alpha=1, use_visible_bias=True, dtype=float)

# Metropolis Local Sampling
sa = nk.sampler.MetropolisHamiltonian(hi, ha, n_chains=16)

# Variational state
vs = nk.variational.MCState(sa, ma, n_samples=1000, n_discard=100)

# Optimizer
sr = nk.optimizer.SR(diag_shift=0.0001)

#
solver = nk.dynamics.Euler(dt=0.01)

te = nk.TimeEvolution(ha, variational_state=vs, sr=sr, solver=solver)

Sx = sum([nk.operator.spin.sigmax(hi, i) for i in range(L)])

log = nk.logging.JsonLog("test")

out = te.run(1.0, out=log, show_progress=False, obs={"SX": Sx}, step_size=0.1)[0]

# Variational monte carlo driver
# gs = nk.VMC(ha, op, sa, ma, n_samples=1000, n_discard=50)

# Run the optimization for 300 iterations
# gs.run(n_iter=300, out="test")
