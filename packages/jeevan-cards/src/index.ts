export const SUITS=[{key:"DHARMA",name:"DHARMA / धर्म",navakas:["SVADHARMA","SADGUNA","MARYADA"]},{key:"KARMA",name:"KARMA / कर्म",navakas:["KRIYA","PHALA","SAMSKARA"]},{key:"CHETANA",name:"CHETANA / चेतना",navakas:["MANAS","BODHA","VIVEKA"]},{key:"VEDANA",name:"VEDANA / वेदना",navakas:["BHAYA","KLESHA","VIRAHA"]}] as const;
export type SuitKey=typeof SUITS[number]["key"];
export function jeevanNumber(cardId:number):number{if(!Number.isInteger(cardId)||cardId<1||cardId>108)throw new RangeError("cardId must be an integer from 1 to 108");return((cardId-1)%9)+1}
export function navakaPosition(cardId:number):number{return jeevanNumber(cardId)}
export * from "./types";
export * from "./structure";
export * from "./spreads";
