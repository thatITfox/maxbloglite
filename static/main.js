// global stuff
const headerTitle = document.getElementById("main-header-title");
const orientationQuery = window.matchMedia("(orientation: portrait)");

function handleOrientationChange(e) {
    if (e.matches) {
        // Portrait mode
        headerTitle.innerText = "MTCF";
    } else {
        // Landscape mode
        headerTitle.innerText = "Max The Computer Fox";
    }
}

// Run once on load
handleOrientationChange(orientationQuery);
// Listen for changes
orientationQuery.addEventListener("change", handleOrientationChange);
