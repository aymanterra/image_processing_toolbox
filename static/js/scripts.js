var elements = document.getElementsByClassName('sidebar-nav-link')
for (var i = 0; i < elements.length; i++) {
    elements[i].classList.remove('active')
}

const path = document.location.pathname.split('/')[1]
let x = undefined
if (path == "removing_noise_mask") {
    x = document.getElementsByClassName('sidebar-nav-link')["removing_noise"]
} else {
    x = document.getElementsByClassName('sidebar-nav-link')[path]
}
if (x) {
    x.classList.add('active')
}

let file = document.querySelector('#file')
if (file) {
    file.addEventListener("change", function() {
        const fileList = this.files; /* now you can work with the file list */
        if (fileList.length > 0) {
            file_label = document.querySelector('#file-label')
            if (file_label) {
                file_label.innerHTML = fileList[0].name
            }
        }
    }, false)
}

let noise_type = document.querySelector('#noise_type')
let removal_type_selector = document.querySelector('#removal_type')
if (noise_type) {
    noise_type.addEventListener("change", function() {
        const noise_type_value = this.value;
        noise_type_elements = document.getElementsByClassName('noise_type')
        for (var i = 0; i < noise_type_elements.length; i++) {
            if (noise_type_value == "Periodic" && removal_type_selector) {
                removal_type_selector.required = 1
            }
            else if (removal_type_selector) {
                removal_type_selector.required = 0
            }

            if (noise_type_elements[i].id == noise_type_value) {
                noise_type_elements[i].hidden = 0
            }
            else {
                noise_type_elements[i].hidden = 1
            }
        }
    }, false)
}

let pixels = []
const mask_img = document.querySelector("#mask_img")
if (mask_img) {
    mask_img.addEventListener("click", function (event) {
        console.log(event.offsetX, event.offsetY)
        pixels.push({"x": event.offsetX, "y": event.offsetY})
        document.querySelector("#selected_pixels").value = JSON.stringify(pixels)
        document.querySelector("#selected_pixels_text").innerHTML = JSON.stringify(pixels, undefined, 4)
    })
}
