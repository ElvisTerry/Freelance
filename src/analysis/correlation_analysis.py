# src/analysis/correlation_analysis.py

"""
INF232 - THÈME B

Question 2 :
Étude de la relation entre :

- performance_score
- activity_score
- hourly_rate

avec :
- corrélation de Pearson
- test de significativité
- régression linéaire
- métriques de prédiction
"""

import numpy as np

from scipy.stats import pearsonr

from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)
from sklearn.model_selection import (
    train_test_split,
    cross_val_score
)


class CorrelationAnalysis:

    @staticmethod
    def performance_vs_activity(df):

        correlation, p_value = pearsonr(
            df["activity_score"],
            df["performance_score"]
        )

        return {
            "correlation": round(float(correlation), 4),
            "p_value": float(p_value)
        }


    @staticmethod
    def performance_vs_hourly_rate(df):

        correlation, p_value = pearsonr(
            df["hourly_rate"],
            df["performance_score"]
        )

        return {
            "correlation": round(float(correlation), 4),
            "p_value": float(p_value)
        }


    @staticmethod
    def regression_model(df):

        X = df[["activity_score"]]

        y = df["performance_score"]


        X_train, X_test, y_train, y_test = train_test_split(

            X,
            y,

            test_size=0.20,

            random_state=42
        )


        model = LinearRegression()

        model.fit(
            X_train,
            y_train
        )


        predictions = model.predict(
            X_test
        )


        mae = mean_absolute_error(
            y_test,
            predictions
        )


        rmse = np.sqrt(

            mean_squared_error(
                y_test,
                predictions
            )
        )


        r2 = r2_score(
            y_test,
            predictions
        )


        cv_scores = cross_val_score(

            model,

            X,

            y,

            cv=5,

            scoring="r2"
        )


        return {

            "model":
                model,

            "slope":
                round(
                    float(
                        model.coef_[0]
                    ),
                    4
                ),

            "intercept":
                round(
                    float(
                        model.intercept_
                    ),
                    4
                ),

            "r2":
                round(
                    float(r2),
                    4
                ),

            "mae":
                round(
                    float(mae),
                    4
                ),

            "rmse":
                round(
                    float(rmse),
                    4
                ),

            "cv_mean":
                round(
                    float(
                        cv_scores.mean()
                    ),
                    4
                ),

            "cv_std":
                round(
                    float(
                        cv_scores.std()
                    ),
                    4
                )
        }


    @staticmethod
    def predict_performance(
        model,
        activity_score
    ):

        prediction = model.predict(
            [[activity_score]]
        )[0]

        return round(
            float(prediction),
            2
        )


    @staticmethod
    def interpret_correlation(r):

        r = abs(r)

        if r < 0.20:

            return "Corrélation très faible"

        elif r < 0.40:

            return "Corrélation faible"

        elif r < 0.60:

            return "Corrélation modérée"

        elif r < 0.80:

            return "Corrélation forte"

        else:

            return "Corrélation très forte"


    @staticmethod
    def business_interpretation(

        activity_result,
        regression_result

    ):

        r = activity_result["correlation"]

        r2 = regression_result["r2"]

        mae = regression_result["mae"]

        interpretation = []


        interpretation.append(

            f"Le coefficient de corrélation "
            f"entre l'activité et la performance "
            f"est de {r}, ce qui correspond à une "
            f"{CorrelationAnalysis.interpret_correlation(r).lower()}."
        )


        interpretation.append(

            f"Le modèle explique "
            f"{round(r2*100,2)}% "
            f"de la variabilité observée."
        )


        interpretation.append(

            f"L'erreur moyenne absolue "
            f"est de {mae} points."
        )


        if r2 >= 0.70:

            conclusion = (

                "L'utilisation du niveau "
                "d'activité pour anticiper "
                "la performance semble "
                "très pertinente."
            )

        elif r2 >= 0.50:

            conclusion = (

                "Une prédiction préliminaire "
                "reste raisonnable, mais "
                "ne doit pas remplacer "
                "une évaluation réelle."
            )

        else:

            conclusion = (

                "Le niveau d'activité seul "
                "ne suffit pas pour produire "
                "une prédiction fiable."
            )


        interpretation.append(conclusion)

        return "\n\n".join(interpretation)