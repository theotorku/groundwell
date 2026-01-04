/**
 * SignalTimeline Component
 * Displays chronological list of execution signals
 */

import { AlertTriangle, Clock, CheckCircle } from 'lucide-react'
import { formatDate, getSeverityBadgeClass, cn } from '@/lib/utils'

export function SignalTimeline({ signals }) {
    if (!signals || signals.length === 0) {
        return (
            <div className="text-center py-12 text-muted-foreground">
                <CheckCircle className="h-12 w-12 mx-auto mb-4 text-green-500" />
                <p>No active execution signals. Site is performing well!</p>
            </div>
        )
    }

    return (
        <div className="space-y-4">
            {signals.map((signal, index) => (
                <div
                    key={signal.signal_id}
                    className="glass p-4 rounded-lg border-l-4 border-l-orange-500"
                >
                    <div className="flex items-start justify-between mb-2">
                        <div className="flex items-center gap-2">
                            <AlertTriangle className="h-5 w-5 text-orange-400" />
                            <h4 className="font-semibold capitalize">
                                {signal.signal_type.replace(/_/g, ' ')}
                            </h4>
                        </div>
                        <span className={cn(
                            'px-2 py-1 rounded text-xs font-medium border',
                            getSeverityBadgeClass(signal.severity)
                        )}>
                            {signal.severity}
                        </span>
                    </div>

                    <p className="text-sm text-muted-foreground mb-3">
                        {signal.explanation}
                    </p>

                    {signal.evidence?.quote && (
                        <div className="bg-black/30 p-3 rounded border border-white/10 mb-3">
                            <p className="text-sm italic text-gray-300">
                                "{signal.evidence.quote}"
                            </p>
                        </div>
                    )}

                    <div className="flex items-center justify-between text-xs text-muted-foreground">
                        <div className="flex items-center gap-2">
                            <Clock className="h-3 w-3" />
                            <span>{formatDate(signal.detected_date)}</span>
                        </div>
                        <span>Confidence: {(signal.confidence_score * 100).toFixed(0)}%</span>
                    </div>
                </div>
            ))}
        </div>
    )
}
