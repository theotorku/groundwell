/**
 * API service for Groundswell backend
 */

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

class ApiService {
    async get(endpoint) {
        const response = await fetch(`${API_BASE}${endpoint}`)
        if (!response.ok) {
            throw new Error(`API  error: ${response.statusText}`)
        }
        return response.json()
    }

    async post(endpoint, data) {
        const response = await fetch(`${API_BASE}${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        if (!response.ok) {
            throw new Error(`API error: ${response.statusText}`)
        }
        return response.json()
    }

    // Sites
    async getAtRiskSites(minScore = 50.0, limit = 50) {
        return this.get(`/api/sites/at-risk?min_score=${minScore}&limit=${limit}`)
    }

    async getSite(siteId) {
        return this.get(`/api/sites/${siteId}`)
    }

    async getSiteHistory(siteId) {
        return this.get(`/api/sites/${siteId}/history`)
    }

    // Signals
    async getSignalsBreakdown(filters = {}) {
        const params = new URLSearchParams(filters).toString()
        return this.get(`/api/signals/breakdown${params ? `?${params}` : ''}`)
    }

    async resolveSignal(signalId) {
        const response = await fetch(`${API_BASE}/api/signals/${signalId}/resolve`, {
            method: 'PATCH',
        })
        if (!response.ok) {
            throw new Error(`API error: ${response.statusText}`)
        }
        return response.json()
    }

    // Inspections
    async ingestInspection(inspection) {
        return this.post('/api/inspections/ingest', inspection)
    }

    // Work Orders
    async ingestWorkOrder(workOrder) {
        return this.post('/api/work-orders/ingest', workOrder)
    }
}

export const api = new ApiService()
