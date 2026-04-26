window.addEventListener('DOMContentLoaded', (event) => {
    getVisitCount();
});

// ⚠️ CONFIGURATION:
// 1. For LOCAL TESTING: Uncomment the localApiUrl line below and comment out productionApiUrl.
// 2. For PRODUCTION: Uncomment the productionApiUrl line and fill in your Azure Function URL.

// --- LOCAL TESTING (Uncomment this line for local dev) ---
// const apiUrl = 'http://localhost:7071/api/get_visitor_count';

// --- PRODUCTION (Uncomment this line and fill URL for deploy) ---
const apiUrl = 'https://funccountcv01.azurewebsites.net/api/main';

const getVisitCount = async () => {
    const countElement = document.getElementById("counter");
    
    // Show loading state immediately
    if (countElement) {
        countElement.innerText = "Loading...";
    }

    try {
        // Check if URL is empty (common mistake)
        if (!apiUrl || apiUrl === '') {
            throw new Error("API URL is not configured. Check main.js!");
        }

        const response = await fetch(apiUrl);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        
        console.log("Website called function API successfully.");
        
        // Update the counter
        if (countElement && data.count !== undefined) {
            countElement.innerText = data.count;
        } else {
            console.warn("Count data missing or element not found.");
            if (countElement) countElement.innerText = "Error";
        }

    } catch (error) {
        console.error("Error fetching visit count:", error);
        if (countElement) {
            countElement.innerText = "0"; // Fallback
        }
    }
};