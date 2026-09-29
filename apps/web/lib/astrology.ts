export async function astrologyPost<T>(path:string, body:unknown):Promise<T>{
  const base=process.env.ASTROLOGY_API_URL ?? "http://localhost:8000";
  const response=await fetch(base+path,{method:"POST",headers:{"content-type":"application/json"},body:JSON.stringify(body),cache:"no-store"});
  if(!response.ok){const detail=await response.text();throw new Error(`Astrology API ${response.status}: ${detail}`)}
  return response.json() as Promise<T>;
}
