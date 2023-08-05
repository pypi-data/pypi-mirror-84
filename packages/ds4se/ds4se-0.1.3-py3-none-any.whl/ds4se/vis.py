# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/5.0_vis.ipynb (unless otherwise specified).

__all__ = ['get_contours', 'visualize_gt_ngt', 'visualize_events', 'plot_counts', 'vis_3d', 'reduce_dims',
           'clusterize_w_entropy']

# Cell
# Imports
import matplotlib.pyplot as plt
import numpy as np

from .desc.stats import *
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

# Cell
def get_contours(x_range, y_range, delta):
    x = np.arange(x_range[0], x_range[1], delta)
    y = np.arange(x_range[0], x_range[1], delta)
    X, Y = np.meshgrid(x, y)
    Z = X + Y

    return X, Y, Z

# Cell
def visualize_gt_ngt(gt, ngt, title, y_label):
    plt.title(title)
    plt.xlim(2, 15)
    plt.xlabel('req entropy')

    plt.ylim(2, 15)
    plt.ylabel(f'{y_label} entropy')
    plt.gca().set_aspect('equal', adjustable='box')

#     xi = np.linspace(2, 10, 10)
#     yi = np.linspace(2, 10, 10)
#     zi = griddata((gt[0], gt[1]), gt[1], (xi[None,:], yi[:,None]), method='linear')
    X, Y, Z = get_contours([1, 16], [1, 16], 1)
    plt.contourf(X, Y, Z, levels = 20, cmap = 'gray')

#     plt.tricontour(gt[0], gt[1])
    plt.scatter(ngt[0], ngt[1], c='r', label='non-groundtruth', alpha = 0.5)
    plt.scatter(gt[0], gt[1], c='b', label='groundtruth', alpha = 0.5)

    plt.legend()
    plt.show()

# Cell
def visualize_events(events, color, title, label):
    plt.title(title)
    maxi, mini, μ, med, σ, med_σ = get_desc_stats(events)
    text = f'Max: {maxi:.3f}\nMin: {mini:.3f}\nMean: {μ:.3f}\nMed: {med:.3f}\nStDev: {σ:.3f}\nMAD: {med_σ:.3f}'
    plt.gcf().text(0.02, 0.35, text, fontsize=14)
    plt.hlines(1,0,1)
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    plt.eventplot(events, orientation='horizontal', colors=color, alpha = 0.5, label=label)
    plt.subplots_adjust(left=0.25)
    plt.legend()
    plt.show()

# Cell
def plot_counts(counts, x_label, y_label, top_k = 30):
    labels, values = zip(*counts.most_common()[:top_k])

    indexes = np.arange(len(labels))
    width = 0.5
    plt.figure(num=None, figsize=(22, 4), dpi=60, facecolor='w', edgecolor='k')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.bar(indexes, values, width, align = 'center')
    plt.xticks(indexes, labels)
    plt.show()

# Cell
def vis_3d(gt, ngt, src_dtype, trgt_dtype):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    plt.xlim(1, 15)
    plt.ylim(1, 15)
    ax.scatter(gt[0], gt[1], gt[2], c='b', marker='o')
    ax.scatter(ngt[0], ngt[1], ngt[2], c='r', marker='^')

    ax.set_xlabel(src_dtype)
    ax.set_ylabel(trgt_dtype)
    ax.set_zlabel('Word Mover Distance')

    ax.invert_yaxis()
    ax.set_zlim(0, 1)

    plt.show()

# Cell
# Uses PCA first and then t-SNE
def reduce_dims(doc_vecs, dims = 2):
    # hyperparameters from https://towardsdatascience.com/visualising-high-dimensional-datasets-using-pca-and-t-sne-in-python-8ef87e7915b

    pca = PCA(n_components=30)
    pca_features = pca.fit_transform(doc_vecs)

    tsne = TSNE(n_components=dims, verbose=1, perplexity=40, n_iter=300)
    tsne_features = tsne.fit_transform(doc_vecs)

    return tsne_features

# Cell
def clusterize_w_entropy(gt_doc_vecs, ngt_doc_vecs, gt_entropies, ngt_entropies):
    gt_reduced_vecs = reduce_dims(gt_doc_vecs)
    ngt_reduced_vecs = reduce_dims(ngt_doc_vecs)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(gt_reduced_vecs[:, 0], gt_reduced_vecs[:, 1], gt_entropies, c='b', marker='o')
    ax.scatter(ngt_reduced_vecs[:, 0], ngt_reduced_vecs[:, 1], ngt_entropies, c='r', marker='^')

#     ax.set_xlabel(src_dtype)
#     ax.set_ylabel(trgt_dtype)
    ax.set_zlabel('Entropy')

    ax.invert_yaxis()

    plt.show()