const elements = {
    loginSection: document.querySelector("#login-section"),
    dashboardSection: document.querySelector("#dashboard-section"),
    loginForm: document.querySelector("#login-form"),
    logoutButton: document.querySelector("#logout-button"),

    usernameInput: document.querySelector("#username"),
    passwordInput: document.querySelector("#password"),

    uploadForm: document.querySelector("#upload-form"),
    documentInput: document.querySelector("#document-input"),
    selectedFileName: document.querySelector("#selected-file-name"),
    dropZone: document.querySelector("#drop-zone"),
    uploadButton: document.querySelector("#upload-button"),

    documentsTable: document.querySelector("#documents-table"),
    documentsTableBody: document.querySelector("#documents-table-body"),
    documentCount: document.querySelector("#document-count"),

    loadingState: document.querySelector("#loading-state"),
    emptyState: document.querySelector("#empty-state"),

    refreshButton: document.querySelector("#refresh-button"),
    searchInput: document.querySelector("#search-input"),

    apiStatus: document.querySelector("#api-status"),
    apiStatusDescription: document.querySelector(
        "#api-status-description"
    ),

    toastContainer: document.querySelector("#toast-container"),
};

let documentsState = [];

document.addEventListener("DOMContentLoaded", () => {
    initializeThreeBackground();
    initializeAnimations();
    initializeEvents();
    updateApiStatus();
});

function initializeEvents() {
    elements.loginForm.addEventListener("submit", handleLogin);
    elements.logoutButton.addEventListener("click", handleLogout);
    elements.uploadForm.addEventListener("submit", handleUpload);
    elements.refreshButton.addEventListener("click", loadDocuments);
    elements.searchInput.addEventListener("input", filterDocuments);
    elements.documentInput.addEventListener("change", updateSelectedFile);

    elements.dropZone.addEventListener("dragover", (event) => {
        event.preventDefault();
        elements.dropZone.classList.add("dragging");
    });

    elements.dropZone.addEventListener("dragleave", () => {
        elements.dropZone.classList.remove("dragging");
    });

    elements.dropZone.addEventListener("drop", (event) => {
        event.preventDefault();
        elements.dropZone.classList.remove("dragging");

        const file = event.dataTransfer.files[0];

        if (!file) {
            return;
        }

        const transfer = new DataTransfer();
        transfer.items.add(file);

        elements.documentInput.files = transfer.files;
        updateSelectedFile();
    });
}

async function handleLogin(event) {
    event.preventDefault();

    const username = elements.usernameInput.value.trim();
    const password = elements.passwordInput.value;

    if (!username || !password) {
        showToast("Preencha o usuário e a senha.", "error");
        return;
    }

    const button = elements.loginForm.querySelector("button");
    setButtonLoading(button, true, "Autenticando...");

    try {
        setCredentials(username, password);

        const documents = await authenticateUser();
        documentsState = documents;

        showDashboard();
        renderDocuments(documentsState);
        showToast("Autenticação realizada com sucesso.");

        elements.passwordInput.value = "";
    } catch (error) {
        clearCredentials();

        const message = error.status === 401
            ? "Usuário ou senha inválidos."
            : error.message;

        showToast(message, "error");
    } finally {
        setButtonLoading(button, false, "Entrar");
    }
}

function handleLogout() {
    clearCredentials();
    documentsState = [];

    elements.dashboardSection.hidden = true;
    elements.loginSection.hidden = false;
    elements.logoutButton.hidden = true;
    elements.loginForm.reset();

    gsap.fromTo(
        elements.loginSection,
        { opacity: 0, y: 20 },
        { opacity: 1, y: 0, duration: 0.6 }
    );

    showToast("Sessão encerrada.");
}

