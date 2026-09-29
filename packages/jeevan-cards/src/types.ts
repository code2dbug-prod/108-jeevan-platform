export type CardStatus="DRAFT"|"RESEARCHED"|"REVIEWED"|"APPROVED"|"LOCKED"|"RETIRED";
export interface JeevanCard { id:number; suit:"DHARMA"|"KARMA"|"CHETANA"|"VEDANA"; navaka:string; title:string; transliteration?:string; core:string; prakasha:string; chhaya:string; marga:string; keywords:string[]; status:CardStatus; }
