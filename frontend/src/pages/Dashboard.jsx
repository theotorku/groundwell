/**
 * Dashboard Page
 * At-risk sites list
 */

import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { AlertCircle, TrendingUp, Filter } from 'lucide-react'
import { SiteCard } from '@/components/SiteCard'
import { api } from '@/services/api'

export function Dashboard() {
    const [sites, setSites] = useState([])
    const [loading, setLoading] = useState(true)
    const [minScore, setMinScore] = useState(50)
    const navigate = useNavigate()

    useEffect(() => {
        loadSites()
    }, [minScore])

    async function loadSites() {
        try {
            setLoading(true)
            const data = await api.getAtRiskSites(minScore, 50)
            setSites(data.sites || [])
        } catch (error) {
            console.error('Failed to load sites:', error)
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="min-h-screen bg-background p-8">
            <div className="max-w-7xl mx-auto">
                {/* Header */}
                <div className="mb-8">
                    <div className="flex items-center gap-3 mb-2">
                        <div className="p-3 rounded-lg gradient-primary">
                            <TrendingUp className="h-6 w-6 text-white" />
                        </div>
                        <div>
                            <h1 className="text-3xl font-bold">At-Risk Sites</h1>
                            <p className="text-muted-foreground">
                                Execution intelligence from the ground up
                            </p>
                        </div>
                    </div>
                </div>

                {/* Filters */}
                <div className="glass p-4 rounded-lg mb-6">
                    <div className="flex items-center gap-4">
                        <Filter className="h-5 w-5 text-muted-foreground" />
                        <div className="flex items-center gap-2">
                            <label className="text-sm text-muted-foreground">
                                Minimum Risk Score:
                            </label>
                            <input
                                type="range"
                                min="0"
                                max="100"
                                value={minScore}
                                onChange={(e) => setMinScore(Number(e.target.value))}
                                className="w-32"
                            />
                            <span className="text-sm font-semibold w-12">{minScore}</span>
                        </div>
                        <div className="ml-auto text-sm text-muted-foreground">
                            {sites.length} sites
                        </div>
                    </div>
                </div>

                {/* Sites Grid */}
                {loading ? (
                    <div className="text-center py-12">
                        <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-current border-r-transparent"></div>
                        <p className="mt-4 text-muted-foreground">Loading sites...</p>
                    </div>
                ) : sites.length === 0 ? (
                    <div className="glass p-12 rounded-lg text-center">
                        <AlertCircle className="h-12 w-12 mx-auto mb-4 text-muted-foreground" />
                        <p className="text-muted-foreground">
                            No sites found above risk threshold of {minScore}
                        </p>
                    </div>
                ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        {sites.map((site) => (
                            <SiteCard
                                key={site.site_id}
                                site={site}
                                onClick={() => navigate(`/sites/${site.site_id}`)}
                            />
                        ))}
                    </div>
                )}
            </div>
        </div>
    )
}
