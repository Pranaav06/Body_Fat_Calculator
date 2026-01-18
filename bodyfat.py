from typing import Literal


# =====================================================
# CORE EQUATIONS
# =====================================================

def siri_equation(body_density: float) -> float:
    """
    Converts body density to body fat percentage
    using the Siri (1956) equation.
    """
    return (495 / body_density) - 450


# =====================================================
# 7-SITE JACKSON–POLLOCK (PROFESSIONAL STANDARD)
# =====================================================

def body_fat_7_site(
    sum_mm: float,
    age: int,
    gender: Literal["male", "female"]
) -> float:
    """
    Jackson–Pollock 7-site body fat calculation.
    Valid for lean → obese populations.

    Parameters
    ----------
    sum_mm : float
        Sum of 7 skinfolds (mm)
    age : int
        Age in years
    gender : 'male' | 'female'

    Returns
    -------
    Body fat percentage (float)
    """

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


# =====================================================
# 12-SITE YUHASZ (ATHLETE-ONLY)
# =====================================================

def body_fat_12_site_yuhasz(
    sum_mm: float,
    gender: Literal["male", "female"]
) -> float:
    """
    Yuhasz 12-site body fat formula.
    Valid ONLY for lean athletic populations (~5–15%).

    Parameters
    ----------
    sum_mm : float
        Sum of 12 skinfolds (mm)
    gender : 'male' | 'female'

    Returns
    -------
    Body fat percentage (float)
    """

    gender = gender.lower()

    if gender == "male":
        body_fat = (0.1051 * sum_mm) + 2.585

    elif gender == "female":
        body_fat = (0.1548 * sum_mm) + 3.580

    else:
        raise ValueError("Gender must be 'male' or 'female'")

    return round(body_fat, 2)


# =====================================================
# PROFESSIONAL DECISION LOGIC
# =====================================================

def calculate_body_fat(
    method: Literal["7-site", "12-site"],
    sum_mm: float,
    age: int,
    gender: Literal["male", "female"],
    athlete: bool
) -> float:
    """
    Professional decision wrapper.

    Rules
    -----
    • 7-site → always valid
    • 12-site → ONLY for lean athletes
    • Obese / high-fat athletes → 7-site enforced

    Returns
    -------
    Body fat percentage (float)
    """

    if method == "7-site":
        return body_fat_7_site(sum_mm, age, gender)

    if method == "12-site":
        if not athlete:
            raise ValueError(
                "12-site method is restricted to trained athletes only."
            )

        # Guardrail: Yuhasz breaks at high fat levels
        if sum_mm > 160:
            raise ValueError(
                "12-site Yuhasz is invalid at high fat levels. "
                "Use 7-site Jackson–Pollock instead."
            )

        return body_fat_12_site_yuhasz(sum_mm, gender)

    raise ValueError("Method must be '7-site' or '12-site'")
