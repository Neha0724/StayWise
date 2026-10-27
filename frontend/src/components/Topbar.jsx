import { Menu } from 'lucide-react'

export default function Topbar({ activeLabel, setMobile }) {
  return <header className="topbar"><button className="mobile-menu" onClick={() => setMobile(true)}><Menu size={20}/></button><div className="breadcrumb">Workspace <span>/</span> <b>{activeLabel}</b></div><div className="top-actions"><span className="status-dot"></span><span className="live-text">API workspace</span><div className="top-avatar">SW</div></div></header>
}
