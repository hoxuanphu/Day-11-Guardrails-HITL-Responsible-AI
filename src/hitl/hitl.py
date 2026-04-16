"""
Lab 11 — Part 4: Human-in-the-Loop Design
  TODO 12: Confidence Router
  TODO 13: Design 3 HITL decision points
"""
from dataclasses import dataclass


# ============================================================
# TODO 12: Implement ConfidenceRouter
#
# Route agent responses based on confidence scores:
#   - HIGH (>= 0.9): Auto-send to user
#   - MEDIUM (0.7 - 0.9): Queue for human review
#   - LOW (< 0.7): Escalate to human immediately
#
# Special case: if the action is HIGH_RISK (e.g., money transfer,
# account deletion), ALWAYS escalate regardless of confidence.
#
# Implement the route() method.
# ============================================================

HIGH_RISK_ACTIONS = [
    "transfer_money",
    "close_account",
    "change_password",
    "delete_data",
    "update_personal_info",
]


@dataclass
class RoutingDecision:
    """Result of the confidence router."""
    action: str          # "auto_send", "queue_review", "escalate"
    confidence: float
    reason: str
    priority: str        # "low", "normal", "high"
    requires_human: bool


class ConfidenceRouter:
    """Route agent responses based on confidence and risk level.

    Thresholds:
        HIGH:   confidence >= 0.9 -> auto-send
        MEDIUM: 0.7 <= confidence < 0.9 -> queue for review
        LOW:    confidence < 0.7 -> escalate to human

    High-risk actions always escalate regardless of confidence.
    """

    HIGH_THRESHOLD = 0.9
    MEDIUM_THRESHOLD = 0.7

    def route(self, response: str, confidence: float,
              action_type: str = "general") -> RoutingDecision:
        """Route a response based on confidence score and action type.

        Args:
            response: The agent's response text
            confidence: Confidence score between 0.0 and 1.0
            action_type: Type of action (e.g., "general", "transfer_money")

        Returns:
            RoutingDecision with routing action and metadata
        """

        if action_type in HIGH_RISK_ACTIONS:
            return RoutingDecision(
                action="escalate",
                confidence=confidence,
                reason=f"High-risk action: {action_type}",
                priority="high",
                requires_human=True
            )

        if confidence >= self.HIGH_THRESHOLD:
            return RoutingDecision(
                action="auto_send",
                confidence=confidence,
                reason="High confidence",
                priority="low",
                requires_human=False
            )
        elif self.MEDIUM_THRESHOLD <= confidence < self.HIGH_THRESHOLD:
            return RoutingDecision(
                action="queue_review",
                confidence=confidence,
                reason="Medium confidence",
                priority="normal",
                requires_human=True
            )
        else:
            return RoutingDecision(
                action="escalate",
                confidence=confidence,
                reason="Low confidence",
                priority="high",
                requires_human=True
            )
        #      requires_human=True, reason="Medium confidence — needs review"
        #
        #    - confidence < 0.7:
        #      action="escalate", priority="high",
        #      requires_human=True, reason="Low confidence — escalating"

        return RoutingDecision(
            action="auto_send",
            confidence=confidence,
            reason="TODO: implement routing logic",
            priority="low",
            requires_human=False,
        )  # TODO: Replace with implementation


# ============================================================
from typing import Optional


