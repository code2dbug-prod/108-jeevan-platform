"use client";
import { FormEvent, useMemo, useState } from "react";

type Precision="exact"|"approximate"|"unknown";
type Json=Record<string,unknown>|unknown[]|string|number|boolean|null;

async function postJson(path:string,body:unknown){
  const r=await fetch(path,{method:"POST",headers:{"content-type":"application/json"},body:JSON.stringify(body)});
  const j=await r.json();
  if(!r.ok)throw new Error(j.error||j.detail||"Request failed");
  return j;
}

export function ReaderConsole(){
  const [precision,setPrecision]=useState<Precision>("exact");
  const [birthPayload,setBirthPayload]=useState<Record<string,unknown>|null>(null);
  const [chart,setChart]=useState<Json>(null);
  const [dasha,setDasha]=useState<Json>(null);
  const [draw,setDraw]=useState<any>(null);
  const [synthesis,setSynthesis]=useState<any>(null);
  const [busy,setBusy]=useState(false);
  const [error,setError]=useState<string|null>(null);
  const [spreadKey,setSpreadKey]=useState("three-path");
  const [question,setQuestion]=useState("");

  const canInterpret=useMemo(()=>Boolean(question.trim()&&draw),[question,draw]);

  async function submit(e:FormEvent<HTMLFormElement>){
    e.preventDefault();setBusy(true);setError(null);setSynthesis(null);setDraw(null);
    const f=new FormData(e.currentTarget);
    const payload={
      full_name:String(f.get("full_name")||""),
      date_of_birth:String(f.get("date_of_birth")||""),
      birth_time:precision==="unknown"?null:String(f.get("birth_time")||""),
      birth_time_precision:precision,
      birthplace_label:String(f.get("birthplace_label")||""),
      latitude:Number(f.get("latitude")),
      longitude:Number(f.get("longitude")),
      timezone:String(f.get("timezone")||"Asia/Kolkata")
    };
    setBirthPayload(payload);
    try{
      if(precision==="unknown"){
        setChart(await postJson("/api/astrology/unknown-time",payload));
        setDasha(null);
      }else{
        const [full,timing]=await Promise.all([
          postJson("/api/astrology/full",payload),
          postJson("/api/astrology/dasha",payload)
        ]);
        setChart(full);setDasha(timing);
      }
    }catch(err){setError(err instanceof Error?err.message:"Calculation failed")}
    finally{setBusy(false)}
  }

  async function drawCards(){
    setError(null);setSynthesis(null);
    try{setDraw(await postJson("/api/cards/draw",{spreadKey}))}
    catch(err){setError(err instanceof Error?err.message:"Card draw failed")}
  }

  async function interpret(){
    if(!canInterpret)return;
    setBusy(true);setError(null);
    const evidence:any[]=[];
    if(chart)evidence.push({type:"natal",key:"chart",summary:precision==="unknown"?"Unknown-time uncertainty analysis":"Deterministic natal chart",confidence:precision==="exact"?1:0.7,payload:chart});
    if(dasha)evidence.push({type:"dasha",key:"current",summary:"Current Vimshottari timing",confidence:.95,payload:dasha});
    for(const item of draw?.draws||[]){
      evidence.push({
        type:"card",key:`card-${item.cardId}`,
        summary:`${item.card?.title||item.card?.cardTitle||"Card"} in ${item.position.label}`,
        confidence:.8,payload:item
      });
    }
    try{setSynthesis(await postJson("/api/readings/synthesize",{question,evidence}))}
    catch(err){setError(err instanceof Error?err.message:"Synthesis failed")}
    finally{setBusy(false)}
  }

  return <div className="readerStack">
    <section className="readerGrid">
      <form className="panel form" onSubmit={submit}>
        <h2>1. Birth data</h2>
        <label>Full name<input name="full_name" required/></label>
        <label>Date of birth<input name="date_of_birth" type="date" required/></label>
        <label>Birth time precision<select value={precision} onChange={e=>setPrecision(e.target.value as Precision)}><option value="exact">Exact</option><option value="approximate">Approximate</option><option value="unknown">Unknown</option></select></label>
        {precision!=="unknown"&&<label>Birth time<input name="birth_time" type="time" required/></label>}
        <label>Birthplace<input name="birthplace_label" placeholder="Bhilai, Chhattisgarh, India" required/></label>
        <div className="two"><label>Latitude<input name="latitude" type="number" step="any" required/></label><label>Longitude<input name="longitude" type="number" step="any" required/></label></div>
        <label>Timezone<input name="timezone" defaultValue="Asia/Kolkata" required/></label>
        <button disabled={busy}>{busy?"Calculating…":"Calculate Kundli"}</button>
      </form>
      <article className="panel result">
        <h2>2. Kundli + timing</h2>
        {!chart&&<p>No calculation yet.</p>}
        {chart&&<><h3>Chart evidence</h3><pre>{JSON.stringify(chart,null,2)}</pre></>}
        {dasha&&<><h3>Current Vimshottari</h3><pre>{JSON.stringify(dasha,null,2)}</pre></>}
      </article>
    </section>

    <section className="readerGrid">
      <article className="panel form">
        <h2>3. Question + card spread</h2>
        <label>Question<textarea rows={4} value={question} onChange={e=>setQuestion(e.target.value)} placeholder="What do I need to understand about…?"/></label>
        <label>Spread<select value={spreadKey} onChange={e=>setSpreadKey(e.target.value)}><option value="single">Single Card</option><option value="three-path">Three Card Path</option><option value="five-question">Five Card Question</option><option value="nine-mandala">Nine Card Mandala</option></select></label>
        <button type="button" onClick={drawCards}>Draw cards</button>
        {draw&&<pre>{JSON.stringify(draw,null,2)}</pre>}
      </article>
      <article className="panel result">
        <h2>4. Combined reading</h2>
        <p>The AI receives chart/card evidence only. It is not allowed to invent planetary placements or cards.</p>
        <button type="button" disabled={!canInterpret||busy} onClick={interpret}>{busy?"Synthesizing…":"Interpret question"}</button>
        {synthesis&&<pre>{JSON.stringify(synthesis,null,2)}</pre>}
      </article>
    </section>
    {error&&<p className="error panel">{error}</p>}
  </div>
}
