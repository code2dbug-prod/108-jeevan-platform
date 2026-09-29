export const NAVAKAS=[
  {suit:"DHARMA",navaka:"SVADHARMA",start:1,end:9},
  {suit:"DHARMA",navaka:"SADGUNA",start:10,end:18},
  {suit:"DHARMA",navaka:"MARYADA",start:19,end:27},
  {suit:"KARMA",navaka:"KRIYA",start:28,end:36},
  {suit:"KARMA",navaka:"PHALA",start:37,end:45},
  {suit:"KARMA",navaka:"SAMSKARA",start:46,end:54},
  {suit:"CHETANA",navaka:"MANAS",start:55,end:63},
  {suit:"CHETANA",navaka:"BODHA",start:64,end:72},
  {suit:"CHETANA",navaka:"VIVEKA",start:73,end:81},
  {suit:"VEDANA",navaka:"BHAYA",start:82,end:90},
  {suit:"VEDANA",navaka:"KLESHA",start:91,end:99},
  {suit:"VEDANA",navaka:"VIRAHA",start:100,end:108},
] as const;

export function structureForCard(cardId:number){
  if(!Number.isInteger(cardId)||cardId<1||cardId>108)throw new RangeError("cardId must be 1..108");
  const navaka=NAVAKAS.find(n=>cardId>=n.start&&cardId<=n.end);
  if(!navaka)throw new Error("card structure not found");
  return {...navaka,position:((cardId-1)%9)+1,jeevanNumber:((cardId-1)%9)+1};
}