class HitlDecisionPoints:
    """3 sample HITL decision points to control AI response handling."""

    def __init__(self, router: ConfidenceRouter):
        self.router = router

    def check_sensitive_content(self, response: str, confidence: float) -> Optional[str]:
        """Decision point 1:
        Check if response contains sensitive keywords or low confidence.
        Returns a string message if human review needed, else None.
        """
        sensitive_keywords = ["password", "secret", "admin", "key", "token"]
        if any(word in response.lower() for word in sensitive_keywords):
            return "Sensitive content detected, manual review required."

        if confidence < self.router.MEDIUM_THRESHOLD:
            return "Low confidence response, manual review required."

        return None

    def check_high_risk_action(self, action_type: str) -> Optional[str]:
        """Decision point 2:
        Check if the action is high-risk (like money transfer).
        Always escalate for human approval.
        """
        if action_type in HIGH_RISK_ACTIONS:
            return f"High risk action '{action_type}' detected, escalate for approval."
        return None

    def manual_review_queue(self, routing_decision: RoutingDecision) -> Optional[str]:
        """Decision point 3:
        If previous routing was to queue for review, require manual HITL process.
        """
        if routing_decision.action == "queue_review":
            return "Response queued for manual human review."
        return None

    def evaluate(self, response: str, confidence: float, action_type: str) -> list:
        """Run all 3 HITL decision points and collect messages for manual intervention."""
        messages = []
        msg = self.check_sensitive_content(response, confidence)
        if msg:
            messages.append(msg)
        msg = self.check_high_risk_action(action_type)
        if msg:
            messages.append(msg)
        routing = self.router.route(response, confidence, action_type)
        msg = self.manual_review_queue(routing)
        if msg:
            messages.append(msg)
        return messages
#
# For each decision point, define:
# - trigger: What condition activates this HITL check?
# - hitl_model: Which model? (human-in-the-loop, human-on-the-loop,
#   human-as-tiebreaker)
# - context_needed: What info does the human reviewer need?
# - example: A concrete scenario
#
# Think about real banking scenarios where human judgment is critical.
# ============================================================

hitl_decision_points = [
    {
        "id": 1,
        "name": "TODO: Name this decision point",
        "trigger": "TODO: When does this trigger?",
        "hitl_model": "TODO: human-in-the-loop / human-on-the-loop / human-as-tiebreaker",
        "context_needed": "TODO: What does the reviewer need to see?",
        "example": "TODO: Give a concrete example scenario",
    },
    {
        "id": 2,
        "name": "TODO: Name this decision point",
        "trigger": "TODO: When does this trigger?",
        "hitl_model": "TODO: human-in-the-loop / human-on-the-loop / human-as-tiebreaker",
        "context_needed": "TODO: What does the reviewer need to see?",
        "example": "TODO: Give a concrete example scenario",
    },
    {
        "id": 3,
        "name": "TODO: Name this decision point",
        "trigger": "TODO: When does this trigger?",
        "hitl_model": "TODO: human-in-the-loop / human-on-the-loop / human-as-tiebreaker",
        "context_needed": "TODO: What does the reviewer need to see?",
        "example": "TODO: Give a concrete example scenario",
    },
]


# ============================================================
# Quick tests
# ============================================================

def test_confidence_router():
    """Test ConfidenceRouter with sample scenarios."""
    router = ConfidenceRouter()

    test_cases = [
        ("Balance inquiry", 0.95, "general"),
        ("Interest rate question", 0.82, "general"),
        ("Ambiguous request", 0.55, "general"),
        ("Transfer $50,000", 0.98, "transfer_money"),
        ("Close my account", 0.91, "close_account"),
    ]

    print("Testing ConfidenceRouter:")
    print("=" * 80)
    print(f"{'Scenario':<25} {'Conf':<6} {'Action Type':<18} {'Decision':<15} {'Priority':<10} {'Human?'}")
    print("-" * 80)

    for scenario, conf, action_type in test_cases:
        decision = router.route(scenario, conf, action_type)
        print(
            f"{scenario:<25} {conf:<6.2f} {action_type:<18} "
            f"{decision.action:<15} {decision.priority:<10} "
            f"{'Yes' if decision.requires_human else 'No'}"
        )

    print("=" * 80)


def test_hitl_points():
    """Display HITL decision points."""
    print("\nHITL Decision Points:")
    print("=" * 60)
    for point in hitl_decision_points:
        print(f"\n  Decision Point #{point['id']}: {point['name']}")
        print(f"    Trigger:  {point['trigger']}")
        print(f"    Model:    {point['hitl_model']}")
        print(f"    Context:  {point['context_needed']}")
        print(f"    Example:  {point['example']}")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    test_confidence_router()
    test_hitl_points()
