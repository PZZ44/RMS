def calculate_base_score(loyal_client: int) -> int:
    return 100 if loyal_client == 1 else 90


def age_hard_reject(age: int) -> tuple[bool, str | None]:
    if age < 18:
        return True, "AGE_LESS_THAN_18"
    if age > 70:
        return True, "AGE_GREATER_THAN_70"
    return False, None


def calculate_penalties(successful_loans_count: int) -> int:
    # Пока risk-service не штрафует за займы,
    # он используется как фактор для СПР
    return 0


def calculate_risk(
    age: int,
    loyal_client: int,
    successful_loans_count: int
):
    hard_reject, reason = age_hard_reject(age)
    if hard_reject:
        return {
            "base_score": 0,
            "penalties": 0,
            "final_score": 0,
            "hard_reject": True,
            "reject_reason": reason
        }

    base_score = calculate_base_score(loyal_client)
    penalties = calculate_penalties(successful_loans_count)

    final_score = max(base_score - penalties, 0)

    return {
        "base_score": base_score,
        "penalties": penalties,
        "final_score": final_score,
        "hard_reject": False,
        "reject_reason": None
    }
