# src/clustering/freelancer_clustering.py

import numpy as np
import pandas as pd

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA


class FreelancerClustering:

    def __init__(self, df):
        self.df = df.copy()

        self.features = [
            "performance_score",
            "activity_score",
            "hourly_rate"
        ]

        self.scaler = StandardScaler()
        self.model = None
        self.pca = PCA(n_components=2)

    # -------------------------
    # PREPROCESSING
    # -------------------------
    def prepare_data(self):

        X = self.df[self.features]

        X_scaled = self.scaler.fit_transform(X)

        return X_scaled

    # -------------------------
    # ELBOW METHOD
    # -------------------------
    def compute_elbow(self, max_k=10):

        X = self.prepare_data()

        inertias = []

        for k in range(2, max_k + 1):

            model = KMeans(n_clusters=k, random_state=42, n_init=10)
            model.fit(X)

            inertias.append(model.inertia_)

        return inertias

    # -------------------------
    # SILHOUETTE SCORE
    # -------------------------
    def best_k_silhouette(self, max_k=10):

        X = self.prepare_data()

        scores = {}

        for k in range(2, max_k + 1):

            model = KMeans(n_clusters=k, random_state=42, n_init=10)
            labels = model.fit_predict(X)

            score = silhouette_score(X, labels)
            scores[k] = score

        best_k = max(scores, key=scores.get)

        return best_k, scores

    # -------------------------
    # FIT FINAL MODEL
    # -------------------------
    def fit(self, k=3):

        X = self.prepare_data()

        self.model = KMeans(n_clusters=k, random_state=42, n_init=10)

        self.df["cluster"] = self.model.fit_predict(X)

        return self.df

    # -------------------------
    # PCA VISUALISATION
    # -------------------------
    def reduce_pca(self):

        X = self.prepare_data()

        X_pca = self.pca.fit_transform(X)

        self.df["pca_x"] = X_pca[:, 0]
        self.df["pca_y"] = X_pca[:, 1]

        return self.df

    # -------------------------
    # CLUSTER PROFILING
    # -------------------------
    def profile_clusters(self):

        return self.df.groupby("cluster")[self.features].mean()

    # -------------------------
    # INTERPRETATION BUSINESS
    # -------------------------
    def interpret_clusters(self):

        profiles = self.profile_clusters()

        interpretation = []

        for cluster_id, row in profiles.iterrows():

            interpretation.append(
                f"""
Cluster {cluster_id} :
- Performance moyenne : {row['performance_score']:.2f}
- Activité moyenne : {row['activity_score']:.2f}
- Tarif moyen : {row['hourly_rate']:.2f}
"""
            )

        return "\n".join(interpretation)