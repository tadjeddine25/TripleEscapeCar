import { LEVELS } from "./campaign.js";
// Data loading only. All gameplay and rendering are native Construct events and objects.
runOnStartup(runtime => { runtime.addEventListener("beforeprojectstart", () => { runtime.globalVars.CampaignJSON = JSON.stringify(LEVELS); }); });
