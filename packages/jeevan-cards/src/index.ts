export const SUITS=[{key:"DHARMA",name:"DHARMA / धर्म",navakas:["SVADHARMA","SADGUNA","MARYADA"]},{key:"KARMA",name:"KARMA / कर्म",navakas:["KRIYA","PHALA","SAMSKARA"]},{key:"CHETANA",name:"CHETANA / चेतना",navakas:["MANAS","BODHA","VIVEKA"]},{key:"VEDANA",name:"VEDANA / वेदना",navakas:["BHAYA","KLESHA","VIRAHA"]}] as const;
export type SuitKey=typeof SUITS[number]["key"];
export * from "./types";
export * from "./structure";
export * from "./spreads";
export * from "./catalog";
export * from "./memory";
