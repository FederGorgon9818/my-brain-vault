import urllib.request

urls = {
    "paper1_4416622": "https://r.jina.ai/https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4416622",
    "paper2_6745958": "https://r.jina.ai/https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6745958",
}

for name, url in urls.items():
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=60) as r:
            txt = r.read().decode("utf-8", errors="replace")
        with open(f"{name}.md", "w") as f:
            f.write(txt)
        print(f"=== {name}: {len(txt)} chars ===")
        print(txt[:1500])
        print("\n\n")
    except Exception as e:
        print(f"{name} FAILED: {e}")