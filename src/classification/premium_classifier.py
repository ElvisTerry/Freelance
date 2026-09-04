# src/classification/premium_classifier.py

import pandas as pd

from sklearn.model_selection import (
    train_test_split,
    cross_val_score
)

from sklearn.preprocessing import StandardScaler

from sklearn.pipeline import Pipeline

from sklearn.linear_model import LogisticRegression

from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    roc_auc_score
)


class PremiumClassifier:

    FEATURES = [
        "activity_score",
        "hourly_rate"
    ]

    TARGET = "profile_type"

    def __init__(self, df):

        self.df = df.copy()

        self.X = self.df[self.FEATURES]

        self.y = self.df[self.TARGET]

        (
            self.X_train,
            self.X_test,
            self.y_train,
            self.y_test

        ) = train_test_split(

            self.X,
            self.y,

            test_size=0.20,

            stratify=self.y,

            random_state=42
        )

    # ==================================================
    # LOGISTIC REGRESSION
    # ==================================================

    def logistic_model(self):

        pipeline = Pipeline([

            ("scaler", StandardScaler()),

            ("model", LogisticRegression(
                max_iter=1000,
                random_state=42
            ))

        ])

        pipeline.fit(
            self.X_train,
            self.y_train
        )

        predictions = pipeline.predict(
            self.X_test
        )

        probabilities = pipeline.predict_proba(
            self.X_test
        )[:, 1]

        return self._evaluate_model(
            pipeline,
            predictions,
            probabilities,
            "Logistic Regression"
        )

    # ==================================================
    # RANDOM FOREST
    # ==================================================

    def random_forest_model(self):

        model = RandomForestClassifier(

            n_estimators=300,

            max_depth=8,

            random_state=42
        )

        model.fit(
            self.X_train,
            self.y_train
        )

        predictions = model.predict(
            self.X_test
        )

        probabilities = model.predict_proba(
            self.X_test
        )[:, 1]

        result = self._evaluate_model(

            model,

            predictions,

            probabilities,

            "Random Forest"
        )

        result["feature_importance"] = {

            feature: importance

            for feature, importance in zip(

                self.FEATURES,

                model.feature_importances_
            )
        }

        return result

    # ==================================================
    # ÉVALUATION
    # ==================================================

    def _evaluate_model(

        self,

        model,

        predictions,

        probabilities,

        name
    ):

        accuracy = accuracy_score(
            self.y_test,
            predictions
        )

        precision = precision_score(
            self.y_test,
            predictions,
            pos_label="Premium"
        )

        recall = recall_score(
            self.y_test,
            predictions,
            pos_label="Premium"
        )

        f1 = f1_score(
            self.y_test,
            predictions,
            pos_label="Premium"
        )

        auc = roc_auc_score(

            (self.y_test == "Premium").astype(int),

            probabilities
        )

        cv_scores = cross_val_score(

            model,

            self.X,

            self.y,

            cv=5,

            scoring="accuracy"
        )

        cm = confusion_matrix(
            self.y_test,
            predictions
        )

        return {

            "name": name,

            "accuracy": round(float(accuracy), 4),

            "precision": round(float(precision), 4),

            "recall": round(float(recall), 4),

            "f1": round(float(f1), 4),

            "auc": round(float(auc), 4),

            "cv_mean": round(float(cv_scores.mean()), 4),

            "cv_std": round(float(cv_scores.std()), 4),

            "confusion_matrix": cm.tolist(),

            "model": model
        }

    # ==================================================
    # COMPARAISON
    # ==================================================

    def compare_models(self):

        logistic = self.logistic_model()

        rf = self.random_forest_model()

        return [logistic, rf]

    # ==================================================
    # PRÉDICTION
    # ==================================================

    def predict_profile(

        self,

        model,

        activity_score,

        hourly_rate
    ):

        prediction = model.predict([[
            activity_score,
            hourly_rate
        ]])[0]

        return prediction

    # ==================================================
    # INTERPRÉTATION MÉTIER
    # ==================================================

    def business_risk_analysis(self, accuracy):

        if accuracy >= 0.95:

            return (
                "Le système peut assister fortement les équipes "
                "commerciales, mais une validation humaine reste "
                "recommandée pour éviter des erreurs coûteuses."
            )

        elif accuracy >= 0.85:

            return (
                "Le système constitue une aide pertinente, mais "
                "des erreurs de classification restent possibles."
            )

        else:

            return (
                "Le risque commercial est important. "
                "Une automatisation complète n'est pas conseillée."
            )