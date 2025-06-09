document.addEventListener("DOMContentLoaded", function() {
    // --- CSRF Token Setup for Fetch API ---
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    // --- Notice System ---
    const noticeButton = document.getElementById("notice-button");
    const noticeDropdown = document.getElementById("notice-dropdown");
    const noticeCountBadge = document.getElementById("notice-count");
    const noticeModal = document.getElementById("notice-modal");
    const noticeModalTitle = document.getElementById("notice-text-title");
    const noticeModalContent = document.getElementById("notice-text-content");
    const closeModalButton = noticeModal.querySelector(".close-button");

    function updateUnreadCount() {
        const unreadNotices = noticeDropdown.querySelectorAll(".notice-item.unread");
        if (unreadNotices.length > 0) {
            noticeCountBadge.textContent = unreadNotices.length;
            noticeCountBadge.style.display = "inline-block"; // or "flex" if needed
        } else {
            noticeCountBadge.style.display = "none";
        }
    }

    if (noticeButton && noticeDropdown) {
        updateUnreadCount(); // Initial count update

        noticeButton.addEventListener("click", function(event) {
            event.stopPropagation();
            const isOpen = noticeDropdown.classList.toggle("is-open");
            noticeButton.setAttribute("aria-expanded", isOpen.toString());
        });

        document.addEventListener("click", function(event) {
            if (noticeDropdown.classList.contains("is-open") && 
                !noticeDropdown.contains(event.target) && 
                event.target !== noticeButton &&
                !noticeButton.contains(event.target) // ボタン内の要素クリックも考慮
                ) {
                noticeDropdown.classList.remove("is-open");
                noticeButton.setAttribute("aria-expanded", "false");
            }
        });

        noticeDropdown.addEventListener("click", function(event) {
            event.stopPropagation(); // Prevent closing dropdown when clicking inside
            const targetItem = event.target.closest(".notice-item");
            if (targetItem) {
                const title = targetItem.textContent.trim(); // Or get title from a data attribute if complex
                const content = targetItem.getAttribute("data-content");
                const noticeId = targetItem.getAttribute("data-id");
                const readUrl = targetItem.getAttribute("data-read-url");

                noticeModalTitle.textContent = title; // お知らせのタイトルをモーダルに表示
                noticeModalContent.textContent = content;
                noticeModal.classList.add("is-open");
                noticeModal.setAttribute("aria-hidden", "false"); // For accessibility
                
                // Close dropdown after opening modal
                noticeDropdown.classList.remove("is-open");
                noticeButton.setAttribute("aria-expanded", "false");

                if (targetItem.classList.contains("unread") && readUrl) {
                    fetch(readUrl, {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                            "X-CSRFToken": csrftoken
                        },
                        // body: JSON.stringify({ read: true }) // 必要ならバックエンドにデータを送る
                    })
                    .then(response => {
                        if (!response.ok) {
                            // If HTTP-status is 200-299
                            // Throw an error to be caught by the .catch() block
                            return response.json().then(errData => {
                                throw new Error(errData.error || `サーバーエラー: ${response.status}`);
                            });
                        }
                        return response.json();
                    })
                    .then(data => {
                        if (data.success) {
                            targetItem.classList.remove("unread");
                            targetItem.classList.add("read");
                            updateUnreadCount();
                            console.log("Notice marked as read:", noticeId);
                        } else {
                            console.error("Failed to mark notice as read:", data.error || "Unknown error");
                            // Optionally, show an error message to the user
                        }
                    })
                    .catch(error => {
                        console.error("Error marking notice as read:", error);
                        // Optionally, show an error message to the user
                        // alert(`既読処理に失敗しました: ${error.message}`);
                    });
                }
            }
        });
    }

    // Modal close functionality
    if (noticeModal && closeModalButton) {
        closeModalButton.addEventListener("click", function() {
            noticeModal.classList.remove("is-open");
            noticeModal.setAttribute("aria-hidden", "true");
        });

        noticeModal.addEventListener("click", function(event) {
            // Close if clicked on the modal backdrop (outside .modal-content)
            if (event.target === noticeModal) {
                noticeModal.classList.remove("is-open");
                noticeModal.setAttribute("aria-hidden", "true");
            }
        });

        // Close with Escape key
        document.addEventListener("keydown", function(event) {
            if (event.key === "Escape" && noticeModal.classList.contains("is-open")) {
                noticeModal.classList.remove("is-open");
                noticeModal.setAttribute("aria-hidden", "true");
            }
        });
    }

    // --- Smooth scroll for anchor links (optional) ---
    // document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    //     anchor.addEventListener('click', function (e) {
    //         e.preventDefault();
    //         document.querySelector(this.getAttribute('href')).scrollIntoView({
    //             behavior: 'smooth'
    //         });
    //     });
    // });

    // --- Other JS functionalities can be added below ---

});