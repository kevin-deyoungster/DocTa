import { MESSAGES } from "./config";
function downloadFile(data, filename) {
    const url = window.URL.createObjectURL(new Blob([data]));
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", filename);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

function isWithinSizeLimits(file, sizeLimit) {
    let size_MB = file.size / 1000000;
    if (size_MB > sizeLimit) {
        alertError(
            `${file.name} exceeds the size limit: ${sizeLimit} megabytes`
        );
        return false;
    } else {
        return true;
    }
}

function alertError(error) {
    error = error.toString().toLowerCase();
    if (error.includes("network")) {
        alert(MESSAGES.SERVER_NOT_AVAILABLE);
    } else if (error.includes("500")) {
        alert(MESSAGES.SERVER_ERROR);
    } else {
        alert(error);
    }
}

const functions = { downloadFile, alertError, isWithinSizeLimits };
export default functions;
