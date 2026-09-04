# src/statistics/descriptive_analysis.py

"""
INF232
THÈME B

Question 1 :
Analyse descriptive des performances des freelances.
"""

import numpy as np
import pandas as pd
from scipy.stats import mode
from scipy.stats import skew
from scipy.stats import kurtosis


class DescriptiveAnalysis:

    @staticmethod
    def compute_statistics(df):

        x = df["performance_score"]

        q1 = x.quantile(0.25)
        q2 = x.quantile(0.50)
        q3 = x.quantile(0.75)

        iqr = q3 - q1

        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        outliers = x[
            (x < lower_bound)
            |
            (x > upper_bound)
        ]

        stats = {

            "count":
                int(x.count()),

            "mean":
                round(float(x.mean()), 2),

            "median":
                round(float(x.median()), 2),

            "mode":
                round(
                    float(
                        mode(
                            x,
                            keepdims=True
                        ).mode[0]
                    ),
                    2
                ),

            "variance":
                round(
                    float(x.var()),
                    2
                ),

            "std":
                round(
                    float(x.std()),
                    2
                ),

            "min":
                round(
                    float(x.min()),
                    2
                ),

            "max":
                round(
                    float(x.max()),
                    2
                ),

            "range":
                round(
                    float(
                        x.max() - x.min()
                    ),
                    2
                ),

            "cv":
                round(
                    float(
                        (x.std() / x.mean()) * 100
                    ),
                    2
                ),

            "q1":
                round(float(q1), 2),

            "q2":
                round(float(q2), 2),

            "q3":
                round(float(q3), 2),

            "iqr":
                round(float(iqr), 2),

            "lower_bound":
                round(float(lower_bound), 2),

            "upper_bound":
                round(float(upper_bound), 2),

            "outliers_count":
                int(len(outliers)),

            "outliers":
                list(
                    np.round(
                        outliers.values,
                        2
                    )
                ),

            "skewness":
                round(
                    float(skew(x)),
                    3
                ),

            "kurtosis":
                round(
                    float(kurtosis(x)),
                    3
                )
        }

        return stats


    @staticmethod
    def investor_summary(stats):

        mean = stats["mean"]
        std = stats["std"]
        cv = stats["cv"]
        outliers = stats["outliers_count"]

        interpretation = []

        if cv < 15:

            homogeneity = (
                "très homogène"
            )

        elif cv < 30:

            homogeneity = (
                "modérément dispersée"
            )

        else:

            homogeneity = (
                "fortement dispersée"
            )


        interpretation.append(

            f"La performance moyenne des freelances "
            f"est de {mean}/100 avec un écart-type "
            f"de {std}. La population étudiée est "
            f"{homogeneity} (CV = {cv}%)."
        )


        if outliers == 0:

            interpretation.append(

                "Aucune valeur atypique "
                "n'a été détectée."
            )

        else:

            interpretation.append(

                f"{outliers} freelances présentent "
                f"des performances inhabituelles "
                f"et méritent une attention "
                f"particulière."
            )


        interpretation.append(

            "Pour les investisseurs, cette "
            "distribution traduit une plateforme "
            "globalement stable et cohérente."
        )

        return "\n\n".join(interpretation)