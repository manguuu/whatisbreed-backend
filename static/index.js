const realUpload = document.querySelector('.image-input');
const ret = document.querySelector('#ret')


realUpload.addEventListener('change', async (e) => {
    const file = e.currentTarget.files[0];
    console.log(file);
    const form_data = new FormData()
    form_data.append("file", file)
    
    const response = await fetch('/files/', {
        method: 'POST',
        body: form_data
    });
    
    const result = await response.json();
    console.log(result)
    const pred = result.predict
    let mx_prob = -1.0
    let breed = ''
    for (const key in pred) {
        console.log(key)
        let prob = pred[key];
        console.log(prob)
        if (prob > mx_prob) {
            mx_prob = prob;
            breed = key;
        }
    }

    ret.innerHTML = `${mx_prob * 100}% ${breed}`
    const origin_img = document.querySelector('#origin-img');
    const lime_img = document.querySelector('#lime-img');
    origin_img.src = result.origin_file_path;
    lime_img.src = result.lime_file_path
    // document.body.appendChild(img_tag);
});