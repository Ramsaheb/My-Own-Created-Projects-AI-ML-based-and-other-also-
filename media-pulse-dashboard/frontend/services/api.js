const BASE_URL = (process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:5000").replace(/\/+$/, ''); // remove trailing slash

// Log to debug
console.log("Using backend BASE_URL:", BASE_URL);

export const fetchArticles = async (query) => {
  try {
    const url = `${BASE_URL}/api/articles?query=${encodeURIComponent(query)}`;
    console.log("Fetching articles from:", url);

    const res = await fetch(url);
    if (!res.ok) {
      throw new Error(`API error: ${res.status} ${res.statusText}`);
    }
    const data = await res.json();
    if (data.status === "success") {
      return data.data;
    } else {
      throw new Error(data.message || "Unknown API error");
    }
  } catch (error) {
    console.error("fetchArticles error:", error);
    throw error;
  }
};

export const analyzeSentiment = async (text) => {
  try {
    const url = `${BASE_URL}/api/analyze`;
    console.log("Analyzing sentiment via:", url);

    const res = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ text })
    });

    if (!res.ok) {
      throw new Error(`API error: ${res.status} ${res.statusText}`);
    }
    const data = await res.json();
    if (data.status === "success") {
      return data.data;
    } else {
      throw new Error(data.message || "Unknown API error");
    }
  } catch (error) {
    console.error("analyzeSentiment error:", error);
    return { error: error.message };
  }
};
