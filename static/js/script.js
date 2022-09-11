// const callback = () => {}

// const observer = new IntersectionObserver(callback)

const fetchData = async () => {
    const response = await fetch("http://127.0.0.1:5000/api/floods");
    const data = await response.json();

    console.log(data);
};

fetchData();
