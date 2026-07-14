export interface CropKnowledge {
  id: string;
  moistureRange: string;
  commonProblems: string;
  wateringTips: string;
}

export const CROP_KNOWLEDGE: CropKnowledge[] = [
  {
    id: "wheat",
    moistureRange:
      "Ideal moisture range: 35–50%. Wheat is a low-water-need crop compared to rice or sugarcane; overwatering above 50% risks root rot and fungal disease.",
    commonProblems:
      "Rust (orange-brown leaf spots) in humid conditions; aphids in early growth stages; waterlogging if drainage is poor.",
    wateringTips:
      "Reduce watering frequency during grain-filling stage to avoid lodging. Critical watering windows are crown root initiation and flowering stages.",
  },
  {
    id: "rice",
    moistureRange:
      "Ideal moisture range: 65–85%. Rice tolerates standing water far better than most crops; moisture below 60% for extended periods significantly stresses the plant.",
    commonProblems:
      "Blast disease (grayish leaf lesions) in humid, poorly-drained conditions; stem borer pests; nutrient deficiency if fields are flooded too long without drying.",
    wateringTips:
      "Maintain standing water during tillering and flowering stages. Brief drying periods between floods can reduce disease risk without harming yield.",
  },
  {
    id: "cotton",
    moistureRange:
      "Ideal moisture range: 40–55%. Cotton is moderately drought-tolerant once established, but sensitive to both under- and over-watering during flowering and boll formation.",
    commonProblems:
      "Bollworm infestation is the most significant pest risk; root rot in waterlogged soil; leaf reddening under prolonged moisture stress.",
    wateringTips:
      "Reduce watering as bolls mature and open — excess moisture can cause boll rot. Earlier growth stages need more consistent moisture than late-stage.",
  },
];

export function getCropKnowledge(id: string): CropKnowledge | undefined {
  return CROP_KNOWLEDGE.find((c) => c.id === id);
}