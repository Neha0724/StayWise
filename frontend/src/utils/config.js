import { Activity, BrainCircuit, Database, Globe2, LayoutDashboard, Sparkles } from 'lucide-react'

export const API = '/api'
export const money = n => new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(n || 0)
export const number = n => new Intl.NumberFormat('en-IN').format(n || 0)

export const navItems = [
  { id: 'overview', label: 'Overview', icon: LayoutDashboard },
  { id: 'predict', label: 'Rating studio', icon: Sparkles },
  { id: 'insights', label: 'Statistical lab', icon: Activity },
  { id: 'models', label: 'Model performance', icon: BrainCircuit },
  { id: 'dataset', label: 'Dataset explorer', icon: Database },
  { id: 'live', label: 'Live hotel scraping', icon: Globe2 },
]

export const COLORS = ['#1c7774', '#d17a55', '#93b7b2', '#e5b79c', '#29475a', '#e4c66a']
