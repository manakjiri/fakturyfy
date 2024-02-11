import axios from "axios";

export default function useFetching() {

    function getCookie(name: string) {
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
    
    const Axios = axios.create({
        baseURL: `http://${window.location.hostname}:${window.location.port}/api/`,
        timeout: 5000,
    });
    
    Axios.defaults.headers.post['X-CSRFToken'] = getCookie('csrftoken');
    Axios.defaults.headers.post['Accept'] = 'application/json';
    Axios.defaults.headers.post['Content-Type'] = 'application/json';
    Axios.defaults.headers.delete['X-CSRFToken'] = getCookie('csrftoken');
    Axios.defaults.headers.put['X-CSRFToken'] = getCookie('csrftoken');

    return {Axios}
}