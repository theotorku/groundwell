/**
 * SiteCard Component
 * Displays site risk summary card
 */

import { Building2, TrendingUp, TrendingDown, Minus } from 'lucide-react'
import { RiskBadge } from './RiskBadge'
import { cn } from '@/lib/utils'

export function SiteCard({ site, onClick }) {
    const riskScore = site.risk_score
    const trend = riskScore?.trend || 'stable'

    const TrendIcon = trend === 'deteriorating' ? TrendingUp :
        trend === 'improving' ? TrendingDown : Minus

    const trendColor = trend === 'deteriorating' ? 'text-red-400' :
        trend === 'improving' ? 'text-green-400' : 'text-gray-400'

    return (
        <div
            onClick={onClick}
            className="glass p-6 rounded-lg cursor-pointer hover:bg-white/10 transition-all duration-200 group"
        >
            <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                    <div className="p-2 rounded-lg bg-primary/10">
                        <Building2 className="h-5 w-5 text-primary" />
                    </div>
                    <div>
                        <h3 className="font-semibold text-lg group-hover:text-primary transition-colors">
                            {site.name}
                        </h3>
                        <p className="text-sm text-muted-foreground">{site.location}</p>
                    </div>
                </div>
                <RiskBadge score={riskScore?.score || 0} />
            </div>

            <div className="flex items-center justify-between">
                <div className="text-sm">
                    <p className="text-muted-foreground">
                        {riskScore?.metadata?.total_signals || 0} active signals
                    </p>
                    <p className="text-xs text-muted-foreground mt-1">
                        {site.site_type} • {site.region || 'No region'}
                    </p>
                </div>

                <div className={cn('flex items-center gap-1 text-sm', trendColor)}>
                    <TrendIcon className="h-4 w-4" />
                    <span className="capitalize">{trend}</span>
                </div>
            </div>
        </div>
    )
}
