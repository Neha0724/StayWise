import { Activity, ArrowUpRight } from 'lucide-react'

export function PageTitle({ eyebrow, title, description, action }) {
  return <div className="page-heading"><div><div className="eyebrow">{eyebrow}</div><h1>{title}</h1><p>{description}</p></div>{action}</div>
}

export function Metric({ label, value, change, icon: Icon, tint = 'teal', foot }) {
  return <div className="metric-card"><div className="metric-top"><span>{label}</span><span className={`metric-icon ${tint}`}><Icon size={18}/></span></div><div className="metric-value">{value}</div><div className="metric-foot"><span className="metric-change"><ArrowUpRight size={13}/>{change}</span><span>{foot}</span></div></div>
}

export function SectionHead({ title, subtitle, link, onClick }) {
  return <div className="section-head"><div><h3>{title}</h3><p>{subtitle}</p></div>{link && <button className="text-link" onClick={onClick}>{link}<ArrowUpRight size={14}/></button>}</div>
}

export function Loading() {
  return <div className="loading"><span className="spin">◌</span> Preparing your workspace…</div>
}

export function SlidersIcon() {
  return <Activity size={19}/>
}

export function Field({ label, suffix, children }) {
  return <label className="field"><span>{label}{suffix && <small>{suffix}</small>}</span>{children}</label>
}
