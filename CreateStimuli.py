import numpy as np
import random
import pylab
from matplotlib import animation


class CreateStimuli(object):
    def __init__():
        pass

    def create_motion_sequence_2D(params, random_order):
        """Creates the motion parameters (x, y, u, v) for a sequence of 2-dim stimuli

        Keyword arguments:
        random_order -- (bool) if True the sequence is shuffled
        """

        n_theta = params['n_theta']
        n_speeds = params['n_speeds']
        n_cycles = params['n_cycles']
        self.n_stim_per_direction = params['n_stim_per_direction']
        self.n_stim_total = n_speeds * n_theta * n_cycles * self.n_stim_per_direction
        random.seed(0)
        # arrays to be filled by the stimulus creation loops below
        self.all_speeds = np.zeros(self.n_stim_total)
        self.all_thetas = np.zeros(self.n_stim_total)
        self.all_starting_pos = np.zeros((self.n_stim_total, 2))

        # create stimulus ranges
        if params['log_scale']==1:
            speeds = np.linspace(params['v_min_training'], params['v_max_training'], num=params['N_V'], endpoint=True)
        else:
            speeds = np.logspace(np.log(params['v_min_training'])/np.log(params['log_scale']),
                            np.log(params['v_max_training'])/np.log(params['log_scale']), num=params['N_V'],
                            endpoint=True, base=params['log_scale'])
        thetas = np.linspace(0, 2 * np.pi, n_theta, endpoint=False)

        stim_cnt = 0
        for speed in xrange(n_speeds):
            v = speeds[speed]
            for cycle in xrange(n_cycles):
                # if random_order: for direction in random.shuffle(range(n_theta)):
                for direction in xrange(n_theta):
                    theta = thetas[direction]
                    print '\ntheta', theta, theta / (np.pi)

                    # decide where dot starts moving from
                    # 1
                    if theta == 0: # start on the left border (0, y)
                        y_0 = np.linspace(0, 1, self.n_stim_per_direction + 2)[1:-1]
                        x_0 = np.zeros(self.n_stim_per_direction)
                    elif theta == np.pi: # start on the right border (1., y)
                        y_0 = np.linspace(0, 1, self.n_stim_per_direction + 2)[1:-1]
                        x_0 = np.ones(self.n_stim_per_direction)

                    elif theta == .5 * np.pi: # start on the upper border (x, 0)
                        x_0 = np.linspace(0, 1, self.n_stim_per_direction + 2)[1:-1]
                        y_0 = np.ones(self.n_stim_per_direction)

                    elif theta == 1.5 * np.pi: # start on the lower border (x, 1)
                        x_0 = np.linspace(0, 1, self.n_stim_per_direction + 2)[1:-1]
                        y_0 = np.zeros(self.n_stim_per_direction)

                    elif theta < .5 * np.pi: # moving to lower right, start on the left or upper border
                        x_min, x_max = 0.0, .75 # improvement?: inrtoduce dependence of theta here
                        y_min, y_max = 0.25, 1.
                        up_or_left = np.array([i / int((self.n_stim_per_direction) /2) for i in range(self.n_stim_per_direction)])
                        upper_idx = up_or_left.nonzero()[0]
                        upper_x = np.linspace(x_min, x_max, upper_idx.size + 2)[1:-1]
                        x_0 = np.zeros(self.n_stim_per_direction)
                        y_0 = np.ones(self.n_stim_per_direction)
                        x_0[upper_idx] = upper_x
                        left_idx = up_or_left == 0
                        y_0[left_idx] = np.linspace(y_min, y_max, left_idx.nonzero()[0].size)

                    elif theta > .5 * np.pi and theta < np.pi: # moving to lower left, start on the right or upper border
                        x_min, x_max = 0, 1.
                        y_min, y_max = 0.5, 1.
                        upper_or_right = np.array([i / int((self.n_stim_per_direction) /2) for i in range(self.n_stim_per_direction)])
                        x_0 = np.ones(self.n_stim_per_direction)
                        upper_idx = upper_or_right.nonzero()[0]
                        right_idx = upper_or_right == 0
                        upper_x = np.linspace(x_min, x_max, upper_idx.size + 2)[1:-1]
                        x_0[upper_idx] = upper_x
                        y_0 = np.ones(self.n_stim_per_direction)
                        y_0[right_idx] = np.linspace(y_min, y_max, right_idx.nonzero()[0].size)

                    elif theta > np.pi and theta < 1.5 * np.pi: # moving to upper left, start on the right or bottom border
                        x_min, x_max = 0.25, 1.
                        y_min, y_max = 0.0, 0.5
                        bottom_or_right = np.array([i / int((self.n_stim_per_direction) /2) for i in range(self.n_stim_per_direction)])
                        x_0 = np.ones(self.n_stim_per_direction)
                        bottom_idx = bottom_or_right.nonzero()[0]
                        bottom_x = np.linspace(x_min, x_max, bottom_idx.size + 2)[1:-1]
                        x_0[bottom_idx] = bottom_x
                        y_0 = np.zeros(self.n_stim_per_direction)
                        right_idx = bottom_or_right == 0
                        y_0[right_idx] = np.linspace(y_min, y_max, right_idx.nonzero()[0].size)

                    elif theta > 1.5 * np.pi: # moving to upper right, starting at left or bottom border
                        x_min, x_max = 0., 0.75
                        y_min, y_max = 0., 0.75
                        bottom_or_left = np.array([i / int((self.n_stim_per_direction) /2) for i in range(self.n_stim_per_direction)])
                        x_0 = np.zeros(self.n_stim_per_direction)
                        bottom_idx = bottom_or_left.nonzero()[0]
                        bottom_x = np.linspace(x_min, x_max, bottom_idx.size + 2)[1:-1]
                        x_0[bottom_idx] = bottom_x
                        y_0 = np.zeros(self.n_stim_per_direction)
                        left_idx = bottom_or_left == 0
                        y_0[left_idx] = np.linspace(y_min, y_max, left_idx.nonzero()[0].size)

                    stim_order_for_one_direction = range(self.n_stim_per_direction)
                    if random_order:
                        random.shuffle(stim_order_for_one_direction)

                    for i in stim_order_for_one_direction:
        #            for i in xrange(self.n_stim_per_direction):
                        self.all_starting_pos[stim_cnt, :] = x_0[i], y_0[i]
                        self.all_speeds[stim_cnt] = v
                        rnd_rotation = params['sigma_theta_training'] * (np.random.rand() - .5)
                        self.all_thetas[stim_cnt] = theta + rnd_rotation
                        stim_cnt += 1

    def get_motion_params(self, random_order=False):

        stim_order = range(self.n_stim_total)
        if random_order:
            random.shuffle(stim_order)
        return self.all_speeds[stim_order], self.all_starting_pos[stim_order, :], self.all_thetas[stim_order]


