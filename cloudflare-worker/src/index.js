// Fixes a real GitHub Releases limitation: release assets are always served with
// Content-Type: application/octet-stream and Content-Disposition: attachment,
// regardless of what was declared at upload time. Podcast apps (Apple Podcasts
// confirmed) refuse to play an enclosure with that content type, so this proxy
// re-serves the same bytes from GitHub with the headers a podcast app expects.
// The audio itself stays only in GitHub Releases — nothing is duplicated here.
const REPO = "ZhongZheng782/YoutubeAudio.Fetch";
const STEM_RE = /^\/audio\/([A-Za-z0-9_-]+)\.m4a$/;

export default {
  async fetch(request) {
    const url = new URL(request.url);
    const match = url.pathname.match(STEM_RE);
    if (!match) {
      return new Response("Not found", { status: 404 });
    }
    const stem = match[1];
    const originUrl = `https://github.com/${REPO}/releases/download/audio-${stem}/${stem}.m4a`;

    const originHeaders = {};
    const range = request.headers.get("Range");
    if (range) originHeaders["Range"] = range;

    const originResp = await fetch(originUrl, { headers: originHeaders, redirect: "follow" });

    const headers = new Headers(originResp.headers);
    headers.set("Content-Type", "audio/mp4");
    headers.delete("Content-Disposition");
    headers.set("Access-Control-Allow-Origin", "*");

    return new Response(originResp.body, {
      status: originResp.status,
      headers,
    });
  },
};
