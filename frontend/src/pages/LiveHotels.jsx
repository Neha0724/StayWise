import { useEffect, useState } from 'react'
import { ArrowDownToLine, ExternalLink, Database, Globe2, LoaderCircle, RefreshCw, Star } from 'lucide-react'
import { API, number } from '../utils/config'
import { PageTitle, Metric, SectionHead } from '../components/Common'

export default function LiveHotels(){
 const [city,setCity]=useState('Mumbai')
 const [limit,setLimit]=useState('30')
 const [records,setRecords]=useState([])
 const [busy,setBusy]=useState(false)
 const [error,setError]=useState('')
 const [notice,setNotice]=useState('')
 const [loaded,setLoaded]=useState(false)
 useEffect(()=>{fetch(`${API}/scrape/hotels`).then(r=>r.ok?r.json():Promise.reject()).then(d=>{setRecords(d.records||[]);setLoaded(true)}).catch(()=>setLoaded(true))},[])
 async function fetchLive(){
  setBusy(true);setError('');setNotice('')
  try{
   const response=await fetch(`${API}/scrape/hotels`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({city,limit:Number(limit)})})
   const body=await response.json()
   if(!response.ok)throw new Error(body.detail||'Could not fetch live listings. Please retry.')
   setRecords(body.records||[])
   setNotice(`${body.count_fetched} live accommodation records fetched from ${body.display_name}. CSV has been saved by the backend.`)
  }catch(e){setError(e.message||'Network request failed. Check that the backend is running and has internet access.')}
  finally{setBusy(false)}
 }
 return <><PageTitle eyebrow="LIVE DATA ACQUISITION" title={<>Bring live listings <em>into StayWise.</em></>} description="Fetch public hotel metadata from OpenStreetMap, save the records as CSV, and run the existing regression pipeline on the fields that are available." action={<button className="primary-btn" onClick={fetchLive} disabled={busy}>{busy?<LoaderCircle size={16} className="spin"/>:<RefreshCw size={16}/>} {busy?'Fetching live data…':'Fetch live data'}</button>}/>
 <div className="dataset-warning"><Globe2 size={18}/><div><b>Live source: OpenStreetMap</b><p>Public accommodation listings may include names, locations, hotel type, star tags and website links. This source generally does not provide real guest ratings or consistent review/experience data.</p></div></div>
 <section className="panel scrape-controls"><SectionHead title="Scraping configuration" subtitle="Choose a city and the maximum number of named accommodation records to request."/><div className="scrape-form"><label>City<select value={city} onChange={e=>setCity(e.target.value)}><option>Mumbai</option><option>Delhi</option><option>Jaipur</option><option>Goa</option><option>Udaipur</option><option>Bengaluru</option><option>Pune</option><option>Hyderabad</option><option>Chennai</option><option>Kolkata</option></select></label><label>Maximum records<select value={limit} onChange={e=>setLimit(e.target.value)}><option value="10">10 records</option><option value="30">30 records</option><option value="50">50 records</option><option value="100">100 records</option></select></label><button className="primary-btn" onClick={fetchLive} disabled={busy}>{busy?<LoaderCircle size={16} className="spin"/>:<Globe2 size={16}/>} {busy?'Fetching…':'Scrape & predict'}</button></div>{error&&<div className="scrape-alert error">{error}</div>}{notice&&<div className="scrape-alert success">{notice}</div>}</section>
 <div className="metric-grid"><Metric label="Saved records" value={number(records.length)} change="CSV dataset" icon={Database} foot="live source rows"/><Metric label="Source" value="OSM" change="Open data" icon={Globe2} foot="source linked"/><Metric label="Prediction target" value="1–5" change="Regression" icon={Star} foot="illustrative estimate"/><Metric label="Live fetching" value={busy?'Running':'On demand'} change="Manual refresh" icon={RefreshCw} foot="not background polling"/></div>
 <section className="panel"><div className="section-head"><div><h3>Scraped listings & rating estimates</h3><p>Records currently saved in the live scraping CSV.</p></div><div className="scrape-downloads"><a className="primary-btn anchor-btn" href={`${API}/scrape/hotels.csv`}><ArrowDownToLine size={16}/> Download CSV</a><a className="secondary-btn anchor-btn" href={`${API}/scrape/hotels.xlsx`}><ArrowDownToLine size={16}/> Download Excel</a></div></div>
 {records.length===0?<div className="scrape-empty"><Globe2 size={25}/><b>No live records yet</b><p>Choose a city above and select “Scrape & predict”. The first request needs internet access on the backend.</p></div>:<div className="table-scroll"><table className="data-table"><thead><tr><th>Hotel / property</th><th>City</th><th>Source type</th><th>Stars</th><th>Predicted rating*</th><th>Website</th><th>Source record</th></tr></thead><tbody>{records.map((r,i)=><tr key={`${r.osm_type}-${r.osm_id}-${i}`}><td className="feature-name">{r.hotel_name||'Unnamed property'}</td><td>{r.city||r.city_searched||city}</td><td>{r.hotel_type_source||'—'}</td><td>{r.star_category??'Not listed'}</td><td><span className="corr-pill positive">{r.predicted_rating??'—'}/5</span></td><td>{r.website?<a href={r.website.startsWith('http')?r.website:`https://${r.website}`} target="_blank" rel="noreferrer">Website <ExternalLink size={11}/></a>:'Not listed'}</td><td>{r.source_url?<a href={r.source_url} target="_blank" rel="noreferrer">OpenStreetMap <ExternalLink size={11}/></a>:'—'}</td></tr>)}</tbody></table></div>}
 <p className="scrape-disclaimer">*Predictions are illustrative only. The model was trained on synthetic data. Missing nightly price, review count and guest-experience scores are imputed by the trained pipeline; these values are not real customer ratings.</p></section>
 <section className="panel"><SectionHead title="How the live-data workflow works" subtitle="A separate acquisition pipeline that preserves your existing CSV and model."/><div className="scrape-steps"><div><span>01</span><b>Fetch</b><p>Resolve the city with Nominatim and query accommodation listings through Overpass.</p></div><div><span>02</span><b>Clean & save</b><p>Keep named listings, normalize fields, store source links and timestamps, and write a persistent CSV.</p></div><div><span>03</span><b>Prepare features</b><p>Map only available fields to the existing model schema. Unknown fields remain missing and are imputed by the pipeline.</p></div><div><span>04</span><b>Predict & inspect</b><p>Show estimated rating, retain the source record, and download the scraped CSV for further analysis.</p></div></div></section>
 </>
}
