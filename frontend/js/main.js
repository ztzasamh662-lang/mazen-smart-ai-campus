// ===== Role Protection (Admin Only) =====
const role = localStorage.getItem("role")

if(role !== "admin"){
    window.location.href = "login.html"
}


// ===== Fake Data =====
let attendanceData = [
    {id:1, name: "Ahmed", confidence: 0.98, status: "Present", alreadyMarked: true},
    {id:2, name: "Sara", confidence: 0.91, status: "Present", alreadyMarked: true},
    {id:3, name: "Mazen", confidence: 0.87, status: "Present", alreadyMarked: true},
    {id:4, name: "Mona", confidence: 0.95, status: "Present", alreadyMarked: true},
];


// ===== Logout =====
function logout(){
    localStorage.clear()
    window.location.href = "login.html"
}


// ===== Dashboard Counters =====
function animateCounter(id, target) {

    const el = document.getElementById(id);
    if(!el) return;

    let count = 0;
    const increment = target / 100;

    const interval = setInterval(() => {

        count += increment;

        if(count >= target){
            el.textContent = target;
            clearInterval(interval);
        } else {
            el.textContent = Math.floor(count);
        }

    }, 15);
}


// ===== Populate Attendance Table =====
function populateAttendanceTable(filter="all", search="") {

    const tableBody = document.querySelector("#attendance-table tbody");
    if(!tableBody) return;

    tableBody.innerHTML = "";

    attendanceData
        .filter(s => (filter==="all" || s.status.toLowerCase()===filter))
        .filter(s => s.name.toLowerCase().includes(search.toLowerCase()))
        .forEach(student => {

            const row = document.createElement("tr");

            const idCell = document.createElement("td");
            idCell.textContent = student.id;

            const nameCell = document.createElement("td");
            nameCell.textContent = student.name;

            const confCell = document.createElement("td");
            confCell.textContent = `${(student.confidence*100).toFixed(1)}%`;

            const statusCell = document.createElement("td");
            statusCell.textContent = student.status;
            statusCell.className = student.status.toLowerCase();

            const noteCell = document.createElement("td");
            noteCell.textContent = student.alreadyMarked ? "Already Marked" : "";
            noteCell.style.color = student.alreadyMarked ? "#ff5252" : "#00e676";

            row.appendChild(idCell);
            row.appendChild(nameCell);
            row.appendChild(confCell);
            row.appendChild(statusCell);
            row.appendChild(noteCell);

            tableBody.appendChild(row);

        });
}


// ===== Charts =====
function renderCharts() {

    const attendanceCanvas = document.getElementById("attendanceChart");
    const alertsCanvas = document.getElementById("alertsChart");

    if(!attendanceCanvas || !alertsCanvas) return;

    const attendanceCtx = attendanceCanvas.getContext('2d');

    new Chart(attendanceCtx, {

        type: 'pie',

        data: {
            labels: ['Present', 'Absent'],
            datasets: [{
                label: 'Attendance',
                data: [
                    attendanceData.filter(s=>s.status==="Present").length,
                    attendanceData.filter(s=>s.status==="Absent").length
                ],
                backgroundColor: ['#00e676','#ff5252']
            }]
        },

        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'bottom' }
            }
        }

    });


    const alertsCtx = alertsCanvas.getContext('2d');

    new Chart(alertsCtx, {

        type: 'bar',

        data: {
            labels: attendanceData.map(s=>s.name),
            datasets: [{
                label: 'Alerts',
                data: attendanceData.map(()=>Math.floor(Math.random()*3)),
                backgroundColor: '#00bcd4'
            }]
        },

        options: { responsive: true }

    });

}


// ===== Fake Live Detection =====
function simulateLiveDetection(){

    const el = document.getElementById("live-detection");
    if(!el) return;

    const randomStudent = attendanceData[Math.floor(Math.random()*attendanceData.length)];

    el.innerHTML = `
        Face Detected: <b>${randomStudent.name}</b><br>
        Confidence: ${(randomStudent.confidence*100).toFixed(1)}%
    `;
}


// ===== Page Load =====
window.onload = () => {

    animateCounter("total-students", 120);
    animateCounter("present-today", attendanceData.length);
    animateCounter("alerts-count", 2);

    populateAttendanceTable();

    renderCharts();

    // ===== Live Detection Simulation =====
    setInterval(()=>{
        simulateLiveDetection();
    },4000);

}