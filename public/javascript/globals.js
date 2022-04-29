try {
    document.getElementById('auth-nav').addEventListener('click', (e) => {
        document.getElementById('logout-dropup').classList.toggle('hidden');
        document.getElementById('auth-nav').classList.toggle('activated');
    });
} catch (error){
    console.log(error);
}
try {
    window.addEventListener('load', (e) => {
        for (let tweet of document.querySelectorAll("[id^='tweetid']")){
            const timestamp = tweet.dataset.timestamp * 1000;
            const current_time = Date.now()
            const time_since_ms = current_time - timestamp;
            let time_since_tweeted = time_since_ms / 1000 / 60 / 60;
            let time_str = ''
            if (time_since_tweeted < 1){
                const minutes = Math.round(time_since_tweeted * 60);
                time_str = `· ${minutes}m`
            } else if (time_since_tweeted > 24) {
                const days = Math.round(time_since_tweeted / 24);
                time_str = `· ${days}d`
            } else {
                const hours = Math.round(time_since_tweeted);
                time_str = `· ${hours}h`
            }
            tweet.querySelector(".tweeted-date").innerHTML = time_str
        }
    });
} catch (error) {
    console.log(error);
}
try {
    window.addEventListener('load', (e) => {
        for (let follow_btn of document.querySelectorAll(".follow-btn")){
            follow_btn.addEventListener('click', async (e) => {
                console.log('following', e.target.dataset.user);

                const response = await fetch(`/follow/${e.target.dataset.user}`, {
                    method: 'POST'
                });
            
                console.log(response);
            });
        }
    });
} catch (error) {
    console.log(error);
}

