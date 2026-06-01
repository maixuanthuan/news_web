const APP_CONFIG = {

    siteName: "Điều Cần Biết",

    siteDescription:
        "Cập nhật nhanh các thông tin quan trọng dành cho người dân địa phương",

    trustLabel:
        "Thông tin đã được xác thực · Minh bạch · Chính thống",

    /**
     * FLAG CHÍNH:
     *   true  → dùng MOCK_NEWS từ data.js (hiện tại)
     *   false → gọi API thật tại apiEndpoint (production)
     */
    useMockData: false,

    apiEndpoint: "/api/news",

    categories: [
        { id: "doi-song",  label: "Đời sống"  },
        { id: "an-ninh",   label: "An ninh"   },
        { id: "hoc-tap",   label: "Học tập"   },
        { id: "suc-khoe",  label: "Sức khỏe"  },
        { id: "giao-thong",label: "Giao thông" },
        { id: "thoi-tiet", label: "Thời tiết" }
    ]
};