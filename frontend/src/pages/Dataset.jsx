import { useState } from 'react'
import {
  ArrowDownToLine,
  Check,
  Database,
  Activity,
  Gauge,
  Search,
  BarChart3
} from 'lucide-react'

import { PageTitle, Metric, SectionHead, Loading } from '../components/Common'
import { API, money, number } from '../utils/config'

export default function Dataset({data}){
 const [query,setQuery]=useState(''),[filter,setFilter]=useState('All')
 if(!data)return <Loading/>
 const sample=data.sample.filter(r=>(filter==='All'||r.hotel_type===filter)&&Object.values(r).join(' ').toLowerCase().includes(query.toLowerCase()))
 return <><PageTitle eyebrow="DATA EXPLORER" title={<>Know the data <em>you model.</em></>} description="Inspect sample records, missing values, numerical summaries and the fields used by the regression pipeline." action={<a className="primary-btn anchor-btn" href={`${API}/dataset.csv`}><ArrowDownToLine size={16}/> Download CSV</a>}/><div className="dataset-warning"><Database size={18}/><div><b>Teaching dataset · {number(data.rows)} rows</b><p>{data.dataset_note} It includes a few missing values so preprocessing and imputation can be demonstrated.</p></div></div><div className="metric-grid"><Metric label="Observations" value={number(data.rows)} change="Rows" icon={Database} foot="records"/><Metric label="Variables" value={data.columns} change="Columns" icon={BarChart3} foot="features + target"/><Metric label="Missing cells" value={data.missing_cells} change="Preprocessing" icon={Activity} foot="handled by pipeline"/><Metric label="Numeric outlier flags" value={Object.values(data.outlier_counts).reduce((a,b)=>a+b,0)} change="IQR rule" icon={Gauge} foot="counts across columns"/></div><section className="panel"><SectionHead title="Sample records" subtitle="First eight rows, including missing values where present."/><div className="table-tools"><input placeholder="Search sample fields…" value={query} onChange={e=>setQuery(e.target.value)}/><select value={filter} onChange={e=>setFilter(e.target.value)}><option>All</option>{['Boutique','Business','Resort','Budget','Luxury'].map(x=><option>{x}</option>)}</select></div><div className="table-scroll"><table className="data-table"><thead><tr>{['hotel_type','city','price_per_night','star_category','cleanliness_score','service_score','location_score','amenities_score','value_score','review_count','rating'].map(c=><th key={c}>{c.replaceAll('_',' ')}</th>)}</tr></thead><tbody>{sample.map((r,i)=><tr key={i}>{Object.values(r).map((v,j)=><td key={j}>{v===null||v===undefined?<span className="missing-cell">Missing</span>:v}</td>)}</tr>)}{sample.length===0&&<tr><td colSpan="11">No matching rows in this sample.</td></tr>}</tbody></table></div><div className="table-foot">Showing {sample.length} of {data.rows} dataset rows in the preview. Download the CSV for the full dataset.</div></section><div className="content-grid"><section className="panel"><SectionHead title="Missing values by field" subtitle="Data quality check before model fitting"/><div className="missing-list">{data.missing_by_column.filter(x=>x.missing>0).map(x=><div className="missing-row" key={x.name}><span>{x.name.replaceAll('_',' ')}</span><div><i style={{width:`${x.missing/data.rows*100}%`}}/></div><b>{x.missing}</b></div>)}</div><div className="mini-note"><span className="note-icon"><Check size={16}/></span><p>Numeric missing values use median imputation; categorical fields use the most frequent category in the trained pipeline.</p></div></section><section className="panel"><SectionHead title="Dataset field guide" subtitle="What each group contributes to prediction"/><div className="field-guide">{[{t:'Property context',v:'hotel_type, city, star_category'},{t:'Price & value',v:'price_per_night, value_score'},{t:'Guest experience',v:'cleanliness_score, service_score, location_score, amenities_score'},{t:'Review history',v:'review_count'},{t:'Prediction target',v:'rating (1–5)' }].map(x=><div key={x.t}><span>{x.t}</span><b>{x.v}</b></div>)}</div></section></div></>
}
