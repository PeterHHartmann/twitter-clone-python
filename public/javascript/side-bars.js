try {
    document.getElementById('auth-nav').addEventListener('click', (e) => {
        document.getElementById('logout-dropup').classList.toggle('hidden');
        document.getElementById('auth-nav').classList.toggle('activated');
    });
} catch {}
try {
    window.addEventListener('load', (e) => {
        for (let follow_btn of document.querySelectorAll(".follow-btn")){
            follow_btn.addEventListener('click', async (e) => {
                await fetch(`/follow/${e.target.dataset.user}`, {
                    method: 'POST'
                });
            });
        }
    });
} catch {}