"use client";
import { FormEvent, useState } from "react";

type Precision="exact"|"approximate"|"unknown";

export function BirthProfileForm(){
  const [precision,setPrecision]=useState<Precision>("exact");
  const [message,setMessage]=useState("");
  const [busy,setBusy]=useState(false);
  async function submit(e:FormEvent<HTMLFormElement>){
    e.preventDefault();setBusy(true);setMessage("");
    const f=new FormData(e.currentTarget);
    const body={
      subject_name:String(f.get("subject_name")||""),
      date_of_birth:String(f.get("date_of_birth")||""),
      birth_time:precision==="unknown"?null:String(f.get("birth_time")||""),
      birth_time_precision:precision,
      birthplace_label:String(f.get("birthplace_label")||""),
      latitude:Number(f.get("latitude")),
      longitude:Number(f.get("longitude")),
      timezone:String(f.get("timezone")||"Asia/Kolkata"),
      gender:String(f.get("gender")||"")||null,
      current_city:String(f.get("current_city")||"")||null,
      relationship_status:String(f.get("relationship_status")||"")||null,
      phone:String(f.get("phone")||"")||null,
    };
    try{
      const r=await fetch("/api/birth-profiles",{method:"POST",headers:{"content-type":"application/json"},body:JSON.stringify(body)});
      const j=await r.json();
      if(!r.ok)throw new Error(j.error||"Could not save profile");
      setMessage("Birth profile saved. Refresh this page to see it in the list.");
      e.currentTarget.reset();
    }catch(err){setMessage(err instanceof Error?err.message:"Could not save profile")}
    finally{setBusy(false)}
  }
  return <form className="form" onSubmit={submit}>
    <label>Person's full name<input name="subject_name" required/></label>
    <label>Date of birth<input name="date_of_birth" type="date" required/></label>
    <label>Birth-time knowledge<select value={precision} onChange={e=>setPrecision(e.target.value as Precision)}><option value="exact">Exact</option><option value="approximate">Approximate</option><option value="unknown">Unknown</option></select></label>
    {precision!=="unknown"&&<label>Birth time<input name="birth_time" type="time" required/></label>}
    <label>Birthplace<input name="birthplace_label" required/></label>
    <div className="two"><label>Latitude<input name="latitude" type="number" step="any" required/></label><label>Longitude<input name="longitude" type="number" step="any" required/></label></div>
    <label>Timezone<input name="timezone" defaultValue="Asia/Kolkata" required/></label>
    <div className="two"><label>Gender (optional)<input name="gender"/></label><label>Current city (optional)<input name="current_city"/></label></div>
    <div className="two"><label>Relationship status (optional)<input name="relationship_status"/></label><label>Phone (optional)<input name="phone"/></label></div>
    <button disabled={busy}>{busy?"Saving…":"Save birth profile"}</button>
    {message&&<p>{message}</p>}
  </form>
}
