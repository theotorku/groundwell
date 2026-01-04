"""Risk Scoring Agent"""

from datetime import datetime, timedelta
from typing import Optional
from collections import defaultdict
import uuid

from backend.models import RiskScore, ExecutionSignal


class RiskScorerAgent:
    """
    Deterministic risk scoring engine for site-level execution risk
    
    Uses rule-based scoring to ensure explainability and consistency.
    No ML in Phase 0 - pure logic.
    """
    
    # Severity weights (how much each severity contributes to risk)
    SEVERITY_WEIGHTS = {
        "critical": 25.0,
        "high": 15.0,
        "medium": 8.0,
        "low": 3.0
    }
    
    # Recency multiplier (newer signals weighted more heavily)
    def _get_recency_multiplier(self, signal_age_days: int) -> float:
        """Calculate recency multiplier based on signal age"""
        if signal_age_days <= 7:
            return 1.0  # Full weight for signals within 7 days
        elif signal_age_days <= 30:
            return 0.7  # 70% weight for signals within 30 days
        elif signal_age_days <= 90:
            return 0.4  # 40% weight for signals within 90 days
        else:
            return 0.2  # 20% weight for older signals
    
    def calculate_site_risk(
        self,
        site_id: str,
        signals: list[ExecutionSignal],
        previous_score: Optional[RiskScore] = None
    ) -> RiskScore:
        """
        Calculate risk score for a site based on execution signals
        
        Args:
            site_id: Site identifier
            signals: List of execution signals for this site
            previous_score: Previous risk score for trend calculation
            
        Returns:
            RiskScore object with detailed breakdown
        """
        now = datetime.utcnow()
        
        # Filter to unresolved signals only
        active_signals = [s for s in signals if not s.resolved]
        
        # Calculate total risk score
        total_score = 0.0
        breakdown_by_type = defaultdict(float)
        
        for signal in active_signals:
            # Base score from severity
            base_score = self.SEVERITY_WEIGHTS.get(signal.severity, 0.0)
            
            # Apply confidence score
            confidence_adjusted = base_score * signal.confidence_score
            
            # Apply recency decay
            signal_age = (now - signal.detected_date).days
            recency_multiplier = self._get_recency_multiplier(signal_age)
            
            final_score = confidence_adjusted * recency_multiplier
            
            total_score += final_score
            breakdown_by_type[signal.signal_type] += final_score
        
        # Cap at 100
        total_score = min(total_score, 100.0)
        
        # Determine trend
        trend = self._calculate_trend(total_score, previous_score)
        
        # Generate explanation
        explanation = self._generate_explanation(
            total_score,
            active_signals,
            breakdown_by_type
        )
        
        # Create risk score
        risk_score = RiskScore(
            risk_score_id=str(uuid.uuid4()),
            site_id=site_id,
            score=round(total_score, 2),
            calculated_date=now,
            contributing_signals=[s.signal_id for s in active_signals],
            explanation=explanation,
            trend=trend,
            breakdown=dict(breakdown_by_type),
            metadata={
                "total_signals": len(active_signals),
                "critical_signals": len([s for s in active_signals if s.severity == "critical"]),
                "high_signals": len([s for s in active_signals if s.severity == "high"])
            }
        )
        
        return risk_score
    
    def _calculate_trend(
        self,
        current_score: float,
        previous_score: Optional[RiskScore]
    ) -> str:
        """Determine if risk is improving, stable, or deteriorating"""
        if previous_score is None:
            return "stable"
        
        change = current_score - previous_score.score
        
        if change > 5.0:
            return "deteriorating"
        elif change < -5.0:
            return "improving"
        else:
            return "stable"
    
    def _generate_explanation(
        self,
        score: float,
        signals: list[ExecutionSignal],
        breakdown: dict
    ) -> str:
        """Generate human-readable explanation of risk score"""
        if not signals:
            return "No active execution signals. Site is performing well."
        
        # Count by severity
        critical_count = len([s for s in signals if s.severity == "critical"])
        high_count = len([s for s in signals if s.severity == "high"])
        medium_count = len([s for s in signals if s.severity == "medium"])
        low_count = len([s for s in signals if s.severity == "low"])
        
        # Build explanation
        parts = []
        
        if critical_count > 0:
            parts.append(f"{critical_count} critical issue{'s' if critical_count > 1 else ''}")
        if high_count > 0:
            parts.append(f"{high_count} high-severity issue{'s' if high_count > 1 else ''}")
        if medium_count > 0:
            parts.append(f"{medium_count} medium-severity issue{'s' if medium_count > 1 else ''}")
        if low_count > 0:
            parts.append(f"{low_count} low-severity issue{'s' if low_count > 1 else ''}")
        
        severity_text = ", ".join(parts)
        
        # Top contributing signal types
        top_types = sorted(breakdown.items(), key=lambda x: x[1], reverse=True)[:3]
        type_text = ", ".join([t.replace("_", " ") for t, _ in top_types])
        
        explanation = f"Site shows elevated risk (score: {score:.1f}) due to {severity_text}. "
        explanation += f"Primary concerns: {type_text}."
        
        return explanation
    
    def rank_sites(self, risk_scores: list[RiskScore]) -> list[RiskScore]:
        """
        Rank sites by risk score (highest first)
        
        Args:
            risk_scores: List of RiskScore objects
            
        Returns:
            Sorted list of RiskScore objects
        """
        return sorted(risk_scores, key=lambda x: x.score, reverse=True)
