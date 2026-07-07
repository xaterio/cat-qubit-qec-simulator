import numpy as np
import matplotlib.pyplot as plt
from qutip import wigner
import os
from .cat_state import CatState


def plot_wigner_function(state, x_range=(-5, 5), y_range=(-5, 5), 
                        resolution=100, save_path=None, title=None):
    xvec = np.linspace(x_range[0], x_range[1], resolution)
    yvec = np.linspace(y_range[0], y_range[1], resolution)
    
    W = wigner(state, xvec, yvec)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    contour = ax.contourf(xvec, yvec, W, 100, cmap='RdBu_r', 
                         vmin=-0.3, vmax=0.3)
    ax.contour(xvec, yvec, W, 10, cmap='RdBu_r', 
               vmin=-0.3, vmax=0.3, linewidths=0.5)
    
    ax.set_xlabel('Re($\\alpha$)')
    ax.set_ylabel('Im($\\alpha$)')
    
    if title:
        ax.set_title(title)
    else:
        ax.set_title('Wigner Function')
    
    plt.colorbar(contour, ax=ax, label='W(x, p)')
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.show()
    
    return W


def plot_cat_state_comparison(cat_state, alpha_values, n_cavity=30, 
                              save_dir='../results'):
    for alpha in alpha_values:
        cat = CatState(n_cavity, alpha)
        even_cat = cat.even_cat_state()
        odd_cat = cat.odd_cat_state()
        
        save_path_even = f'{save_dir}/wigner_even_alpha_{alpha:.1f}.png'
        save_path_odd = f'{save_dir}/wigner_odd_alpha_{alpha:.1f}.png'
        
        plot_wigner_function(even_cat, 
                            title=f'Even Cat State ($\\alpha$={alpha:.1f})',
                            save_path=save_path_even)
        
        plot_wigner_function(odd_cat, 
                            title=f'Odd Cat State ($\\alpha$={alpha:.1f})',
                            save_path=save_path_odd)


def plot_wigner_3d(state, x_range=(-5, 5), y_range=(-5, 5), 
                   resolution=50, save_path=None):
    from mpl_toolkits.mplot3d import Axes3D
    
    xvec = np.linspace(x_range[0], x_range[1], resolution)
    yvec = np.linspace(y_range[0], y_range[1], resolution)
    
    W = wigner(state, xvec, yvec)
    
    X, Y = np.meshgrid(xvec, yvec)
    
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    surf = ax.plot_surface(X, Y, W, cmap='RdBu_r', 
                          vmin=-0.3, vmax=0.3, alpha=0.8)
    
    ax.set_xlabel('Re($\\alpha$)')
    ax.set_ylabel('Im($\\alpha$)')
    ax.set_zlabel('W(x, p)')
    ax.set_title('3D Wigner Function')
    
    plt.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.show()
    
    return W
