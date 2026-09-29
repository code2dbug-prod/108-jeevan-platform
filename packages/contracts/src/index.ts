import { z } from "zod";
export const birthPrecisionSchema=z.enum(["exact","approximate","unknown"]);
export const birthDataSchema=z.object({fullName:z.string().min(1),dateOfBirth:z.string().date(),birthTime:z.string().regex(/^([01]\d|2[0-3]):[0-5]\d$/).nullable(),birthTimePrecision:birthPrecisionSchema,birthplaceLabel:z.string().min(1),latitude:z.number().gte(-90).lte(90),longitude:z.number().gte(-180).lte(180),timezone:z.string().min(1)});
export type BirthData=z.infer<typeof birthDataSchema>;
export const grahaSchema=z.object({key:z.enum(["sun","moon","mars","mercury","jupiter","venus","saturn","rahu","ketu"]),longitude:z.number().gte(0).lt(360),rashi:z.number().int().gte(1).lte(12),degreeInRashi:z.number().gte(0).lt(30),nakshatra:z.string(),pada:z.number().int().gte(1).lte(4),retrograde:z.boolean().default(false)});
export const chartResponseSchema=z.object({calculationVersion:z.string(),ayanamsa:z.literal("lahiri"),houseSystem:z.literal("whole-sign"),birthTimeReliability:z.enum(["exact","approximate","unknown"]),ascendant:z.object({longitude:z.number(),rashi:z.number().int().gte(1).lte(12)}).nullable(),grahas:z.array(grahaSchema),warnings:z.array(z.string())});
export type ChartResponse=z.infer<typeof chartResponseSchema>;
