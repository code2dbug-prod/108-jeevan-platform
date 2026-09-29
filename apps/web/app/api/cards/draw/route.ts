import { randomInt } from "node:crypto";
import { getSpread, structureForCard } from "@jeevan/cards";

export async function POST(request:Request){
  const body=await request.json();
  const spread=getSpread(String(body.spreadKey||"single"));
  const selected=new Set<number>();
  while(selected.size<spread.positions.length)selected.add(randomInt(1,109));
  const ids=[...selected];
  return Response.json({
    spread:spread.key,
    draws:spread.positions.map((position,index)=>({position,index:index+1,cardId:ids[index],structure:structureForCard(ids[index])}))
  });
}
