document.getElementById('auth-nav').addEventListener('click', (e) => {
    document.getElementById('logout-dropup').classList.toggle('hidden');
    document.getElementById('auth-nav').classList.toggle('activated');
});

window.addEventListener('load', (e) => {
    for (let tweet of document.querySelectorAll("[id^='tweetid']")){
        const timestamp = tweet.dataset.timestamp * 1000;
        const current_time = Date.now()
        let time_since_ms = current_time - timestamp;
        let time_since_hours = time_since_ms / 1000 / 60 / 60;
        let time_since_tweeted = Math.round(time_since_hours);
        if (time_since_tweeted < 1){
            time_since_tweeted = '· right now'
        } else {
            time_since_tweeted = `· ${time_since_tweeted}h`
        }
        tweet.querySelector(".tweeted-date").innerHTML = time_since_tweeted
    }
});