async function handleUpload(event) {
    event.preventDefault();

    const file = elements.documentInput.files[0];

    if (!file) {
        showToast("Selecione um documento PDF.", "error");
        return;
    }

    if (
        file.type !== "application/pdf" &&
        !file.name.toLowerCase().endsWith(".pdf")
    ) {
        showToast("O arquivo precisa estar no formato PDF.", "error");
        return;
    }

    setButtonLoading(
        elements.uploadButton,
        true,
        "Enviando documento..."
    );

    try {
        await uploadDocument(file);

        elements.uploadForm.reset();
        elements.selectedFileName.textContent =
            "Nenhum arquivo selecionado";

        showToast("Documento enviado e criptografado com sucesso.");

        await loadDocuments();
    } catch (error) {
        handleApiError(error);
    } finally {
        setButtonLoading(
            elements.uploadButton,
            false,
            "Enviar documento"
        );
    }
}

async function loadDocuments() {
    setDocumentsLoading(true);

    try {
        documentsState = await fetchDocuments();
        renderDocuments(documentsState);
    } catch (error) {
        handleApiError(error);
    } finally {
        setDocumentsLoading(false);
    }
}

function renderDocuments(documents) {
    elements.documentsTableBody.innerHTML = "";
    elements.documentCount.textContent = documentsState.length;

    if (!documents.length) {
        elements.emptyState.hidden = false;
        elements.documentsTable.hidden = true;
        return;
    }

    elements.emptyState.hidden = true;
    elements.documentsTable.hidden = false;

    documents.forEach((documentItem) => {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>
                <div
                    class="document-name"
                    title="${escapeHtml(documentItem.original_name)}"
                >
                    ${escapeHtml(documentItem.original_name)}
                </div>
            </td>

            <td>${formatFileSize(documentItem.size)}</td>

            <td>${formatDate(documentItem.created_at)}</td>

            <td>
                <button
                    type="button"
                    class="download-button"
                    data-id="${documentItem.id}"
                    data-name="${escapeHtml(documentItem.original_name)}"
                >
                    Download
                </button>
            </td>
        `;

        elements.documentsTableBody.appendChild(row);
    });

    document.querySelectorAll(".download-button").forEach((button) => {
        button.addEventListener("click", async () => {
            await handleDownload(
                button.dataset.id,
                button.dataset.name,
                button
            );
        });
    });

    gsap.from("#documents-table-body tr", {
        opacity: 0,
        y: 12,
        duration: 0.35,
        stagger: 0.05,
    });
}

async function handleDownload(documentId, originalName, button) {
    setButtonLoading(button, true, "...");

    try {
        await downloadDocumentById(documentId, originalName);
        showToast("Download iniciado.");
    } catch (error) {
        handleApiError(error);
    } finally {
        setButtonLoading(button, false, "Download");
    }
}

function filterDocuments() {
    const search = elements.searchInput.value
        .trim()
        .toLowerCase();

    const filteredDocuments = documentsState.filter((documentItem) =>
        documentItem.original_name.toLowerCase().includes(search)
    );

    renderDocuments(filteredDocuments);
}

function showDashboard() {
    elements.loginSection.hidden = true;
    elements.dashboardSection.hidden = false;
    elements.logoutButton.hidden = false;

    gsap.fromTo(
        elements.dashboardSection,
        { opacity: 0, y: 25 },
        { opacity: 1, y: 0, duration: 0.7 }
    );

    gsap.from(".stat-card", {
        opacity: 0,
        y: 25,
        duration: 0.6,
        stagger: 0.12,
        delay: 0.15,
    });
}

function updateSelectedFile() {
    const file = elements.documentInput.files[0];

    elements.selectedFileName.textContent = file
        ? file.name
        : "Nenhum arquivo selecionado";
}

async function updateApiStatus() {
    try {
        await checkApiHealth();

        elements.apiStatus.textContent = "Online";
        elements.apiStatus.className = "status-online";
        elements.apiStatusDescription.textContent =
            "serviço disponível";
    } catch {
        elements.apiStatus.textContent = "Offline";
        elements.apiStatus.className = "status-offline";
        elements.apiStatusDescription.textContent =
            "não foi possível conectar";
    }
}

function showToast(message, type = "success") {
    const toast = document.createElement("div");
    toast.className = `toast ${type}`;
    toast.textContent = message;

    elements.toastContainer.appendChild(toast);

    gsap.fromTo(
        toast,
        { opacity: 0, x: 35 },
        { opacity: 1, x: 0, duration: 0.35 }
    );

    setTimeout(() => {
        gsap.to(toast, {
            opacity: 0,
            x: 35,
            duration: 0.3,
            onComplete: () => toast.remove(),
        });
    }, 3500);
}

function setDocumentsLoading(isLoading) {
    elements.loadingState.hidden = !isLoading;

    if (isLoading) {
        elements.documentsTable.hidden = true;
        elements.emptyState.hidden = true;
    }
}

function setButtonLoading(button, isLoading, text) {
    button.disabled = isLoading;
    button.textContent = text;
}

function handleApiError(error) {
    if (error.status === 401) {
        showToast(
            "Sua autenticação não é mais válida.",
            "error"
        );

        handleLogout();
        return;
    }

    showToast(error.message, "error");
}

function formatFileSize(bytes) {
    if (!bytes) {
        return "0 B";
    }

    const units = ["B", "KB", "MB", "GB"];
    const unitIndex = Math.floor(
        Math.log(bytes) / Math.log(1024)
    );

    const value = bytes / Math.pow(1024, unitIndex);

    return `${value.toFixed(unitIndex ? 1 : 0)} ${units[unitIndex]}`;
}

function formatDate(dateValue) {
    return new Intl.DateTimeFormat("pt-BR", {
        dateStyle: "short",
        timeStyle: "short",
    }).format(new Date(dateValue));
}

function escapeHtml(value) {
    const element = document.createElement("div");
    element.textContent = value;
    return element.innerHTML;
}

function initializeAnimations() {
    gsap.from(".topbar", {
        opacity: 0,
        y: -20,
        duration: 0.7,
    });

    gsap.from(".login-card", {
        opacity: 0,
        y: 35,
        scale: 0.97,
        duration: 0.8,
        ease: "power3.out",
    });
}

function initializeThreeBackground() {
    const canvas = document.querySelector("#three-background");

    const scene = new THREE.Scene();

    const camera = new THREE.PerspectiveCamera(
        75,
        window.innerWidth / window.innerHeight,
        0.1,
        1000
    );

    const renderer = new THREE.WebGLRenderer({
        canvas,
        alpha: true,
        antialias: true,
    });

    renderer.setPixelRatio(
        Math.min(window.devicePixelRatio, 2)
    );

    renderer.setSize(
        window.innerWidth,
        window.innerHeight
    );

    const particleCount = window.innerWidth < 700
        ? 450
        : 1000;

    const geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(particleCount * 3);

    for (let index = 0; index < particleCount * 3; index += 3) {
        positions[index] = (Math.random() - 0.5) * 18;
        positions[index + 1] = (Math.random() - 0.5) * 12;
        positions[index + 2] = (Math.random() - 0.5) * 14;
    }

    geometry.setAttribute(
        "position",
        new THREE.BufferAttribute(positions, 3)
    );

    const material = new THREE.PointsMaterial({
        color: 0x39ff14,
        size: 0.025,
        transparent: true,
        opacity: 0.75,
    });

    const particles = new THREE.Points(geometry, material);
    scene.add(particles);

    camera.position.z = 6;

    let mouseX = 0;
    let mouseY = 0;

    window.addEventListener("mousemove", (event) => {
        mouseX = (event.clientX / window.innerWidth - 0.5) * 0.35;
        mouseY = (event.clientY / window.innerHeight - 0.5) * 0.35;
    });

    function animate() {
        requestAnimationFrame(animate);

        particles.rotation.y += 0.0008;
        particles.rotation.x += 0.00025;

        particles.rotation.y += (
            mouseX - particles.rotation.y
        ) * 0.002;

        particles.rotation.x += (
            -mouseY - particles.rotation.x
        ) * 0.002;

        renderer.render(scene, camera);
    }

    animate();

    window.addEventListener("resize", () => {
        camera.aspect =
            window.innerWidth / window.innerHeight;

        camera.updateProjectionMatrix();

        renderer.setSize(
            window.innerWidth,
            window.innerHeight
        );
    });
}