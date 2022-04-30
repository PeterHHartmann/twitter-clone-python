try {
    document.getElementById('auth-nav').addEventListener('click', (e) => {
        document.getElementById('logout-dropup').classList.toggle('hidden');
        document.getElementById('auth-nav').classList.toggle('activated');
    });
} catch {}

const toggle_follow_user = async(follow_btn) => {
    const is_following = Number(follow_btn.dataset.following);
    const user_name = follow_btn.dataset.user;
    const method = is_following ? 'DELETE' : 'POST';
    const response = await fetch(`/follow/${user_name}`, {
        method: method
    });
    if (response.ok) {
        for (let btn of document.querySelectorAll(`button[data-user=${user_name}]`)){
            btn.dataset.following = is_following ? '0' : '1';
            btn.innerHTML = is_following ? 'Follow' : 'Unfollow';
            btn.className = is_following ? 'btn-dark' : 'btn-light';
        };
    };
}