if __name__ == '__main__':
    import simulation_parameters
    PS = simulation_parameters.parameter_storage()
    params = PS.load_params()                       # params stores cell numbers, etc as a dictionary

    random_order = False
    CS = CreateStimuli()
    CS.create_motion_sequence_2D(params, random_order)

    fig = pylab.figure()
    ax = fig.add_subplot(111)
    ax.set_xlim((-0.2, 1.2))
    ax.set_ylim((-0.2, 1.2))
    color_list = ['k', 'b', 'g', 'r', 'y', 'c', 'm', '#00f80f', '#deff00', '#ff00e4', '#00ffe6']

    #init_rect
    ax.plot([0, 1], [0, 0], 'k--', lw=3)
    ax.plot([1, 1], [0, 1], 'k--', lw=3)
    ax.plot([1, 0], [1, 1], 'k--', lw=3)
    ax.plot([0, 0], [1, 0], 'k--', lw=3)

    all_speeds, all_starting_pos, all_thetas = CS.get_motion_params(random_order)
    stim_start = CS.n_stim_per_direction * 8
    stim_stop = CS.n_stim_per_direction * (9 + 1)
    for stim_id in xrange(stim_start, stim_stop):
        theta = all_thetas[stim_id]
        v = 5 * all_speeds[stim_id]
        vx, vy = v * np.cos(theta), - v * np.sin(theta)
        x0, y0 = all_starting_pos[stim_id, :]
        print 'debug stim_id %d' % stim_id, x0, y0
        x_pos = x0 + vx
        y_pos = y0 + vy
        color_idx = stim_id / CS.n_stim_per_direction
        ax.plot([x0, x_pos], [y0, y_pos], color=color_list[color_idx], lw=2)

    pylab.show()
