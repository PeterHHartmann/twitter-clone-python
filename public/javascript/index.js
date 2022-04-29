const auto_grow = (element) => {
    element.style.height = "5px";
    element.style.height = (element.scrollHeight)+"px";
};

const toggle_modal = (modal_id) => {
    document.getElementById(modal_id).classList.toggle('hidden');
};
try {
    document.getElementById('modal-bg').addEventListener('click', (e) => {
        toggle_modal('modal-mount');
        const modal_content = document.getElementById('edit-tweet-modal');
        modal_content.innerHTML = '';
        modal_content.parentNode.classList.add('hidden');
    });
} catch {}
try {
    document.getElementById('image-input').addEventListener('change', (e) => {
        e.preventDefault();
        const media_container = document.getElementById('media-container');
        media_container.innerHTML = '';
        const img = document.createElement('img');
        const button = document.createElement('button');
        button.className = 'remove-btn';
        button.innerHTML = '<svg viewBox="0 0 24 24"><g><path d="M13.414 12l5.793-5.793c.39-.39.39-1.023 0-1.414s-1.023-.39-1.414 0L12 10.586 6.207 4.793c-.39-.39-1.023-.39-1.414 0s-.39 1.023 0 1.414L10.586 12l-5.793 5.793c-.39.39-.39 1.023 0 1.414.195.195.45.293.707.293s.512-.098.707-.293L12 13.414l5.793 5.793c.195.195.45.293.707.293s.512-.098.707-.293c.39-.39.39-1.023 0-1.414L13.414 12z"></path></g></svg>'
        button.addEventListener('click', () => {
            e.preventDefault();
            media_container.innerHTML = '';
            document.getElementById('image-input').value = '';
        });
        img.src = URL.createObjectURL(e.target.files[0]);
        media_container.appendChild(button);
        media_container.appendChild(img);
    });
} catch {}

const create_tweet = (tweet_id, user_name, display_name, tweet_image_name, tweet_text, tweet_timestamp) => {
    const tweet = document.createElement('div');
    tweet.className = 'tweet';
    tweet.id = `tweetid-${tweet_id}`
    const current_time = Date.now()
    let time_since_tweeted = Math.round((current_time - tweet_timestamp) / 1000 / 60 / 60)
    if (time_since_tweeted < 1){
        time_since_tweeted = 'right now'
    } else {
        time_since_tweeted += 'h'
    }

    console.log(tweet_text);

    const pfp_image_name = document.querySelector('#session-user-pfp').src

    tweet.innerHTML =
    `<div class="tweet-container">
        <div class="pfp-container">
            <img src="${pfp_image_name}" onerror="this.src='/image/default-pfp.jpg'">
        </div>
        <div class="content-container">
            <div class="tweet-header">
                <div class="user-text">
                    <a href="/user/${user_name}">
                        <span>${display_name}</span>
                        <span>@${user_name}</span>
                    </a>
                </div>
                <div class="tweeted-date">· ${time_since_tweeted}</div>
                <div class="tweet-settings" id="tweet-settings" data-tweet_id="${tweet_id}">
                    edit
                </div>
            </div>
            <div class="tweet-content">
                ${tweet_text ? `<div class="tweet-text">${tweet_text}</div>` : ``}
                ${tweet_image_name ? `<div class="tweet-img"><img src="/tweet/${tweet_id}/${tweet_image_name}"></div>` : ``}
            </div>
        </div>
    </div>`
    tweet.dataset.tweet_id = tweet_id
    return tweet
}
try {
    document.getElementById('new-tweet-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        data = new FormData();
        const tweet_textarea = document.getElementById('tweet-text')
        const tweet_text = tweet_textarea.value
        data.append('tweet_text', tweet_text)
        tweet_textarea.value = ''
        try {
            data.append('tweet_img', document.getElementById('image-input').files[0], 'tweet-img.jpg')
        } catch {
            console.log('no image attached image to tweet');
        };
        const user_name = document.getElementById('tweet_user_name').value
        const response = await fetch(`/tweet/${user_name}`, {
            method: "POST",
            body: data
        });
        console.log(response);

        if (response.ok){
            body = await response.json();
            console.log(body);
            tweet_textarea.value = ''
            document.getElementById('image-input').value = '';
            document.getElementById('media-container').innerHTML = '';

            const tweet = create_tweet(body.tweet_id, user_name, document.querySelector('#tweet_display_name').value, body.image_name, tweet_text.trim(), body.tweet_timestamp )
            document.getElementById('tweet-deck').prepend(tweet)
            prepare_tweet_edit(tweet.querySelector('#tweet-settings'));
        }
    });
} catch {}