/* =============================================================================
   StoneBuild Games — game list
   Add a new game by copying the TEMPLATE object below into the GAMES array.
   Everything on /games/ and the home page "Games" section is generated from this.
   -----------------------------------------------------------------------------
   Fields:
     id          short slug, letters/numbers/dashes only (used as element id)
     title       display name
     tagline     one short line shown on the cover
     description 1–2 sentences for the card
     genre       e.g. "Puzzle", "Action RPG", "Hyper-casual"
     platforms   array: "Android", "iOS", "PC", "Web"
     status      "live" | "coming-soon" | "in-production"
     theme       cover art theme when no image: "forge" | "steel" | "ember" | "moss" | "violet"
     cover       optional path to an image (recommended 1600×1000 WebP/PNG) e.g. "/assets/games/my-game.webp"
     playStore   Google Play URL or "" if not live yet
     appStore    App Store URL or ""
     steam       Steam URL or ""
     released    "YYYY-MM-DD" or "" (used in structured data)
   ========================================================================== */

/* TEMPLATE — copy, paste into GAMES, and fill in:
  {
    id: "my-game",
    title: "My Game",
    tagline: "A one-line hook for the cover",
    description: "What the game is and why it is fun, in one or two sentences.",
    genre: "Puzzle",
    platforms: ["Android", "iOS"],
    status: "live",
    theme: "steel",
    cover: "",
    playStore: "https://play.google.com/store/apps/details?id=com.stonebuildgames.mygame",
    appStore: "",
    steam: "",
    released: "2026-12-01"
  },
*/

window.STONEBUILD_GAMES = [
  {
    id: "first-title",
    title: "Our first title",
    tagline: "Currently in production",
    description: "We are building our first game right now. Screenshots, a trailer and store links will appear here the day it goes live on Google Play.",
    genre: "To be announced",
    platforms: ["Android"],
    status: "in-production",
    theme: "forge",
    cover: "",
    playStore: "",
    appStore: "",
    steam: "",
    released: ""
  }
];
