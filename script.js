document.addEventListener("DOMContentLoaded", function () {
    console.log("📌 מנסה לטעון את services.txt...");

    // 📌 טעינת שירותים מ- services.txt
    fetch("./services.txt")
        .then(response => {
            console.log(`🔍 תגובת שרת: ${response.status} ${response.statusText}`);
            if (!response.ok) {
                throw new Error(`שגיאה בטעינת הקובץ: ${response.status} ${response.statusText}`);
            }
            return response.text();
        })
        .then(data => {
            console.log("✅ תוכן השירותים נטען בהצלחה!");
            document.getElementById("services-content").innerHTML = `<pre>${data}</pre>`;
        })
        .catch(error => {
            console.error("❌ שגיאה בטעינת השירותים:", error);
            document.getElementById("services-content").innerHTML = "<p>⚠ לא ניתן לטעון את השירותים.</p>";
        });

    // 📌 פונקציה להוספת כפתור העתקה לכל קטע קוד
    document.querySelectorAll("pre").forEach(pre => {
        const button = document.createElement("button");
        button.className = "copy-btn";
        button.innerText = "העתק קוד";

        button.addEventListener("click", function () {
            const code = pre.querySelector("code") ? pre.querySelector("code").innerText : pre.innerText;
            navigator.clipboard.writeText(code).then(() => {
                button.innerText = "הועתק!";
                setTimeout(() => { button.innerText = "העתק קוד"; }, 2000);
            }).catch(err => {
                console.error("❌ שגיאה בהעתקה:", err);
            });
        });

        pre.style.position = "relative";
        pre.appendChild(button);
    });

    console.log("📌 הסקריפט נטען בהצלחה.");

    // 📌 פונקציה לטיפול בכפתורי "קרא עוד"
    document.querySelectorAll(".read-more").forEach(button => {
        button.addEventListener("click", function () {
            const fullText = this.previousElementSibling;
            if (fullText.classList.contains("hidden")) {
                fullText.classList.remove("hidden");
                fullText.classList.add("inline"); // מציג את הטקסט בשורה אחת
                this.textContent = "הסתר";
            } else {
                fullText.classList.add("hidden");
                fullText.classList.remove("inline");
                this.textContent = "קרא עוד";
            }
        });
    });
});
