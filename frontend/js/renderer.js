const menuContainer  = document.getElementById("menu-container");
const newsContainer  = document.getElementById("news-container");

let NEWS_DATA = {};

let activeCategory = APP_CONFIG.categories[0].id;


/* ── HEADER ─────────────────────────────────────────────── */

function renderHeader() {

    document.getElementById("site-name").textContent =
        APP_CONFIG.siteName;

    document.getElementById("trust-label").textContent =
        APP_CONFIG.trustLabel;

    document.getElementById("site-description").textContent =
        APP_CONFIG.siteDescription;
}


/* ── MENU ────────────────────────────────────────────────── */

function renderMenu() {

    menuContainer.innerHTML = "";

    APP_CONFIG.categories.forEach(category => {

        const button = document.createElement("button");

        button.className = "menu-btn";

        button.textContent = category.label;

        if (category.id === activeCategory) {
            button.classList.add("active");
        }

        button.onclick = () => {
            activeCategory = category.id;
            renderMenu();
            renderNews();
        };

        menuContainer.appendChild(button);
    });
}


/* ── NEWS ────────────────────────────────────────────────── */

function renderNews() {

    newsContainer.innerHTML = "";

    const newsList = NEWS_DATA[activeCategory] || [];

    if (newsList.length === 0) {

        const empty = document.createElement("div");
        empty.className = "empty-state";
        empty.textContent = "Chưa có dữ liệu cho chuyên mục này.";
        newsContainer.appendChild(empty);
        return;
    }

    newsList.forEach(news => {

        const card = document.createElement("article");
        card.className = "news-card";

        // ── card-image
        const img = document.createElement("div");
        img.className = "card-image";
        if (news.thumbnail) {
        img.style.backgroundImage = `url(${news.thumbnail})`;
        img.style.backgroundSize = "cover";
        img.style.backgroundPosition = "center";
        }

        // ── card-body
        const body = document.createElement("div");
        body.className = "card-body";

        const categoryTag = document.createElement("span");
        categoryTag.className = "card-category";
        categoryTag.textContent = getCategoryLabel(activeCategory);

        const title = document.createElement("h3");
        title.textContent = news.title;   // textContent → không bị XSS

        const desc = document.createElement("p");
        desc.textContent = news.desc;

        const footer = document.createElement("div");
        footer.className = "card-footer";

        const time = document.createElement("span");
        time.textContent = news.time;

        const readBtn = document.createElement("button");
        readBtn.textContent = "Đọc thêm";
        readBtn.onclick = () => openArticle(news.link);

        footer.appendChild(time);
        footer.appendChild(readBtn);

        body.appendChild(categoryTag);
        body.appendChild(title);
        body.appendChild(desc);
        body.appendChild(footer);

        card.appendChild(img);
        card.appendChild(body);

        newsContainer.appendChild(card);
    });
}


/* ── HELPERS ─────────────────────────────────────────────── */

function getCategoryLabel(categoryId) {

    const found = APP_CONFIG.categories.find(c => c.id === categoryId);

    return found ? found.label : "";
}


/* ── ARTICLE DETAIL ──────────────────────────────────────────── */

async function openArticle(url) {

    if (!url) return;

    newsContainer.innerHTML = `<div class="empty-state">Đang tải bài viết...</div>`;

    try {

        const res = await fetch("/api/article", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url })
        });

        const article = await res.json();

        renderArticle(article);

    } catch (err) {

        newsContainer.innerHTML = `<div class="empty-state">Không thể tải bài viết.</div>`;
    }
}


function renderArticle(article) {

    newsContainer.innerHTML = "";
    newsContainer.style.display = "block";

    const wrapper = document.createElement("div");
    wrapper.className = "article-detail";

    const back = document.createElement("button");
    back.className = "back-btn-floating";
    back.textContent = "← Quay lại";
    back.onclick = () => {
    back.remove(); // xóa nút khi quay lại
    newsContainer.style.display = "";
    renderNews();
};
document.body.appendChild(back); // gắn vào body thay vì wrapper
    const title = document.createElement("h1");
    title.className = "article-title";
    title.textContent = article.title;

    const meta = document.createElement("div");
    meta.className = "article-meta";
    meta.textContent = [article.author, article.date].filter(Boolean).join(" · ");

    const lead = document.createElement("p");
    lead.className = "article-lead";
    lead.textContent = article.lead;

    const content = document.createElement("div");
    content.className = "article-content";
    content.innerHTML = article.content;

    wrapper.appendChild(back);
    wrapper.appendChild(title);
    wrapper.appendChild(meta);
    wrapper.appendChild(lead);
    wrapper.appendChild(content);

    // Bài đề xuất
    const relatedTitle = document.createElement("h3");
    relatedTitle.className = "related-title";
    relatedTitle.textContent = "Có thể bạn quan tâm";

    const relatedGrid = document.createElement("div");
    relatedGrid.className = "related-grid";

    const currentList = NEWS_DATA[activeCategory] || [];

    currentList.slice(0, 4).forEach(news => {

        if (!news.link) return;

        const card = document.createElement("div");
        card.className = "related-card";
        card.onclick = () => openArticle(news.link);

        const t = document.createElement("p");
        t.textContent = news.title;

        const time = document.createElement("span");
        time.textContent = news.time;

        card.appendChild(t);
        card.appendChild(time);
        relatedGrid.appendChild(card);
    });

    wrapper.appendChild(relatedTitle);
    wrapper.appendChild(relatedGrid);

    newsContainer.appendChild(wrapper);


}