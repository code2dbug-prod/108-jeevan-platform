import { randomInt } from "node:crypto";
import { cardById, getSpread, JEEVAN_NUMBER_HOOKS, structureForCard } from "@jeevan/cards";

export async function POST(request:Request){
  try{
    const body=await request.json();
    const spread=getSpread(String(body.spreadKey||"single"));
    const selected=new Set<number>();
    while(selected.size<spread.positions.length)selected.add(randomInt(1,109));
    const ids=[...selected];
    return Response.json({
      spread:{key:spread.key,name:spread.name,positions:spread.positions},
      draws:spread.positions.map((position,index)=>{
        const cardId=ids[index];
        const structure=structureForCard(cardId);
        const memoryHook=JEEVAN_NUMBER_HOOKS[structure.jeevanNumber as keyof typeof JEEVAN_NUMBER_HOOKS];
        return {position,index:index+1,cardId,structure,memoryHook,card:cardById(cardId)};
      })
    });
  }catch(error){
    return Response.json({error:error instanceof Error?error.message:"Card draw failed"},{status:400});
  }
}
