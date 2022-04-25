const follow_user = async (user_name) => {
    console.log('following:', user_name);

    const response = await fetch(`/follow/${user_name}`, {
        method: 'POST',
        body: JSON.stringify({'user_name': user_name})
    })

    console.log(response);

}

window.addEventListener('load', async () => {
    const response = await fetch('/follow/whotofollow', {
        method: 'GET'
    });

    body = await response.json()
    const follows_nav = document.getElementById('follows-nav');
    for (let user of body.users){
        const container = document.createElement('div')

        const user_info_div = document.createElement('div');
        user_info_div.className = 'user-info';
        const pfp = document.createElement('img')
        pfp.src = `/image/${user.user_name}/pfp.jpg`
        pfp.addEventListener('error', function(){
            this.src = `/image/default-pfp.jpg`
        });
        pfp.className = 'person-pfp'
        
        const user_text_div = document.createElement('div');
        user_text_div.className = 'user-text'
        const user_handle_anchor = document.createElement('a')
        user_handle_anchor.className = 'person-handle'
        user_handle_anchor.href = `/user/${user.user_name}`
        user_handle_anchor.innerText = user.display_name
        const user_name_p = document.createElement('p')
        user_name_p.className = 'person-username'
        user_name_p.innerText = '@' + user.user_name
        
        user_text_div.appendChild(user_handle_anchor)
        user_text_div.appendChild(user_name_p)
        
        const follow_btn = document.createElement('button')
        follow_btn.innerText = 'Follow'
        follow_btn.dataset.user = user.user_name

        follow_btn.addEventListener('click', async () => { await follow_user(user.user_name)})

        user_info_div.appendChild(pfp)
        user_info_div.appendChild(user_text_div)
        container.appendChild(user_info_div)
        container.appendChild(follow_btn)
        follows_nav.appendChild(container)

    }
});