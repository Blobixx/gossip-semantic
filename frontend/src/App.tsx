import { useState } from "react";
import { getArticles } from "./api/query";
import { Article } from "./api/types";

export default function App() {
  const [articles, setArticles] = useState<Article[]>([]);
  const [query, setQuery] = useState<string>("");

  const handleOnClick = () => {
    getArticles(query).then(setArticles);
  };

  console.log(articles);

  return (
    <>
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          padding: 20,
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        <h1>Find articles</h1>
        <div
          style={{
            display: "flex",
          }}
        >
          <input value={query} onChange={(e) => setQuery(e.target.value)} />
          <button onClick={handleOnClick}>Search</button>
        </div>
      </div>
      <div style={{ display: "flex", flexDirection: "column" }}>
        {articles.length > 0 &&
          articles.map((i) => (
            <div
              key={i.url}
              style={{
                display: "flex",
                flexDirection: "column",
                gap: 16,
                padding: 8,
              }}
            >
              <span style={{ fontSize: 26 }}>{i.title}</span>
              <span style={{ textJustify: "inter-word" }}>{i.content}</span>
              <span>
                Par <span style={{ fontStyle: "italic" }}>{i.author}</span> — Le{" "}
                <span>{new Date(i.publishedAt).toLocaleDateString()}</span>
              </span>
            </div>
          ))}
      </div>
    </>
  );
}
