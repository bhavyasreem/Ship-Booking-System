const API_BASE = "http://127.0.0.1:8000";

// Wait for DOM to load to initialize common widgets
document.addEventListener("DOMContentLoaded", () => {
    renderNavbar();
    setupModals();
});

// Toast notification system
function showToast(message, type = "success") {
    let container = document.querySelector(".toast-container");
    if (!container) {
        container = document.createElement("div");
        container.className = "toast-container";
        document.body.appendChild(container);
    }
    
    const toast = document.createElement("div");
    toast.className = `toast ${type}`;
    
    let icon = "fa-check-circle";
    if (type === "danger") icon = "fa-exclamation-circle";
    if (type === "warning") icon = "fa-exclamation-triangle";
    
    toast.innerHTML = `
        <i class="fas ${icon}"></i>
        <span>${message}</span>
    `;
    
    container.appendChild(toast);
    
    // Animate in
    setTimeout(() => {
        toast.classList.add("show");
    }, 50);
    
    // Remove after duration
    setTimeout(() => {
        toast.classList.remove("show");
        setTimeout(() => {
            toast.remove();
        }, 300);
    }, 4000);
}

// User state helper
function getCurrentUser() {
    const userStr = localStorage.getItem("user");
    if (!userStr) return null;
    try {
        return JSON.parse(userStr);
    } catch (e) {
        return null;
    }
}

function setCurrentUser(user) {
    localStorage.setItem("user", JSON.stringify(user));
}

function logout() {
    localStorage.removeItem("user");
    showToast("Logged out successfully", "success");
    setTimeout(() => {
        window.location.href = "login.html";
    }, 800);
}

// Check authorization and redirect if necessary
function checkAuth(requiredRole = null) {
    const user = getCurrentUser();
    if (!user) {
        showToast("Access denied. Please log in.", "danger");
        setTimeout(() => {
            window.location.href = "login.html";
        }, 1000);
        return false;
    }
    
    if (requiredRole && user.role !== requiredRole) {
        showToast(`Access denied. ${requiredRole} role required.`, "danger");
        setTimeout(() => {
            if (user.role === "admin") {
                window.location.href = "admin_dashboard.html";
            } else if (user.role === "passenger") {
                window.location.href = "passenger_dashboard.html";
            } else {
                // Clear corrupted user state and force login
                localStorage.removeItem("user");
                window.location.href = "login.html";
            }
        }, 1000);
        return false;
    }
    return true;
}

// Unified API Caller (Fetch wrapper)
async function apiCall(endpoint, method = "GET", body = null) {
    const url = `${API_BASE}${endpoint}`;
    const config = {
        method: method,
        headers: {
            "Content-Type": "application/json"
        }
    };
    
    if (body && (method === "POST" || method === "PUT")) {
        config.body = JSON.stringify(body);
    }
    
    try {
        const response = await fetch(url, config);
        if (!response.ok) {
            let errorMsg = `HTTP Error ${response.status}`;
            try {
                const data = await response.json();
                errorMsg = data.error || errorMsg;
            } catch (e) {}
            throw new Error(errorMsg);
        }
        return await response.json();
    } catch (error) {
        console.error(`API Call failed to ${endpoint}:`, error);
        showToast(error.message, "danger");
        throw error;
    }
}

// Dynamically renders the navigation header based on user state
function renderNavbar() {
    const headerEl = document.getElementById("main-header");
    if (!headerEl) return;
    
    const user = getCurrentUser();
    const currentPage = window.location.pathname.split("/").pop();
    
    let navLinks = `
        <a href="index.html" class="nav-link ${currentPage === 'index.html' || currentPage === '' ? 'active' : ''}">Home</a>
        <a href="ships.html" class="nav-link ${currentPage === 'ships.html' ? 'active' : ''}">Explore Ships</a>
    `;
    
    let authArea = "";
    
    if (user) {
        if (user.role === "admin") {
            navLinks += `
                <a href="admin_dashboard.html" class="nav-link ${currentPage === 'admin_dashboard.html' ? 'active' : ''}">Admin Control</a>
            `;
            authArea = `
                <div class="user-profile-nav">
                    <span class="user-avatar" title="Administrator"><i class="fas fa-user-shield"></i></span>
                    <span>Admin</span>
                    <button onclick="logout()" class="btn-nav-logout"><i class="fas fa-sign-out-alt"></i></button>
                </div>
            `;
        } else {
            navLinks += `
                <a href="passenger_dashboard.html" class="nav-link ${currentPage === 'passenger_dashboard.html' ? 'active' : ''}">My Dashboard</a>
                <a href="booking_history.html" class="nav-link ${currentPage === 'booking_history.html' ? 'active' : ''}">Trips History</a>
            `;
            
            const initials = user.full_name ? user.full_name.split(" ").map(n => n[0]).join("").toUpperCase().substring(0, 2) : "P";
            authArea = `
                <div class="user-profile-nav">
                    <span class="user-avatar">${initials}</span>
                    <span>${user.full_name}</span>
                    <button onclick="logout()" class="btn-nav-logout"><i class="fas fa-sign-out-alt"></i></button>
                </div>
            `;
        }
    } else {
        authArea = `
            <a href="login.html" class="btn-nav-login">Sign In</a>
            <a href="register.html" class="nav-link" style="margin-left: 0.5rem;">Register</a>
        `;
    }
    
    headerEl.innerHTML = `
        <div class="logo">
            <i class="fas fa-ship"></i>
            <span>Nautica Cruise</span>
        </div>
        <nav>
            ${navLinks}
        </nav>
        <div style="display: flex; align-items: center; gap: 1rem;">
            ${authArea}
        </div>
    `;
}

// Modal handling logic
function setupModals() {
    // Close modal when clicking close button or background overlay
    document.querySelectorAll(".modal-overlay").forEach(overlay => {
        overlay.addEventListener("click", (e) => {
            if (e.target === overlay || e.target.classList.contains("modal-close") || e.target.closest(".modal-close")) {
                closeModal(overlay.id);
            }
        });
    });
}

function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add("active");
        document.body.style.overflow = "hidden";
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove("active");
        document.body.style.overflow = "";
    }
}

// Date formatter helper
function formatDate(dateStr) {
    if (!dateStr) return "N/A";
    const date = new Date(dateStr);
    if (isNaN(date.getTime())) return dateStr;
    return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(amount);
}
