from pathlib import Path

import pandas as pd
import numpy as np

from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler


class GlobalPredictor:

    FEATURES_CLASSIFICATION = [
        "activity_score",
        "hourly_rate"
    ]

    FEATURES_CLUSTERING = [
        "performance_score",
        "activity_score",
        "hourly_rate"
    ]

    TARGET = "profile_type"

    def __init__(self, dataframe):

        self.df = dataframe.copy()

        self.scaler = StandardScaler()

        self.regression_model = None
        self.classification_model = None
        self.clustering_model = None

        self.cluster_labels = {}

        self._train_regression()
        self._train_classifier()
        self._train_clustering()

    # ==================================================
    # QUESTION 2
    # RÉGRESSION
    # ==================================================

    def _train_regression(self):

        X = self.df[["activity_score"]]

        y = self.df["performance_score"]

        self.regression_model = LinearRegression()

        self.regression_model.fit(X, y)

    def predict_performance(self, activity_score):

        prediction = self.regression_model.predict(
            [[activity_score]]
        )[0]

        prediction = float(round(prediction, 2))

        prediction = max(0, min(100, prediction))

        return prediction

    # ==================================================
    # QUESTION 4
    # CLASSIFICATION
    # ==================================================

    def _train_classifier(self):

        X = self.df[self.FEATURES_CLASSIFICATION]

        y = self.df[self.TARGET]

        self.classification_model = RandomForestClassifier(

            n_estimators=300,

            max_depth=8,

            random_state=42
        )

        self.classification_model.fit(X, y)

    def predict_profile(

        self,

        activity_score,

        hourly_rate
    ):

        data = pd.DataFrame([{

            "activity_score": activity_score,
            "hourly_rate": hourly_rate

        }])

        prediction = self.classification_model.predict(
            data
        )[0]

        probability = np.max(

            self.classification_model.predict_proba(data)

        )

        return prediction, round(float(probability), 4)

    # ==================================================
    # QUESTION 3
    # CLUSTERING
    # ==================================================

    def _train_clustering(self):

        X = self.df[self.FEATURES_CLUSTERING]

        X_scaled = self.scaler.fit_transform(X)

        self.clustering_model = KMeans(

            n_clusters=3,

            random_state=42,

            n_init=10
        )

        clusters = self.clustering_model.fit_predict(
            X_scaled
        )

        self.df["cluster"] = clusters

        stats = self.df.groupby("cluster")[
            "performance_score"
        ].mean()

        ordered = stats.sort_values().index.tolist()

        self.cluster_labels = {

            ordered[0]:
            "Freelances émergents",

            ordered[1]:
            "Profils intermédiaires",

            ordered[2]:
            "Experts Premium"
        }

    def predict_cluster(

        self,

        performance_score,

        activity_score,

        hourly_rate
    ):

        sample = pd.DataFrame([{

            "performance_score": performance_score,
            "activity_score": activity_score,
            "hourly_rate": hourly_rate

        }])

        sample_scaled = self.scaler.transform(sample)

        cluster = self.clustering_model.predict(
            sample_scaled
        )[0]

        return self.cluster_labels[cluster]

    # ==================================================
    # ANALYSE MÉTIER
    # ==================================================

    def generate_business_comment(

        self,

        profile,

        confidence,

        cluster,

        performance
    ):

        if profile == "Premium":

            level = "élevé"

        else:

            level = "modéré"

        return f"""
Ce freelance présente un potentiel commercial {level}.

La performance estimée est de {performance}/100.

Le système le rattache au groupe :
{cluster}.

Le modèle prédit un profil {profile}
avec une confiance de {confidence * 100:.1f} %.

Cette recommandation doit être utilisée
comme une aide à la décision et non
comme un remplacement du jugement humain.
"""

    # ==================================================
    # RAPPORT COMPLET
    # ==================================================

    def full_prediction(

        self,

        activity_score,

        hourly_rate
    ):

        performance = self.predict_performance(
            activity_score
        )

        profile, confidence = self.predict_profile(

            activity_score,

            hourly_rate
        )

        cluster = self.predict_cluster(

            performance,

            activity_score,

            hourly_rate
        )

        comment = self.generate_business_comment(

            profile,

            confidence,

            cluster,

            performance
        )

        return {

            "predicted_performance":
            performance,

            "predicted_profile":
            profile,

            "confidence":
            confidence,

            "cluster":
            cluster,

            "business_comment":
            comment
        }