import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

def main(num, dim):

    data = pd.read_pickle(r'./country_data.pkl').sort_values(by="Happiness", ascending=False)

    features = ['GDP', 'Growth', 'Social', 'Life', 'Crime', 'Political']
    target = ["Happiness"]

    x = data.loc[:, features].values
    y = data.loc[:, target].values
    axes = StandardScaler().fit_transform(x).transpose()

    NUM = num

    COV = np.cov(axes)
    eigenvalues, eigenvectors = np.linalg.eig(COV)
    print(np.sum(eigenvalues[:NUM]) / np.sum(eigenvalues) * 100)

    pca = PCA(n_components=NUM)
    principalComponents = pca.fit_transform(axes)

    principalDf = pd.DataFrame(data = principalComponents, columns = ['principal component ' + str(i) for i in range(1, NUM + 1)])

    cm = plt.get_cmap("seismic") # Color Map
    col = [cm(float(i)/(len(axes[0]))) for i in range(len(axes[0]))]

    fig = plt.figure()
    ax = fig.add_subplot(111)

    x_plot = np.dot(np.array(principalDf['principal component 1'].transpose()), axes).flatten()
    y_plot = np.dot(np.array(principalDf['principal component 2'].transpose()), axes).flatten()
    z_plot = np.dot(np.array(principalDf['principal component 3'].transpose()), axes).flatten()

    if dim == 3:
        fig = plt.figure()
        ax3D = fig.add_subplot(111, projection='3d')
        ax3D.scatter(x_plot, y_plot, z_plot, s=10, c=col, marker='o')

    elif dim == 2:
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.scatter(x_plot, y_plot, c=col, marker='o')
    plt.grid()
    plt.show()


if __name__ == "__main__":
    main(3, 3)

