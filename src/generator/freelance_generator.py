# src/generator/freelance_generator.py

"""
INF232
Thème B
Plateforme Freelance / Client
"""

from pathlib import Path

import numpy as np
import pandas as pd

from src.generator.seed_generator import (
    SeedGenerator
)


class FreelanceGenerator:

    CATEGORIES = [
        "Developer",
        "Designer",
        "Writer"
    ]


    def __init__(self, chief_name):

        self.chief_name = chief_name

        self.seed = SeedGenerator.generate_seed(
            chief_name
        )

        self.rng = np.random.default_rng(
            self.seed
        )


    def generate_dataset(
        self,
        n_samples=1200,
        premium_ratio=0.4
    ):

        categories = self.rng.choice(

            self.CATEGORIES,

            size=n_samples,

            p=[0.45, 0.30, 0.25]
        )


        years_experience = self.rng.integers(

            1,
            16,
            size=n_samples
        )


        projects_completed = (

            years_experience
            * self.rng.integers(
                3,
                15,
                size=n_samples
            )

            +

            self.rng.normal(
                0,
                5,
                n_samples
            )

        ).astype(int)


        projects_completed = np.clip(

            projects_completed,

            1,

            None
        )


        activity_score = (

            years_experience * 5

            +

            self.rng.normal(
                40,
                12,
                n_samples
            )

        )


        activity_score = np.clip(

            activity_score,

            0,

            100
        )


        hourly_rate = (

            years_experience * 3

            +

            self.rng.normal(
                20,
                8,
                n_samples
            )

        )


        hourly_rate = np.clip(

            hourly_rate,

            5,

            100
        )


        client_satisfaction = (

            70

            +

            years_experience

            +

            self.rng.normal(
                0,
                8,
                n_samples
            )

        )


        client_satisfaction = np.clip(

            client_satisfaction,

            50,

            100
        )


        response_time = (

            72

            -

            years_experience * 2

            +

            self.rng.normal(
                0,
                10,
                n_samples
            )

        )


        response_time = np.clip(

            response_time,

            1,

            96
        )


        performance_score = (

            0.45 * activity_score

            +

            0.25 * hourly_rate

            +

            0.20 * client_satisfaction

            -

            0.10 * response_time

            +

            self.rng.normal(
                0,
                5,
                n_samples
            )

        )


        performance_score = np.clip(

            performance_score,

            0,

            100
        )


        premium_threshold = np.percentile(

            performance_score,

            100 * (1 - premium_ratio)
        )


        profile_type = np.where(

            performance_score >= premium_threshold,

            "Premium",

            "Standard"
        )


        df = pd.DataFrame({

            "freelancer_id":

                np.arange(
                    1,
                    n_samples + 1
                ),

            "category":
                categories,

            "years_experience":
                years_experience,

            "projects_completed":
                projects_completed,

            "activity_score":
                np.round(
                    activity_score,
                    2
                ),

            "hourly_rate":
                np.round(
                    hourly_rate,
                    2
                ),

            "client_satisfaction":
                np.round(
                    client_satisfaction,
                    2
                ),

            "response_time":
                np.round(
                    response_time,
                    2
                ),

            "performance_score":
                np.round(
                    performance_score,
                    2
                ),

            "profile_type":
                profile_type
        })


        return df


    def save_csv(
        self,
        df
    ):

        output_dir = Path("data")

        output_dir.mkdir(
            exist_ok=True
        )

        path = output_dir / "freelancers.csv"

        df.to_csv(

            path,

            index=False
        )

        return path


    def save_excel(
        self,
        df
    ):

        output_dir = Path("data")

        output_dir.mkdir(
            exist_ok=True
        )

        path = output_dir / "freelancers.xlsx"

        df.to_excel(

            path,

            index=False
        )

        return path


    def save_json(
        self,
        df
    ):

        output_dir = Path("data")

        output_dir.mkdir(
            exist_ok=True
        )

        path = output_dir / "freelancers.json"

        df.to_json(

            path,

            orient="records",

            indent=4
        )

        return path


if __name__ == "__main__":

    chef = input(
        "Nom du chef de groupe : "
    )

    generator = FreelanceGenerator(
        chef
    )

    data = generator.generate_dataset(
        premium_ratio=0.40
    )

    generator.save_csv(data)

    print("\nSeed utilisée :")
    print(generator.seed)

    print("\nDimensions :")
    print(data.shape)

    print("\nAperçu :\n")
    print(data.head())

    print("\nRépartition :\n")
    print(
        data["profile_type"]
        .value_counts()
    )