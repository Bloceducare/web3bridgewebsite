import { defineCliConfig } from "sanity/cli";

export default defineCliConfig({
  api: {
    projectId: "j02dw5x9",
    dataset: "production",
  },
  typegen: {
    enabled: true,
    path: "../frontend_v2/src/**/*.{ts,tsx,js,jsx}",
    schema: "schema.json",
    generates: "../frontend_v2/sanity.types.ts",
    overloadClientMethods: true,
  },
  deployment: {
    autoUpdates: true,
  },
});
