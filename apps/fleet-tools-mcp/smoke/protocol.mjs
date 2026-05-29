// Keyless protocol smoke: spawn the server over stdio, list tools, assert the 3 names.
// Verifies OUTPUT (not just exit code) per L-038.
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const transport = new StdioClientTransport({ command: "node", args: [join(here, "..", "server.mjs")] });
const client = new Client({ name: "protocol-smoke", version: "0.0.0" }, { capabilities: {} });

await client.connect(transport);
const { tools } = await client.listTools();
const names = tools.map((t) => t.name).sort();
console.log("tools listed:", names.join(", "));
await client.close();

const expected = ["cross_check", "openai_image", "tavily_search"];
if (JSON.stringify(names) !== JSON.stringify(expected)) {
  console.error("FAIL: expected", expected.join(", "));
  process.exit(1);
}
console.log("PROTOCOL SMOKE PASS");
