import {LEVELS} from "./campaign.js";
runOnStartup(runtime=>runtime.addEventListener("beforeprojectstart",()=>{runtime.globalVars.CampaignJSON=JSON.stringify(LEVELS);}));
