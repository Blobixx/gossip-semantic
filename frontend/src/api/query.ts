import { articlesReader } from "./reader";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export const getArticles = (query: string) => {
  if (!API_BASE_URL) {
    throw new Error("REACT_APP_API_BASE_URL is not defined");
  }
  return fetch(`${API_BASE_URL}/articles/search`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query }),
  })
    .then((response) => response.json())
    .then((data) => articlesReader(data));
};
