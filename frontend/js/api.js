const API_BASE_URL = "";

const apiState = {
    username: "",
    password: "",
};

function setCredentials(username, password) {
    apiState.username = username;
    apiState.password = password;
}

function clearCredentials() {
    apiState.username = "";
    apiState.password = "";
}

function getAuthorizationHeader() {
    const credentials = `${apiState.username}:${apiState.password}`;
    const encodedCredentials = btoa(credentials);

    return `Basic ${encodedCredentials}`;
}

async function apiRequest(endpoint, options = {}) {
    const headers = new Headers(options.headers || {});

    if (apiState.username && apiState.password) {
        headers.set("Authorization", getAuthorizationHeader());
    }

    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers,
    });

    if (!response.ok) {
        let message = "Não foi possível concluir a operação.";

        try {
            const errorData = await response.json();

            if (errorData.detail) {
                message = errorData.detail;
            }
        } catch {
            message = `Erro HTTP ${response.status}`;
        }

        const error = new Error(message);
        error.status = response.status;

        throw error;
    }

    return response;
}

async function checkApiHealth() {
    const response = await fetch(`${API_BASE_URL}/health`);

    if (!response.ok) {
        throw new Error("API indisponível.");
    }

    return response.json();
}

async function authenticateUser() {
    const response = await apiRequest("/documents");
    return response.json();
}

async function fetchDocuments() {
    const response = await apiRequest("/documents");
    return response.json();
}

async function uploadDocument(file) {
    const formData = new FormData();
    formData.append("file", file);

    const response = await apiRequest("/documents", {
        method: "POST",
        body: formData,
    });

    return response.json();
}

async function downloadDocumentById(documentId, originalName) {
    const response = await apiRequest(
        `/documents/${documentId}/download`
    );

    const blob = await response.blob();
    const fileUrl = URL.createObjectURL(blob);

    const temporaryLink = document.createElement("a");
    temporaryLink.href = fileUrl;
    temporaryLink.download = originalName;

    document.body.appendChild(temporaryLink);
    temporaryLink.click();
    temporaryLink.remove();

    URL.revokeObjectURL(fileUrl);
}