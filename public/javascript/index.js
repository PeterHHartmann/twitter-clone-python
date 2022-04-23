const auto_grow = (element) => {
    element.style.height = "5px";
    element.style.height = (element.scrollHeight)+"px";
};

const toggle_modal = (modal_id) => {
    document.getElementById(modal_id).classList.toggle('hidden');
};

document.getElementById('modal-bg').addEventListener('click', (e) => {
    toggle_modal('modal-mount');
    const modals = document.getElementsByClassName('modal-content')
    for ( let modal of modals){
        if(!modal.classList.contains('hidden')){
            modal.classList.add('hidden')
        }
    }
});

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

document.getElementById('new-tweet-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    data = new FormData();
    data.append('tweet_text', document.getElementById('tweet-text').value)
    data.append('tweet-img', document.getElementById('file-input').files[0], 'tweet-img.jpg')

    const response = await fetch('/user/tweet', {
        method: "POST",
        body: data
    });

});

window.addEventListener('load', () => {
    const toast = document.querySelector('toast');
    if (toast){
        toast.classList.remove('hidden')
        requestAnimationFrame(() => {
            toast.classList.add('showing')
        });
        setTimeout(() => {
            requestAnimationFrame(() => {
                toast.classList.remove('showing')
                toast.classList.remove('hidden')
            })
        }, 2500);
    }
});

