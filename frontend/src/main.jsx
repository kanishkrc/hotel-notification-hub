import React, {useEffect, useState} from 'react';
import {createRoot} from 'react-dom/client';
import './styles.css';
const api = 'http://localhost:8000/api';
function App() {
  const [hotels,setHotels]=useState([]); const [notices,setNotices]=useState([]);
  useEffect(()=>{ Promise.all([fetch(`${api}/hotels/`).then(r=>r.json()), fetch(`${api}/notifications/`).then(r=>r.json())]).then(([h,n])=>{setHotels(h);setNotices(n)}) },[]);
  return <main><header><p className="eyebrow">GUEST EXPERIENCE PLATFORM</p><h1>Notification Hub</h1><p>One calm, central view for every property.</p></header><section className="metrics"><article><b>{hotels.length}</b><span>Hotels</span></article><article><b>{notices.length}</b><span>Notifications</span></article><article><b>{notices.filter(n=>n.status==='sent').length}</b><span>Delivered</span></article></section><section><h2>Properties</h2><div className="cards">{hotels.map(h=><article className="card" key={h.id}><h3>{h.name}</h3><p>{h.city}</p><small>{h.email_from}</small></article>)}{!hotels.length&&<p>Add your first hotel in the Django admin to begin.</p>}</div></section><section><h2>Recent notifications</h2><div className="table"><div className="row head"><span>Guest</span><span>Hotel</span><span>Channel</span><span>Status</span></div>{notices.slice(0,8).map(n=><div className="row" key={n.id}><span>{n.guest_name}</span><span>{n.hotel_name}</span><span>{n.channel}</span><span className={`status ${n.status}`}>{n.status}</span></div>)}</div></section></main>}
createRoot(document.getElementById('root')).render(<App/>);
