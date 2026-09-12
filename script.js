const videoUpload = document.getElementById("videoUpload");

const fileName = document.getElementById("fileName");

const videoPreview = document.getElementById("videoPreview");

const analyzeButton = document.getElementById("analyzeButton");

const loading = document.getElementById("loading");

const results = document.getElementById("results");

const resultImage = document.getElementById("resultImage");

const angleResult = document.getElementById("angleResult");

const timeResult = document.getElementById("timeResult");

const verdict = document.getElementById("verdict");


/* =========================
   VIDEO UPLOAD
========================= */

videoUpload.addEventListener("change", function () {

    const file = this.files[0];

    if (!file) {
        return;
    }

    fileName.textContent = "Selected: " + file.name;

    const videoURL = URL.createObjectURL(file);

    videoPreview.src = videoURL;

    videoPreview.style.display = "block";

    analyzeButton.style.display = "inline-block";

});


/* =========================
   ANALYZE
========================= */

analyzeButton.addEventListener("click", async function () {

    const file = videoUpload.files[0];

    if (!file) {
        alert("Please select a video first.");
        return;
    }

    loading.style.display = "block";

    analyzeButton.disabled = true;

    results.style.display = "none";


    try {

        // Prepare the video for uploading
        const formData = new FormData();

        formData.append("file", file);


        // Send video to Member 2's FastAPI backend
        const response = await fetch(
            "http://127.0.0.1:8000/analyze",
            {
                method: "POST",
                body: formData
            }
        );


        // Check whether the backend responded successfully
        if (!response.ok) {
            throw new Error(
                "Backend error: " + response.status
            );
        }


        // Convert backend response into JavaScript object
        const data = await response.json();

        console.log("MohanLean result:", data);


        /* =========================
           DISPLAY ANGLE
        ========================= */

        const angle = Number(data.max_lean_angle);

        angleResult.textContent =
            angle.toFixed(2) + "°";


        /* =========================
           DISPLAY VERDICT
        ========================= */

        verdict.textContent =
            getVerdict(angle);


        /* =========================
           DISPLAY FRAME
        ========================= */

        if (data.max_lean_frame) {
          resultImage.src =
            "http://127.0.0.1:8000/" +
            data.max_lean_frame +
            "?t=" + Date.now();
}


        /* =========================
           DISPLAY RESULT
        ========================= */

        loading.style.display = "none";

        results.style.display = "block";

        analyzeButton.disabled = false;


        results.scrollIntoView({
            behavior: "smooth"
        });

    }

    catch (error) {

        console.error("MohanLean error:", error);

        loading.style.display = "none";

        analyzeButton.disabled = false;

        alert(
            "Could not connect to the MohanLean backend.\n\n" +
            "Make sure Member 2's FastAPI server is running."
        );

    }

}); 
/* =========================
   LEAN VERDICT
========================= */

function getVerdict(angle) {

    if (angle < 2) {
        return "Standing normally";
    }

    if (angle < 3) {
        return "Mild Lean";
    }

    if (angle < 4) {
        return "Respectable Lean";
    }

    if (angle < 5) {
        return "Serious Lean";
    }

    if (angle < 7) {
        return "MASSIVE LEAN";
    }

    return "ABSOLUTE AYYAPPAA";
}
const danceVideo = document.getElementById("danceVideo");

let targetTime = 0;
let currentTime = 0;

const scrollSpeed = 0.003;

window.addEventListener("scroll", () => {
    const scrollPosition = window.scrollY;

    targetTime = scrollPosition * scrollSpeed;

    if (danceVideo.duration) {
        targetTime = Math.max(
            0,
            Math.min(targetTime, danceVideo.duration)
        );
    }
});

function updateVideo() {

    if (danceVideo.readyState >= 2) {

        // Smoothly move toward the scroll-controlled position
        currentTime += (targetTime - currentTime) * 0.15;

        danceVideo.currentTime = currentTime;
    }

    requestAnimationFrame(updateVideo);
}

danceVideo.addEventListener("loadedmetadata", () => {
    targetTime = 0;
    currentTime = 0;
    danceVideo.currentTime = 0;

    updateVideo();
});