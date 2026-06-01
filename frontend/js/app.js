async function initApp() {

    try {

        if (APP_CONFIG.useMockData) {

            // DEV: dùng mock data từ data.js
            NEWS_DATA = MOCK_NEWS;

        } else {

            // PRODUCTION: chỉ đổi useMockData = false là chạy
            const response = await fetch(APP_CONFIG.apiEndpoint);

            if (!response.ok) {
                throw new Error(`HTTP error: ${response.status}`);
            }

            NEWS_DATA = await response.json();
        }

    } catch (err) {

        console.error("Không thể tải dữ liệu:", err);

        NEWS_DATA = {};
    }

    renderHeader();
    renderMenu();
    renderNews();
}

initApp();