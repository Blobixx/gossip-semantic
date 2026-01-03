import { Article } from "./types";

export const articleReader = (json: any): Article => {
  return {
    description: json.description,
    content: json.content,
    title: json.title,
    url: json.url,
    publishedAt: json.published_at,
    author: json.author,
  };
};

export const articlesReader = (json: any): Article[] => {
  return json.map(articleReader);
};
