from sklearn.cluster import KMeans
from filetools import list_ext_files, copy_file
from pxreader import PXReader


class Clusters:
    def __init__(self, paths: list[str], filenames: list[str], n_clusters: int):
        self.paths = paths
        self.filenames = filenames
        self.n_clusters = n_clusters

        self.readers = [PXReader(path, filename) for path, filename in zip(paths, filenames)]
        # Unused: r.date_mjd, r.gl, r.gb, r.max_dm, r.dm_diff_from_max, r.distance, r.flux_amp, r.flux_mu, r.flux_sigma
        self.features = [[r.snr, r.width, r.dm]
                         for r in self.readers]

        self.kmeans = KMeans(n_clusters=n_clusters).fit(self.features)
        self.labels = self.kmeans.labels_

    def create_cluster_folder(self):
        for i, (reader, label) in enumerate(zip(self.readers, self.labels)):
            copy_file(reader.path, f"clusters/{label}", reader.filename)
            copy_file(reader.png_path, f"clusters/{label}", reader.png_filename)

    def print_cluster_info(self):
        for i, (reader, label) in enumerate(zip(self.readers, self.labels)):
            print(f"PX: {reader.get_info_str()}")
            print(f"Label: {label}")
            print("")


def main():
    paths, filenames = list_ext_files('.px', directory='files')

    clusters = Clusters(paths, filenames, n_clusters=3)
    clusters.print_cluster_info()
    clusters.create_cluster_folder()


if __name__ == '__main__':
    main()
