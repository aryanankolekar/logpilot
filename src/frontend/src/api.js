import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:6969",
  timeout: 60000,
});

export async function sendQuery(query) {
  try {
    const res = await api.post("/query", { query });
    return res.data;
  } catch (err) {
    console.error("Backend error:", err);
    throw err;
  }
}

export async function uploadFile(file) {
  const formData = new FormData();
  formData.append("file", file);
  const res = await api.post("/ingest/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return res.data;
}
