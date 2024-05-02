from sklearn.cluster import KMeans
from filetools import list_ext_files, copy_file
from pxreader import PXReader


def main():
    paths, filenames = list_ext_files('.px', directory='files')

    readers = [PXReader(path, filename) for path, filename in zip(paths, filenames)]

    # Unused: r.date_mjd, r.gl, r.gb, r.max_dm, r.dm_diff_from_max, r.distance, r.flux_amp, r.flux_mu, r.flux_sigma
    features = [[r.snr, r.width, r.dm]
                for r in readers]

    kmeans = KMeans(n_clusters=3).fit(features)

    for i, reader in enumerate(readers):
        label = kmeans.labels_[i]
        print(f"PX: {reader.get_info_str()}")
        print(f"Label: {label}")
        print("")

        copy_file(reader.path, f"clusters/{label}", reader.filename)
        copy_file(reader.png_path, f"clusters/{label}", reader.png_filename)


if __name__ == '__main__':
    main()
