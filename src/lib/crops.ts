import wheatImg from "@/assets/crop-wheat.png";
import riceImg from "@/assets/crop-rice.png";
import barleyImg from "@/assets/crop-barley.png";
import sugarcaneImg from "@/assets/crop-sugarcane.png";
import cottonImg from "@/assets/crop-cotton.png";
import maizeImg from "@/assets/crop-maize.png";
import tomatoImg from "@/assets/crop-tomato.png";
import onionImg from "@/assets/crop-onion.png";
import soybeanImg from "@/assets/crop-soybean.png";

export interface CropInfo {
  id: string;
  nameKey: string;
  image: string;
  threshold: number; // moisture threshold percentage
}

export const CROPS: CropInfo[] = [
  { id: "wheat", nameKey: "crop.wheat", image: wheatImg, threshold: 40 },
  { id: "rice", nameKey: "crop.rice", image: riceImg, threshold: 70 },
  { id: "barley", nameKey: "crop.barley", image: barleyImg, threshold: 35 },
  { id: "sugarcane", nameKey: "crop.sugarcane", image: sugarcaneImg, threshold: 60 },
  { id: "cotton", nameKey: "crop.cotton", image: cottonImg, threshold: 45 },
  { id: "maize", nameKey: "crop.maize", image: maizeImg, threshold: 50 },
  { id: "tomato", nameKey: "crop.tomato", image: tomatoImg, threshold: 55 },
  { id: "onion", nameKey: "crop.onion", image: onionImg, threshold: 45 },
  { id: "soybean", nameKey: "crop.soybean", image: soybeanImg, threshold: 50 },
];

export function getCropById(id: string): CropInfo | undefined {
  return CROPS.find((c) => c.id === id);
}
