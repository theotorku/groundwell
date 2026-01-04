"""Signal Extraction Agent using Pydantic AI"""

import os
from datetime import datetime
from typing import Optional
from pydantic_ai import Agent
from pydantic import BaseModel, Field

from backend.models import ExecutionSignal


class ExtractedSignal(BaseModel):
    """Structured output for extracted execution signals"""
    signal_type: str = Field(
        ...,
        description="Type: missed_inspection, late_work_order, incomplete_task, doc_gap, sla_breach, safety_issue"
    )
    severity: str = Field(..., description="Severity: low, medium, high, critical")
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    evidence_quote: str = Field(..., description="Direct quote from source text")
    explanation: str = Field(..., description="Why this is an execution problem")


class SignalExtractionResult(BaseModel):
    """Result from signal extraction"""
    signals: list[ExtractedSignal]
    processing_notes: Optional[str] = None


class SignalExtractorAgent:
    """
    Pydantic AI agent for extracting execution signals from inspection notes and work orders
    """
    
    def __init__(self, model: str = "openai:gpt-4o"):
        """Initialize the signal extractor agent"""
        self.agent = Agent(
            model=model,
            result_type=SignalExtractionResult,
            system_prompt=self._get_system_prompt()
        )
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for signal extraction"""
        return """You are an expert facilities execution analyst. Your job is to analyze inspection notes and work orders to identify execution breakdowns.

**Signal Types:**
- **missed_inspection**: Scheduled inspection did not occur or was skipped
- **late_work_order**: Work order is past due date without completion
- **incomplete_task**: Required maintenance task identified but not completed
- **doc_gap**: Missing or incomplete documentation
- **sla_breach**: Vendor failed to meet SLA response or completion time
- **safety_issue**: Safety or compliance violation detected

**Severity Levels:**
- **critical**: Immediate safety risk, major compliance violation, or severe operational impact
- **high**: Significant risk or repeated failures
- **medium**: Moderate issues that require attention
- **low**: Minor issues with minimal impact

**Instructions:**
1. Carefully read the provided text
2. Identify all execution signals
3. For each signal, provide:
   - Signal type (from the list above)
   - Severity level
   - Confidence score (how certain you are, 0.0-1.0)
   - Evidence quote (exact text from source)
   - Explanation (why this is a problem)
4. Only extract signals with confidence >= 0.6
5. Be precise and conservative - false positives erode trust

**Important:** Do not invent information. Only extract signals clearly supported by the text."""

    async def extract_from_inspection(
        self,
        inspection_id: str,
        site_id: str,
        notes: str
    ) -> list[ExecutionSignal]:
        """
        Extract execution signals from inspection notes
        
        Args:
            inspection_id: ID of the inspection
            site_id: ID of the site
            notes: Raw inspection notes
            
        Returns:
            List of ExecutionSignal objects
        """
        user_prompt = f"""Analyze the following facilities inspection note and extract execution signals.

**Inspection Note:**
{notes}

Extract all execution signals with their severity, confidence, evidence, and explanation."""

        result = await self.agent.run(user_prompt)
        
        # Convert extracted signals to ExecutionSignal models
        signals = []
        for idx, extracted in enumerate(result.data.signals):
            signal = ExecutionSignal(
                signal_id=f"{inspection_id}_sig_{idx}",
                site_id=site_id,
                signal_type=extracted.signal_type,
                severity=extracted.severity,
                detected_date=datetime.utcnow(),
                confidence_score=extracted.confidence_score,
                evidence={
                    "quote": extracted.evidence_quote,
                    "inspection_id": inspection_id
                },
                explanation=extracted.explanation,
                source_type="inspection",
                source_id=inspection_id,
                resolved=False
            )
            signals.append(signal)
        
        return signals
    
    async def extract_from_work_order(
        self,
        work_order_id: str,
        site_id: str,
        description: str,
        created_date: datetime,
        due_date: datetime,
        status: str
    ) -> list[ExecutionSignal]:
        """
        Extract execution signals from work order
        
        Args:
            work_order_id: ID of the work order
            site_id: ID of the site
            description: Work order description
            created_date: When work order was created
            due_date: Expected completion date
            status: Current status
            
        Returns:
            List of ExecutionSignal objects
        """
        signals = []
        
        # Rule-based detection for late work orders
        if status != "completed" and datetime.utcnow() > due_date:
            days_late = (datetime.utcnow() - due_date).days
            
            # Determine severity based on how late
            if days_late >= 7:
                severity = "high"
            elif days_late >= 3:
                severity = "medium"
            else:
                severity = "low"
            
            signal = ExecutionSignal(
                signal_id=f"{work_order_id}_late",
                site_id=site_id,
                signal_type="late_work_order",
                severity=severity,
                detected_date=datetime.utcnow(),
                confidence_score=1.0,  # Rule-based, high confidence
                evidence={
                    "work_order_id": work_order_id,
                    "due_date": due_date.isoformat(),
                    "days_late": days_late
                },
                explanation=f"Work order is {days_late} days past due date without completion",
                source_type="work_order",
                source_id=work_order_id,
                resolved=False
            )
            signals.append(signal)
        
        return signals
