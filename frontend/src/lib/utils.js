import { clsx } from "clsx"

export function cn(...inputs) {
    return clsx(inputs)
}

export function formatDate(dateString) {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    })
}

export function getRiskColor(score) {
    if (score >= 75) return 'text-red-500'
    if (score >= 50) return 'text-orange-500'
    if (score >= 25) return 'text-yellow-500'
    return 'text-green-500'
}

export function getRiskBadgeClass(score) {
    if (score >= 75) return 'bg-red-500/20 text-red-400 border-red-500/30'
    if (score >= 50) return 'bg-orange-500/20 text-orange-400 border-orange-500/30'
    if (score >= 25) return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30'
    return 'bg-green-500/20 text-green-400 border-green-500/30'
}

export function getSeverityBadgeClass(severity) {
    const severityMap = {
        critical: 'bg-red-500/20 text-red -400 border-red-500/30',
        high: 'bg-orange-500/20 text-orange-400 border-orange-500/30',
        medium: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30',
        low: 'bg-blue-500/20 text-blue-400 border-blue-500/30'
    }
    return severityMap[severity] || 'bg-gray-500/20 text-gray-400 border-gray-500/30'
}
