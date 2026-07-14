export interface CropKnowledge {
  id: string;
  moistureRange: string;
  commonProblems: string;
  wateringTips: string;
}

export const CROP_KNOWLEDGE: CropKnowledge[] = [
  {
    id: "wheat",
    moistureRange: "Ideal moisture range: 35–50%. Wheat is a low-water-need crop; overwatering above 50% risks root rot and fungal disease.",
    commonProblems: "Rust (orange-brown leaf spots) in humid conditions; aphids in early growth stages; waterlogging if drainage is poor.",
    wateringTips: "Reduce watering frequency during grain-filling stage to avoid lodging. Critical windows are crown root initiation and flowering.",
  },
  {
    id: "rice",
    moistureRange: "Ideal moisture range: 65–85%. Rice tolerates standing water far better than most crops; moisture below 60% for extended periods significantly stresses the plant.",
    commonProblems: "Blast disease (grayish leaf lesions) in humid, poorly-drained conditions; stem borer pests; nutrient deficiency if fields are flooded too long.",
    wateringTips: "Maintain standing water during tillering and flowering stages. Brief drying periods between floods can reduce disease risk.",
  },
  {
    id: "barley",
    moistureRange: "Ideal moisture range: 30–45%. Barley is drought-tolerant, similar to wheat but slightly lower water need; excess moisture above 45% increases lodging risk.",
    commonProblems: "Powdery mildew in humid conditions; net blotch on leaves.",
    wateringTips: "Water is most critical during tillering and early stem elongation; reduce watering as grain matures.",
  },
  {
    id: "sugarcane",
    moistureRange: "Ideal moisture range: 55–75%. Sugarcane is a high-water-need crop with a long growth cycle, requiring consistent moisture especially during the grand growth phase.",
    commonProblems: "Red rot disease in waterlogged conditions; stalk borer pests.",
    wateringTips: "Reduce irrigation frequency approaching harvest to improve sugar content. Consistent moisture is most critical 3–8 months after planting.",
  },
  {
    id: "cotton",
    moistureRange: "Ideal moisture range: 40–55%. Cotton is moderately drought-tolerant once established, but sensitive to both under- and over-watering during flowering and boll formation.",
    commonProblems: "Bollworm infestation is the most significant pest risk; root rot in waterlogged soil; leaf reddening under prolonged moisture stress.",
    wateringTips: "Reduce watering as bolls mature and open — excess moisture can cause boll rot.",
  },
  {
    id: "maize",
    moistureRange: "Ideal moisture range: 45–60%. Maize has moderate water needs but is highly sensitive to moisture stress during tasseling and silking stages.",
    commonProblems: "Stalk rot in waterlogged soil; fall armyworm pests.",
    wateringTips: "Prioritize consistent moisture during flowering; reduce watering during grain-filling to avoid stalk rot.",
  },
  {
    id: "tomato",
    moistureRange: "Ideal moisture range: 50–65%. Tomato needs consistent, even moisture; irregular watering commonly causes blossom-end rot and fruit cracking.",
    commonProblems: "Early blight (dark leaf spots); root rot in waterlogged soil.",
    wateringTips: "Maintain steady moisture rather than heavy infrequent watering, especially once fruit begins forming.",
  },
  {
    id: "onion",
    moistureRange: "Ideal moisture range: 40–55%. Onion has shallow roots and needs frequent, light watering rather than deep infrequent watering.",
    commonProblems: "Purple blotch (fungal leaf disease); bulb rot in poorly-drained soil.",
    wateringTips: "Reduce watering 2–3 weeks before harvest to help bulbs cure properly.",
  },
  {
    id: "soybean",
    moistureRange: "Ideal moisture range: 45–60%. Soybean water needs peak during flowering and pod-filling stages.",
    commonProblems: "Root rot in waterlogged soil; pod borer pests.",
    wateringTips: "Moisture is most critical during flowering and pod development; earlier vegetative stages tolerate mild drought stress better.",
  },
];

export function getCropKnowledge(id: string): CropKnowledge | undefined {
  return CROP_KNOWLEDGE.find((c) => c.id === id);
}