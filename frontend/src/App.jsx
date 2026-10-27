import { useEffect, useState } from 'react'
import { CircleHelp } from 'lucide-react'
import { API, navItems } from './utils/config'
import Overview from './pages/Overview'
import Predict from './pages/Predict'
import Insights from './pages/Insights'
import Models from './pages/Models'
import Dataset from './pages/Dataset'
import LiveHotels from './pages/LiveHotels'
import Sidebar from './components/Sidebar'
import Topbar from './components/Topbar'
import './style.css'

export default function App(){
 const [page,setPage]=useState('overview'),[data,setData]=useState(null),[analytics,setAnalytics]=useState(null),[models,setModels]=useState(null),[error,setError]=useState(''),[mobile,setMobile]=useState(false)
 useEffect(()=>{Promise.all([fetch(`${API}/overview`).then(r=>{if(!r.ok)throw Error('API unavailable');return r.json()}),fetch(`${API}/analytics`).then(r=>r.json()),fetch(`${API}/models`).then(r=>r.json())]).then(([d,a,m])=>{setData(d);setAnalytics(a);setModels(m)}).catch(()=>setError('Backend is not connected yet. Start the FastAPI server using the README steps, then refresh this page.'))},[])
 const active=navItems.find(n=>n.id===page)
 return <div className="app-shell">
  <Sidebar page={page} setPage={setPage} mobile={mobile} setMobile={setMobile}/>
  <main className="main-area"><Topbar activeLabel={active?.label} setMobile={setMobile}/>
   <div className="page-content">
    {error&&<div className="error-banner"><CircleHelp size={18}/><div><b>Backend not ready</b><p>{error}</p></div></div>}
    {page==='overview'&&<Overview data={data} setPage={setPage}/>}
    {page==='predict'&&<Predict/>}
    {page==='insights'&&<Insights data={data} analytics={analytics}/>}
    {page==='models'&&<Models models={models}/>}
    {page==='dataset'&&<Dataset data={data}/>}
    {page==='live'&&<LiveHotels/>}
    <footer><span>STAYWISE <b>·</b> SI PRACTICAL PROJECT</span><span>Built for learning · Synthetic demo dataset</span></footer>
   </div>
  </main>
 </div>
}
