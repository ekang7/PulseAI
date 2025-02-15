document.getElementById("scrapeTabs").addEventListener("click", async () => {
    const tabs = await chrome.tabs.query({});
    const tabData = tabs.map(t => ({ url: t.url, title: t.title }));

    fetch("http://localhost:3000/collect", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ tabs: tabData })
    });
});
