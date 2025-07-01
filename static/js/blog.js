window.addEventListener('load', async function (event) {
    event.preventDefault()
    let responseblog = await this.fetch('http://127.0.0.1:8000/en/api/blogs/')
    let responseblogData = await responseblog.json()
    let bloglist = this.document.getElementById('blogsveryveryown')
    for (data of responseblogData){
        bloglist.innerHTML += `
        <option value="${data.id}">${data.title}</option>
        `
    }
})

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

let form = document.getElementById('blog-ultra-comment')
form.addEventListener('submit', async function (event) {
    event.preventDefault()
    let formData = new FormData(form)
    let response = await fetch('http://127.0.0.1:8000/en/api/comments/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken
        },
        body: formData
    })
})