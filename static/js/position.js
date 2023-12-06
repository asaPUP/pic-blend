'use strict';


window.addEventListener('load', () => {
    const up_image = document.getElementById('up_image');
    const bg_image = document.getElementById('selected_bg');
    const send_coords_btn = document.getElementById('send-coords-to-backend');

    const submit_coords = document.getElementById('submit-coords');
    const x_pos = document.getElementById('x-coords');
    const y_pos = document.getElementById('y-coords');
    const error_message = document.getElementById('message');

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
        error_message.style.display = 'none';

        x_pos.value = up_image.offsetLeft - bg_image.offsetLeft;
        y_pos.value = up_image.offsetTop - bg_image.offsetTop;

        if (x_pos.value + up_image.style.width < bg_image.offsetWidth
            && y_pos.value + up_image.style.height < bg_image.offsetHeight
            && parseInt(x_pos.value) >= 0 && parseInt(y_pos.value) >= 0) {
            
            console.log(x_pos.value, y_pos.value);

            submit_coords.click();
        } else {
            error_message.style.display = 'block';
        }
    }
});