let currentPage = 1;

// ✅ Indian phone validation
function isValidIndianPhone(phone) {
    const regex = /^(?:\+91|91)?[6-9]\d{9}$/;
    return regex.test(phone);
}

// 📥 Load Patients
async function loadPatients(page = 1) {
    currentPage = page;

    const res = await fetch(`/patients?page=${page}`);
    const data = await res.json();

    const table = document.getElementById("patientTable");
    table.innerHTML = "";

    data.patients.forEach((p, index) => {
        table.innerHTML += `
            <tr>
                <td>${(currentPage - 1) * 10 + index + 1}</td>
                <td>${p.patient_number}</td>
                <td>${p.name}</td>
                <td>${p.phone || '-'}</td>
                <td>
                    <button class="delete-btn" onclick="deletePatient(${p.id})">
                        Remove
                    </button>
                </td>
            </tr>
        `;
    });

    // Pagination
    const pagination = document.getElementById("pagination");
    pagination.innerHTML = "";

    for (let i = 1; i <= data.total_pages; i++) {
        pagination.innerHTML += `
            <button onclick="loadPatients(${i})">${i}</button>
        `;
    }
}

// ➕ Add Patient
async function addPatient() {
    const patient_number = document.getElementById("patientNumber").value;
    const name = document.getElementById("patientName").value;
    const phone = document.getElementById("phone").value.trim();

    const messageBox = document.getElementById("message");

    if (!patient_number.trim()) {
        messageBox.innerHTML = `<span class="error">Patient number required</span>`;
        return;
    }

    if (!name.trim()) {
        messageBox.innerHTML = `<span class="error">Patient name required</span>`;
        return;
    }

    if (phone && !isValidIndianPhone(phone)) {
        messageBox.innerHTML = `<span class="error">Invalid phone</span>`;
        return;
    }

    const res = await fetch("/add", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ patient_number, name, phone })
    });

    const data = await res.json();
    messageBox.innerHTML = `<span class="success">${data.message}</span>`;

    loadPatients(currentPage);

    // clear
    document.getElementById("patientNumber").value = "";
    document.getElementById("patientName").value = "";
    document.getElementById("phone").value = "";
}

// 🔍 Search
async function searchPatient() {
    const patient_number = document.getElementById("searchInput").value;

    const res = await fetch(`/search?patient_number=${patient_number}`);
    const data = await res.json();

    const resultBox = document.getElementById("searchResult");

    if (data.found) {
        resultBox.innerHTML = `
            <div class="result-box">
                <b>Patient Found:</b><br>
                ID: ${data.patient.id}<br>
                Number: ${data.patient.patient_number}<br>
                Name: ${data.patient.name}<br>
                Phone: ${data.patient.phone || '-'}<br><br>

                <button class="delete-btn" onclick="deletePatientFromSearch(${data.patient.id})">
                    Delete
                </button>
            </div>
        `;
    } else {
        resultBox.innerHTML = `<p class="error">No patient found</p>`;
    }
}

// ❌ Delete
async function deletePatient(id) {
    if (!confirm("Delete this patient?")) return;

    const res = await fetch(`/delete/${id}`, { method: "DELETE" });
    const data = await res.json();

    alert(data.message);
    loadPatients(currentPage);
}

// ❌ Delete from search
async function deletePatientFromSearch(id) {
    if (!confirm("Delete this patient?")) return;

    const res = await fetch(`/delete/${id}`, { method: "DELETE" });
    const data = await res.json();

    document.getElementById("message").innerHTML =
        `<span class="success">${data.message}</span>`;

    document.getElementById("searchResult").innerHTML = "";
    loadPatients(currentPage);
}

// ENTER key support
document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("searchInput").addEventListener("keypress", e => {
        if (e.key === "Enter") searchPatient();
    });

    ["patientNumber", "patientName", "phone"].forEach(id => {
        document.getElementById(id).addEventListener("keypress", e => {
            if (e.key === "Enter") addPatient();
        });
    });

    loadPatients();
});