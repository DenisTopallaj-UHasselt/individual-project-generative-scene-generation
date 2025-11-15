// DOM Elements
const form = document.getElementById("uploadForm");
const videoFile = document.getElementById("videoFile");
const fileInfo = document.getElementById("fileInfo");
const fileText = document.querySelector(".file-text");
const submitBtn = document.getElementById("submitBtn");
const status = document.getElementById("status");
const progressContainer = document.getElementById("progressContainer");
const progressFill = document.getElementById("progressFill");
const progressText = document.getElementById("progressText");

// File selection handler
videoFile.addEventListener("change", (e) => {
	const file = e.target.files[0];
	if (file) {
		const sizeMB = (file.size / (1024 * 1024)).toFixed(2);
		fileText.textContent = file.name;
		fileInfo.textContent = `📄 ${file.name} (${sizeMB} MB)`;
		fileInfo.classList.add("active");
	} else {
		fileText.textContent = "Choose video file...";
		fileInfo.classList.remove("active");
	}
});

// Show status message
function showStatus(message, type) {
	status.textContent = message;
	status.className = `status ${type} active`;
}

// Hide status message
function hideStatus() {
	status.classList.remove("active");
}

// Show progress
function showProgress(text = "Processing...") {
	progressContainer.style.display = "block";
	progressFill.style.width = "100%";
	progressText.textContent = text;
}

// Hide progress
function hideProgress() {
	progressContainer.style.display = "none";
	progressFill.style.width = "0%";
}

// Set button loading state
function setButtonLoading(loading) {
	submitBtn.disabled = loading;
	const btnIcon = submitBtn.querySelector(".btn-icon");
	const btnText = submitBtn.querySelector(".btn-text");

	if (loading) {
		btnIcon.innerHTML = '<span class="spinner"></span>';
		btnText.textContent = "Processing...";
	} else {
		btnIcon.textContent = "▶";
		btnText.textContent = "Process Video";
	}
}

// Download blob as file
function downloadBlob(blob, filename) {
	const url = window.URL.createObjectURL(blob);
	const a = document.createElement("a");
	a.href = url;
	a.download = filename;
	document.body.appendChild(a);
	a.click();
	window.URL.revokeObjectURL(url);
	document.body.removeChild(a);
}

// Format file size
function formatBytes(bytes, decimals = 2) {
	if (bytes === 0) return "0 Bytes";
	const k = 1024;
	const dm = decimals < 0 ? 0 : decimals;
	const sizes = ["Bytes", "KB", "MB", "GB"];
	const i = Math.floor(Math.log(bytes) / Math.log(k));
	return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + " " + sizes[i];
}

// Form submission handler
form.addEventListener("submit", async (e) => {
	e.preventDefault();

	const file = videoFile.files[0];
	const fps = document.getElementById("fps").value;

	// Validation
	if (!file) {
		showStatus("❌ Please select a video file", "error");
		return;
	}

	if (fps < 1 || fps > 120) {
		showStatus("❌ FPS must be between 1 and 120", "error");
		return;
	}

	// Prepare form data
	const formData = new FormData();
	formData.append("video", file);
	formData.append("fps", fps);

	// UI updates
	setButtonLoading(true);
	hideStatus();
	showProgress("Uploading video...");

	try {
		// Send request
		const response = await fetch("/api/process", {
			method: "POST",
			body: formData,
		});

		if (!response.ok) {
			const error = await response.json();
			throw new Error(error.detail || "Processing failed");
		}

		// Update progress
		progressText.textContent = "Processing complete! Preparing download...";

		// Get the blob
		const blob = await response.blob();
		const fileSize = formatBytes(blob.size);

		// Download file
		downloadBlob(blob, "colmap_project.zip");

		// Success message
		showStatus(
			`✅ Processing complete! Downloaded colmap_project.zip (${fileSize})`,
			"success",
		);
		hideProgress();
	} catch (error) {
		console.error("Processing error:", error);
		showStatus(`❌ Error: ${error.message}`, "error");
		hideProgress();
	} finally {
		setButtonLoading(false);
	}
});

// Check API status on load
async function checkStatus() {
	try {
		const response = await fetch("/api/status");
		const data = await response.json();

		if (!data.pipeline_available) {
			showStatus(
				"⚠️ Warning: Pipeline script not found. Processing may fail.",
				"error",
			);
		}
	} catch (error) {
		console.error("Status check failed:", error);
	}
}

// Initialize
checkStatus();
