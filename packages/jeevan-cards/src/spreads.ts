export interface SpreadPosition{key:string;label:string}
export interface SpreadDefinition{key:string;name:string;positions:readonly SpreadPosition[]}

export const SPREADS:readonly SpreadDefinition[]=[
  {key:"single",name:"Single Card",positions:[{key:"focus",label:"Focus"}]},
  {key:"three-path",name:"Three Card Path",positions:[{key:"root",label:"Root"},{key:"present",label:"Present"},{key:"marga",label:"Way Forward"}]},
  {key:"five-question",name:"Five Card Question",positions:[{key:"situation",label:"Situation"},{key:"hidden",label:"Hidden Factor"},{key:"support",label:"Support"},{key:"challenge",label:"Challenge"},{key:"marga",label:"Way Forward"}]},
  {key:"nine-mandala",name:"Nine Card Mandala",positions:Array.from({length:9},(_,i)=>({key:`p${i+1}`,label:`Position ${i+1}`}))},
] as const;

export function getSpread(key:string){const spread=SPREADS.find(s=>s.key===key);if(!spread)throw new Error(`Unknown spread: ${key}`);return spread}
