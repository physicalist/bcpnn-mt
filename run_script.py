import sys
import time
import numpy as np
import os
t1 = time.time()

script_name = 'toy_experiment.py'

#tau_zis = [10, 100, 1000, 5000]
#tau_zis = [10, 100, 250, 500, 1000, 2000, 3000, 4000, 5000]
tau_zis = [10, 100, 250, 500, 1000, 1500, 2000, 3000, 4000, 5000]
tau_zjs = [10, 100, 1000]
tau_es = [10, 100, 1000]
tau_ps = [10000]
dxs = [.5]
#dxs = np.around(np.arange(.5, -.2, -.02), decimals=2)
dvs = [.0]
#dvs = np.around(np.arange(.0, .16, .02), decimals=2)
v_stims = np.around(np.arange(0.1, 2.00, 0.2), decimals=2)
#v_stims = [.5]
#v_stims = [0.1]
n_runs = len(tau_ps) * len(tau_es) * len(dxs) * len(v_stims) * len(tau_zis) * len(tau_zjs) * len(dvs)
it_cnt = 0 
x0, u0 = .5, .5
for tau_p in tau_ps:
    for tau_e in tau_es:
        for tau_zj in tau_zjs:
            for v_stim in v_stims:
                for tau_zi in tau_zis:
                    for dv in dvs:
                        for dx in dxs:
#                            output_folder = 'NewTwoCellSweep_tauzj%d_taue%d_taup%d_dv%.1e_dx%.1e/' % (tau_zj, tau_e, tau_p, dv, dx)
    #                            output_folder = 'TwoCellSweep_tauzj%d_taue%d_taup%d_dv%.1e_dx%.1e/' % (tau_zj, tau_e, tau_p, dv, dx)
#                            output_folder = 'TwoCellSweep_tauzj%d_taue%d_taup%d_vstim%.2f_prex%.2f_u%.2f/' % (tau_zj, tau_e, tau_p, v_stim, x0, u0)
                            output_folder = 'TwoCellTauZjSweep_tauzj%d_taue%d_taup%d_vstim%.2f_prex%.2f_u%.2f/' % (tau_zj, tau_e, tau_p, v_stim, x0, u0)
                            command = 'python %s %d %f %f %f %d %d %d %f %f %s' % (script_name, tau_zi, v_stim, dx, dv, tau_zj, tau_e, tau_p, x0, u0, output_folder)
                            print '\n-------------------\n\tIteration: %d / %d\tdv = %.1f\n----------------------\n' % (it_cnt, n_runs, dv)
                            print command
                            os.system(command)
                            it_cnt += 1

t2 = time.time() - t1
print "Sweep with %d runs took %.2f seconds or %.2f minutes" % (n_runs, t2, t2/60.)
