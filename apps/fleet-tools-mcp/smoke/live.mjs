// Live functional smoke -- imports handlers directly, hits real APIs. Manual run (costs money:
// openai_image ~ $0.04-0.07). Usage: node smoke/live.mjs [tavily|image|gemini|groq|all]
import { tavilySearch, openaiImage, crossCheck } from "../server.mjs";

const which = process.argv[2] || "all";
const run = async (label, p) => {
  const res = await p;
  const text = res.content.map((c) => c.text).join("\n");
  console.log(`\n===== ${label} ${res.isError ? "(isError)" : ""} =====\n${text}`);
  if (res.isError) process.exitCode = 1;
};

if (which === "tavily" || which === "all")
  await run("tavily_search", tavilySearch({ query: "what is the Model Context Protocol", max_results: 3 }));
if (which === "image" || which === "all")
  await run("openai_image", openaiImage({ prompt: "a tiny pixel-art robot mascot, flat colors", size: "1024x1024" }));
if (which === "gemini" || which === "all")
  await run("cross_check/gemini", crossCheck({ model: "gemini-2.5-flash", prompt: "Reply with exactly: FLEET_CROSS_OK" }));
if (which === "groq")
  await run("cross_check/groq", crossCheck({ model: "llama-3.3-70b-versatile", prompt: "Reply with exactly: FLEET_GROQ_OK" }));
