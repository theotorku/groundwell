/**
 * SiteDetail Page
 * Site details with risk score and signal timeline
 */

import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { ArrowLeft, Building2, MapPin, TrendingUp } from 'lucide-react'
import { RiskBadge } from '@/components/RiskBadge'
import { SignalTimeline } from '@/components/SignalTimeline'
import { api } from '@/services/api'

export function SiteDetail() {
    const { siteId } = useParams()
    const navigate = useNavigate()
    const [data, setData] = useState(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        loadSiteData()
    }, [siteId])

    async function loadSiteData() {
        try {
            setLoading(true)
            const result = await api.getSiteHistory(siteId)
            setData(result)
        } catch (error) {
            console.error('Failed to load site data:', error)
        } finally {
            setLoading(false)
        }
    }

    if (loading) {
        return (
            <div className="min-h-screen bg-background flex items-center justify-center">
                <div className="text-center">
                    <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-current border-r-transparent"></div>
                    <p className="mt-4 text-muted-foreground">Loading site data...</p>
                </div>
            </div>
        )
    }

    if (!data) {
        return (
            <div className="min-h-screen bg-background flex items-center justify-center">
                <p className="text-muted-foreground">Site not found</p>
            </div>
        )
    }

    const site = data.site
    const latestRisk = data.risk_history?.[0]

    return (
        <div className="min-h-screen bg-background p-8">
            <div className="max-w-6xl mx-auto">
                {/* Back Button */}
                <button
                    onClick={() => navigate('/')}
                    className="flex items-center gap-2 text-muted-foreground hover:text-primary mb-6 transition-colors"
                >
                    <ArrowLeft className="h-4 w-4" />
                    Back to Dashboard
                </button>

                {/* Site Header */}
                <div className="glass p-6 rounded-lg mb-6">
                    <div className="flex items-start justify-between mb-4">
                        <div className="flex items-center gap-4">
                            <div className="p-3 rounded-lg bg-primary/10">
                                <Building2 className="h-8 w-8 text-primary" />
                            </div>
                            <div>
                                <h1 className="text-3xl font-bold mb-1">{site.name}</h1>
                                <div className="flex items-center gap-2 text-muted-foreground">
                                    <MapPin className="h-4 w-4" />
                                    <span>{site.location}</span>
                                </div>
                            </div>
                        </div>
                        {latestRisk && <RiskBadge score={latestRisk.score} className="text-lg px-4 py-2" />}
                    </div>

                    <div className="grid grid-cols-3 gap-4 mt-6">
                        <div>
                            <p className="text-sm text-muted-foreground">Type</p>
                            <p className="font-semibold capitalize">{site.site_type}</p>
                        </div>
                        <div>
                            <p className="text-sm text-muted-foreground">Region</p>
                            <p className="font-semibold">{site.region || 'N/A'}</p>
                        </div>
                        <div>
                            <p className="text-sm text-muted-foreground">Status</p>
                            <p className="font-semibold capitalize">{site.status}</p>
                        </div>
                    </div>
                </div>

                {/* Risk Explanation */}
                {latestRisk && (
                    <div className="glass p-6 rounded-lg mb-6">
                        <div className="flex items-center gap-2 mb-3">
                            <TrendingUp className="h-5 w-5 text-orange-400" />
                            <h2 className="text-xl font-semibold">Risk Assessment</h2>
                        </div>
                        <p className="text-muted-foreground">{latestRisk.explanation}</p>

                        {latestRisk.breakdown && Object.keys(latestRisk.breakdown).length > 0 && (
                            <div className="mt-4 grid grid-cols-2 md:grid-cols-4 gap-3">
                                {Object.entries(latestRisk.breakdown).map(([type, score]) => (
                                    <div key={type} className="bg-black/30 p-3 rounded">
                                        <p className="text-xs text-muted-foreground capitalize">
                                            {type.replace(/_/g, ' ')}
                                        </p>
                                        <p className="text-lg font-semibold">{score.toFixed(1)}</p>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                )}

                {/* Signal Timeline */}
                <div className="glass p-6 rounded-lg">
                    <h2 className="text-xl font-semibold mb-4">Execution Signals</h2>
                    <SignalTimeline signals={data.signals} />
                </div>
            </div>
        </div>
    )
}
