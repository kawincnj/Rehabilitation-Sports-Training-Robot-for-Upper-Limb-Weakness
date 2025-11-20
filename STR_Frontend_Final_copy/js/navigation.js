// เก็บประวัติหน้าที่เยี่ยมชม
function initPageHistory() {
    const currentPage = location.pathname.split("/").pop();
    let pageHistory = JSON.parse(localStorage.getItem('pageHistory')) || [];
    
    // เพิ่มหน้าปัจจุบันเข้าไปในประวัติ (ไม่ซ้ำกันของหน้าก่อนหน้า)
    if (!pageHistory || pageHistory[pageHistory.length - 1] !== currentPage) {
        pageHistory.push(currentPage);
        localStorage.setItem('pageHistory', JSON.stringify(pageHistory));
    }
}

// เรียกใช้เมื่อเพจโหลด
initPageHistory();

document.addEventListener("DOMContentLoaded", () => {
    const backBtn = document.getElementById("backBtn");
    if (!backBtn) return;

    backBtn.addEventListener("click", () => {
        let pageHistory = JSON.parse(localStorage.getItem('pageHistory')) || [];
        
        // ลบหน้าปัจจุบันออก
        if (pageHistory.length > 0) {
            pageHistory.pop();
        }
        
        // กลับไปหน้าก่อนหน้า หรือกลับไป home
        if (pageHistory.length > 0) {
            const previousPage = pageHistory[pageHistory.length - 1];
            window.location.href = previousPage;
        } else {
            window.location.href = "home.html";
        }
        
        localStorage.setItem('pageHistory', JSON.stringify(pageHistory));
    });
});
