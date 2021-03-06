#!/usr/bin/env python2
"""
@author: Christian Forster
"""

import os
import yaml
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import rc
import matplotlib.lines as mlines
rc('font', **{'family': 'serif', 'serif': ['Cardo']})
rc('text', usetex=True)

FORMAT = '.pdf'


def color_box(bp, color):
    elements = ['medians', 'boxes', 'caps', 'whiskers']
    # Iterate over each of the elements changing the color
    for elem in elements:
        [plt.setp(bp[elem][idx], color=color, linestyle='-', lw=1.0)
         for idx in range(len(bp[elem]))]
    return


def boxplot_compare(ax, xlabels,
                    data, data_labels, data_colors,
                    legend=True):
    n_data = len(data)
    n_xlabel = len(xlabels)
    leg_handles = []
    leg_labels = []
    idx = 0
    for idx, d in enumerate(data):
        # print("idx and d: {0} and {1}".format(idx, d))
        w = 1 / (1.5 * n_data + 1.5)
        widths = [w for pos in np.arange(n_xlabel)]
        positions = [pos - 0.5 + 1.5 * w + idx * w
                     for pos in np.arange(n_xlabel)]
        # print("Positions: {0}".format(positions))
        bp = ax.boxplot(d, 0, '', positions=positions, widths=widths)
        color_box(bp, data_colors[idx])
        tmp, = plt.plot([1, 1], c=data_colors[idx], alpha=0)
        leg_handles.append(mlines.Line2D([], [], color=data_colors[idx]))  # manually add color to handle
        leg_labels.append(data_labels[idx])
        idx += 1

    ax.set_xticks(np.arange(n_xlabel))
    ax.set_xticklabels(xlabels)
    xlims = ax.get_xlim()
    ax.set_xlim([xlims[0]-0.1, xlims[1]-0.1])
    if legend:
        # ax.legend(leg_handles, leg_labels, bbox_to_anchor=(
            # 1.05, 1), loc=2, borderaxespad=0.)
        ax.legend(leg_handles, leg_labels)
    map(lambda x: x.set_visible(False), leg_handles)


def plot_trajectory_top(ax, pos, color, name, alpha=1.0):
    ax.grid(ls='--', color='0.7')
    # pos_0 = pos - pos[0, :]
    ax.plot(pos[:, 0], pos[:, 1], color, linestyle='-', alpha=alpha, label=name)


def plot_trajectory_side(ax, pos, color, name, alpha=1.0):
    ax.grid(ls='--', color='0.7')
    # pos_0 = pos - pos[0, :]
    ax.plot(pos[:, 0], pos[:, 2], color, linestyle='-', alpha=alpha, label=name)


def plot_trajectory_height(ax, pos, color, name, alpha=1.0):
    ax.grid(ls='--', color='0.7')

    xy_dists = [0]
    xy_dist_so_far = 0
    for i in range(len(pos)-1):
        xy_dist_so_far += np.linalg.norm([pos[i+1][:2]-pos[i][:2]])
        xy_dists.append(xy_dist_so_far)
    ax.plot(xy_dists, pos[:, 2], color+'-', alpha=alpha, label=name)


def plot_aligned_top(ax, p_gt, p_es, n_align_frames):
    if n_align_frames <= 0:
        n_align_frames = p_es.shape[0]
    # p_es_0 = p_es - p_gt[0, :]
    # p_gt_0 = p_gt - p_gt[0, :]
    # ax.plot(p_es[0:n_align_frames, 0], p_es[0:n_align_frames, 1],
        # 'g-', linewidth=2, label='aligned')
    for (x1, y1, z1), (x2, y2, z2) in zip(
            p_es[:n_align_frames:10, :], p_gt[:n_align_frames:10, :]):
        ax.plot([x1, x2], [y1, y2], '-', color="gray")


def plot_error_n_dim(ax, distances, errors, results_dir,
                     colors=['r', 'g', 'b'],
                     labels=['x', 'y', 'z']):
    assert len(colors) == len(labels)
    assert len(colors) == errors.shape[1]
    for i in range(len(colors)):
        ax.plot(distances, errors[:, i],
                colors[i]+'-', label=labels[i])

def plot_time_and_z(ax, plot_traj, labels, colors):
    start_time_es = plot_traj.t_es[0]
    start_time_gt = plot_traj.t_gt[0]
    ax.plot((plot_traj.t_es-start_time_es), plot_traj.p_es[:,2], color=colors[0])
    ax.plot((plot_traj.t_gt-start_time_gt), plot_traj.p_gt[:,2], color=colors[1])
    leg_labels = []
    leg_handles = []
    # manually add color to handle
    leg_handles.append(mlines.Line2D([], [], color=colors[0]))  
    leg_handles.append(mlines.Line2D([], [], color=colors[1]))  
    leg_labels.append(labels[0])
    leg_labels.append(labels[1])
    ax.legend(leg_handles, leg_labels)
    map(lambda x: x.set_visible(False), leg_handles)

