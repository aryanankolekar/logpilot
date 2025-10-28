import axios from "axios";

const API_BASE = "http://localhost:6969";

export async function sendQuery(query) {
  try {
    const response = await axios.post(
      `${API_BASE}/query`,
      { query },
      { timeout: 180000 } // 3 min timeout for slow LLMs
    );
    return response.data;
  } catch (error) {
    console.error("Error querying backend:", error);
    return {
      answer: "⚠️ Server took too long to respond or failed.",
      evidence: [],
    };
  }
}
