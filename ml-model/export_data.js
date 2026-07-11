import { initializeApp } from "firebase/app";
import { getDatabase, ref, get } from "firebase/database";
import fs from "fs";
import dotenv from "dotenv";

dotenv.config();

const firebaseConfig = {
  apiKey: process.env.VITE_FIREBASE_API_KEY,
  authDomain: process.env.VITE_FIREBASE_AUTH_DOMAIN,
  databaseURL: process.env.VITE_FIREBASE_DATABASE_URL,
  projectId: "smart-irrigation-system1234",
};

const app = initializeApp(firebaseConfig);
const db = getDatabase(app);

const historyRef = ref(db, "/history");
get(historyRef).then((snapshot) => {
  if (snapshot.exists()) {
    const data = snapshot.val();
    fs.writeFileSync("history_data.json", JSON.stringify(data, null, 2));
    console.log("Data exported to history_data.json");
    console.log("Number of entries:", Object.keys(data).length);
  } else {
    console.log("No data found at /history");
  }
});