window.addEventListener('load', async () => {
    const response = await fetch('/whotofollow', {
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
        const user_handle_div = document.createElement('p')
        user_handle_div.className = 'person-handle'
        user_handle_div.innerText = user.display_name
        const user_name_div = document.createElement('p')
        user_name_div.className = 'person-username'
        user_name_div.innerText = '@' + user.user_name
        
        user_text_div.appendChild(user_handle_div)
        user_text_div.appendChild(user_name_div)
        
        const follow_btn = document.createElement('button')
        follow_btn.innerText = 'Follow'

        user_info_div.appendChild(pfp)
        user_info_div.appendChild(user_text_div)
        container.appendChild(user_info_div)
        container.appendChild(follow_btn)
        follows_nav.appendChild(container)

    }
});