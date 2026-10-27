import { ArrowUpRight, ChevronDown, CircleHelp, Waves, X } from 'lucide-react'
import { navItems } from '../utils/config'

export default function Sidebar({ page, setPage, mobile, setMobile }) {
  return <aside className={`sidebar ${mobile ? 'mobile-open' : ''}`}>
    <div className="brand"><div className="brand-mark"><Waves size={22}/></div><div><div className="brand-name">staywise<span>.</span></div><div className="brand-sub">HOTEL INTELLIGENCE</div></div><button className="mobile-close" onClick={() => setMobile(false)}><X size={18}/></button></div>
    <div className="workspace-label">WORKSPACE</div>
    <nav>{navItems.map(item => <button key={item.id} onClick={() => { setPage(item.id); setMobile(false) }} className={`nav-item ${page === item.id ? 'active' : ''}`}><item.icon size={18}/><span>{item.label}</span>{item.id === 'predict' && <span className="nav-new">AI</span>}</button>)}</nav>
    <div className="sidebar-bottom"><div className="help-card"><div className="help-icon"><CircleHelp size={18}/></div><strong>Working on a practical?</strong><p>Explore the methods behind every prediction.</p><button onClick={() => setPage('insights')}>Explore methods <ArrowUpRight size={14}/></button></div><div className="profile"><div className="avatar">SW</div><div className="profile-text"><b>SI Project</b><span>Regression · Lab series</span></div><ChevronDown size={15}/></div></div>
  </aside>
}
