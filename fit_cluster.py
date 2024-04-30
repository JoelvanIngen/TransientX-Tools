from sklearn.cluster import KMeans
from filetools import list_ext_files
from pxreader import PXReader


def main():
    readers = [PXReader(f) for f in list_ext_files('.px', directory='files')]

    features = [[r.snr, r.width, r.dm, r.max_dm, r.dm_diff_from_max, r.date_mjd, r.gl, r.gb, r.distance, r.flux_amp, r.flux_mu, r.flux_sigma]
                for r in readers]

    kmeans = KMeans(n_clusters=3).fit(features)

    for i, reader in enumerate(readers):
        print(f"PX: {reader.get_info_str()}")
        print(f"Label: {kmeans.labels_[i]}")
        print("")


if __name__ == '__main__':
    main()
