from typing import Literal

def siri_equation(body_density: float) -> float:
    return (495 / body_density) - 450


def body_fat_7_site(
    sum_mm: float,
    age: int,
    gender: Literal["male", "female"]
) -> float:
    gender = gender.lower()

    if gender == "male":
        body_density = (
            1.112
            - 0.00043499 * sum_mm
            + 0.00000055 * (sum_mm ** 2)
            - 0.00028826 * age
        )
    elif gender == "female":
        body_density = (
            1.097
            - 0.00046971 * sum_mm
            + 0.00000056 * (sum_mm ** 2)
            - 0.00012828 * age
        )
    else:
        raise ValueError("Gender must be 'male' or 'female'")

    return round(siri_equation(body_density), 2)


def body_fat_12_site(
    sum_mm: float,
    age: int,
    gender: Literal["male", "female"]
) -> float:
    if gender not in ["male", "female"]:
        raise ValueError("Gender must be 'male' or 'female'")

    body_density = (
        1.10938
        - 0.0008267 * sum_mm
        + 0.0000016 * (sum_mm ** 2)
        - 0.0002574 * age
    )

    return round(siri_equation(body_density), 2)
