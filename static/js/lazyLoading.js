const scroller = document.getElementById("scroller");
const template = document.getElementById("post_template");

const loaded = document.getElementById("loaded");

const sentinel = document.getElementById("sentinel");
let counter = 0;

const fetchData = async () => {
    const response = await fetch(
        `http://127.0.0.1:5000/api/floods?c=${counter}`
    );
    const data = await response.json();

    if (!data.length) {
        sentinel.innerHTML = "No more floods!";
    }

    for (let i = 0; i < data.length; i++) {
        let template_clone = template.content.cloneNode(true);

        template_clone.getElementById("full_link").href = data[i]["full_link"];
        template_clone.getElementById("created").innerHTML = data[i]["created"];
        template_clone.getElementById("title").innerHTML = data[i]["title"];
        template_clone.getElementById("selftext").innerHTML =
            data[i]["selftext"];

        scroller.appendChild(template_clone);
        counter += 1;
        loaded.innerText = counter;
    }
};

const observer = new IntersectionObserver((entries) => {
    if (entries[0].intersectionRatio <= 0) {
        return;
    }

    fetchData();
});
observer.observe(sentinel);
