from decimal import Decimal
from core.models import RecipientRequest, DonationProject

# NLP Scoring
def medical_severity_score(text: str) -> int:
    text = text.lower()

    if any(word in text for word in ["critical", "emergency", "life-threatening", "urgent"]):
        return 4
    if any(word in text for word in ["cancer", "surgery", "organ failure", "chronic"]):
        return 3
    if any(word in text for word in ["treatment", "medication", "hospital"]):
        return 2
    return 1


def financial_hardship_score(text: str) -> int:
    text = text.lower()

    if any(word in text for word in ["no income", "unemployed", "poor", "unable to afford"]):
        return 3
    if any(word in text for word in ["low income", "struggling", "limited income"]):
        return 2
    return 1


def age_vulnerability_score(age: int) -> int:
    if age < 12 or age > 65:
        return 2
    return 1


# Priority calculation

def calculate_priority(recipient: RecipientRequest, project: DonationProject) -> Decimal:
    severity = Decimal(medical_severity_score(recipient.medical_condition))
    financial = Decimal(financial_hardship_score(recipient.financial_condition))
    age_score = Decimal(age_vulnerability_score(recipient.age))

    cost_ratio = recipient.treatment_cost / project.total_estimated_amount
    cost_pressure = min(cost_ratio, Decimal("1.0"))

    priority = (
        severity * Decimal("0.4") +
        financial * Decimal("0.3") +
        age_score * Decimal("0.1") +
        cost_pressure * Decimal("0.2")
    )

    return priority



# AI Allocation

def run_ai_allocation(project: DonationProject):
    recipients = RecipientRequest.objects.filter(
        status=RecipientRequest.STATUS_APPROVED
    )

    if not recipients.exists():
        return "No approved recipients found."

    # Calculate priorities
    scored = []
    for r in recipients:
        score = calculate_priority(r, project)
        scored.append((r, score))

    # Sort by priority (high to low)
    scored.sort(key=lambda x: x[1], reverse=True)

    total_priority = sum(score for _, score in scored)
    remaining_fund = project.total_estimated_amount

    for recipient, score in scored:
        if remaining_fund <= 0:
            break

        share = (score / total_priority) * project.total_estimated_amount

        allocation = min(
            share,
            recipient.treatment_cost,
            remaining_fund
        )


        recipient.ai_recommended_amount = allocation
        recipient.ai_explanation = (
            "Allocation based on medical severity, financial hardship, age vulnerability, "
            "and proportional project fund availability."
        )
        recipient.save()

        remaining_fund -= allocation

    return "AI allocation completed successfully."
