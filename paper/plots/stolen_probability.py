import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.widgets import Slider
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits import mplot3d
from itertools import chain
from matplotlib import rcParams
# rcParams['text.usetex'] = True
# rcParams['text.latex.preamble'] = r'\usepackage{amsmath}'


# https://github.com/CSTR-Edinburgh/mlpractical/blob/mlp2018-9/master/mlp/layers.py
def softmax(inputs):
    exp_inputs = np.exp(inputs - inputs.max(-1)[:, None])
    return exp_inputs / exp_inputs.sum(-1)[:, None]


def get_perp_vecs(vecs):
    vv = vecs.copy()
    vv[:, 0] = 1. /  vv[:, 0]
    vv[:, 1] = - 1. / vv[:, 1]
    vv = np.vstack([vv, -vv])
    scores = vv.dot(vecs.T)
    TOL = -1e-10
    vv = vv[np.all(scores >= TOL, axis=1)]
    vv = vv / np.linalg.norm(vv, axis=1, keepdims=True)
    return vv


def fill_cone(cl, W, ax, color, label):
    C = len(W)
    vecs = []
    for i in range(C):
        if i != cl:
            vecs.append(W[cl, :] - W[i, :])
    vecs = np.vstack(vecs)
    vecs = get_perp_vecs(vecs) * 1
    vecs = np.vstack([vecs, np.array([[0, 0]])]) * 20.
    ww = W[cl, :]
    ww = ww / np.linalg.norm(ww)
    signs = vecs.dot(ww)
    # indices = np.argsort(signs)
    # vecs = vecs[indices]
    # signs = signs[indices]
    vecs = vecs[signs >= 0.]
    ax.fill(vecs[:, 0], vecs[:, 1],
            edgecolor=(*color, .9),
            facecolor=(*color, .2),
            linewidth=.4, linestyle='-')


def plot(W):

    colors = [cm.tab10(float(i) / 10) for i in range(len(W))]

    fill_cone(0, W, ax, color=colors[0][:3], label='a')
    fill_cone(1, W, ax, color=colors[1][:3], label='b')
    fill_cone(2, W, ax, color=colors[2][:3], label='c')

    convex_hull = W[:3]
    # Plot the convex hull
    # ax.fill(convex_hull[:, 0], convex_hull[:, 1],
    #         edgecolor=(.4, .4, .4, .8), facecolor=(.4, .4, .4, .2),
    #         linewidth=.6, linestyle='dotted', label='Convex Hull')
    # ax.legend(fontsize=16, loc='upper left')

    # for i, row in enumerate(W):
    #     ax.arrow(0., 0., *row, color=colors[i], head_width=0.2, head_length=0.35,
    #              linewidth=1, length_includes_head=True)
    # ax.scatter(*W.T, s=2, color=colors)
    ax.set_xlim([-X_LIM, X_LIM])
    ax.set_ylim([-X_LIM, X_LIM])
    ax.set_aspect('equal')
    ax.set_xlabel('Feature $x_1$', fontsize=24)
    ax.set_ylabel('Feature $x_2$', fontsize=24)

    label_pos = [[-1.5, -1], [.5, 2.], [1.75, -1], [0, 0]]

    for i in range(len(W)):

        color = colors[i]

        # ax.text(*(W[i,:] * .98), '$\mathbf{w}_{Class\ %s}$' % chr(97 + i), fontsize=18,
        #         va='top', ha='left', color=color)
        if i == 3:
            # ax.text(*label_pos[i], '$Class\ c_%d?$' % (i + 1), fontsize=22,
            #         va='center', ha='center', color=color)
            pass
        else:
            ax.text(*label_pos[i], '$Class\ c_%d$' % (i + 1), fontsize=24,
                    va='center', ha='center', color=color)

        # axes[i].set_title('P(Class %s)' % chr(97 + i), color=color, fontsize=18, pad=10, y=.96)
        axes[i].set_title('$P\\left(Class\ c_%d \mid \mathbf{x}\\right)$' % (i + 1), color=color, fontsize=18, pad=10, y=.96)
        axes[i].set_xlim([-X_LIM, X_LIM])
        axes[i].set_ylim([-X_LIM, X_LIM])
        axes[i].set_zlim([0., Y_LIM])
        axes[i].set_xlabel('$x_1$', labelpad=-14, fontsize=15)
        axes[i].set_ylabel('$x_2$', labelpad=-14, fontsize=15)
        # axes[i].set_zlabel('Probability')

        act = W.dot(xvec.T).T
        # zz = -np.log(softmax(act)[:, 3]).reshape(xx.shape)
        zz = (softmax(act)[:, i]).reshape(xx.shape)
        surf = axes[i].plot_wireframe(xx, yy, zz, linewidth=0.15, color=color)


def clear_plot():
    global ax, axes
    ax.cla()
    for axx in axes:
        axx.cla()


def update_m1(val):
    global W
    W[len(W) - 1, 0] = val
    clear_plot()
    plot(W)


def update_m2(val):
    global W
    W[len(W) - 1, 1] = val
    clear_plot()
    plot(W)


if __name__ == "__main__":

    X_LIM = 3.
    Y_LIM = 1

    NUM_POINTS = 100
    x = np.linspace(-X_LIM, X_LIM, NUM_POINTS)
    y = np.linspace(-X_LIM, X_LIM, NUM_POINTS)
    xx, yy = np.meshgrid(x, y)

    W = np.array([
        [-2., -2.],
        [1, 2],
        [1.8, -.8],
        [.9, .2],   # This is internal to the convex hull
    ])

    xvec = np.hstack([xx.reshape(-1, 1), yy.reshape(-1, 1)])

    act = W.dot(xvec.T).T
    # zz = -np.log(softmax(act)[:, 3]).reshape(xx.shape)
    zz = (softmax(act)[:, 3]).reshape(xx.shape)

    fig = plt.figure(figsize=(10, 5), dpi=220)
    ax = fig.add_subplot(1, 2, 1)

    ax.xaxis.set_ticklabels([])
    ax.yaxis.set_ticklabels([])

    axes = [fig.add_subplot(2, 4, 3, projection='3d'),
            fig.add_subplot(2, 4, 4, projection='3d'),
            fig.add_subplot(2, 4, 7, projection='3d'),
            fig.add_subplot(2, 4, 8, projection='3d')]

    for axx in axes:
        axx.xaxis.set_ticklabels([])
        axx.yaxis.set_ticklabels([])
        axx.zaxis.set_ticks([0., .5, 1.])


    plot(W)
    # plt.tight_layout()
    # plt.subplots_adjust(left=.038, bottom=0.043, right=0.86, top=0.982, wspace=.373, hspace=.241)
    plt.subplots_adjust(wspace=.02, hspace=.085, top=.97, bottom=.1, left=.04, right=.98)
    plt.show()
