/**
 * RiskBadge Component
 * Displays risk score with color-coded styling
 */

import { cn, getRiskBadgeClass } from '@/lib/utils'

export function RiskBadge({ score, className }) {
    return (
        <div className={cn(
            'inline-flex items-center px-3 py-1 rounded-full text-sm font-semibold border',
            getRiskBadgeClass(score),
            className
        )}>
            {score.toFixed(1)}
        </div>
    )
}
