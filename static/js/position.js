'use strict';


window.addEventListener('load', () => {
    const up_image = document.getElementById('up_image');
    const bg_image = document.getElementById('selected_bg');
    const send_coords_btn = document.getElementById('send-coords-to-backend');

    const submit_coords = document.getElementById('submit-coords');
    const x_pos = document.getElementById('x-coords');
    const y_pos = document.getElementById('y-coords');


    up_image.ondrag = (DragEvent) => {
        up_image.style.left = DragEvent.clientX;
        up_image.style.top = DragEvent.clientY;
        console.log(DragEvent.clientX, DragEvent.clientY);
    };
    
    up_image.ondragend = (DragEvent) => {
        up_image.style.left = DragEvent.clientX;
        up_image.style.top = DragEvent.clientY;
    };

    send_coords_btn.onclick = () => {
        
        x_pos.value = up_image.offsetLeft - bg_image.offsetLeft;
        y_pos.value = up_image.offsetTop - bg_image.offsetTop;

        if (x_pos.value < 0 || y_pos.value < 0) {
            alert("Posicionamiento Incorrecto");
        } else {
            submit_coords.click();
        }
    }
});