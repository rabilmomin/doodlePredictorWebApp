const canvas = document.getElementById("doodle-canvas");
const submit_canvas = document.getElementById("submit-canvas");
const clear_canvas = document.getElementById("clear-canvas");
const ctx = canvas.getContext("2d", { alpha: false });
const prediction_html = document.getElementById("prediction-list");
ctx.fillStyle = "white";
ctx.fillRect(0, 0, 150, 100);

let drawing_flag = false;


window.addEventListener("load", ()=> {
    // get offsets for canvas
    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;
    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
})

const draw = (e) =>{
    if (drawing_flag){
        ctx.lineTo(e.offsetX, e.offsetY); // Create a line based on mouse pointer location
        ctx.stroke(); // Fill in that line with color
    }
    else {
        return;
    }

}

canvas.addEventListener("mousedown", () =>{
    drawing_flag = true;
    ctx.beginPath(); // reset path, so we don't use old path when we invoked mouseup
    ctx.lineWidth = 5;
})

canvas.addEventListener("mouseup", () =>{
    drawing_flag = false;
})

canvas.addEventListener("mouseleave", ()=>{
    drawing_flag = false;
})


canvas.addEventListener("mousemove", draw);

clear_canvas.addEventListener("click", () =>{
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
})

submit_canvas.addEventListener("click", () =>{
    //console.log(canvas.toDataURL());
    sendCanvas(canvas.toDataURL());
})


function sendCanvas(canvas_data){
    const post_object = new XMLHttpRequest();
    post_object.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200){
            while(prediction_html.firstChild)
            {
                prediction_html.removeChild(prediction_html.firstChild);
            }
            let prediction_list = this.response;
            prediction_list = JSON.parse(prediction_list);
            console.log(prediction_list);
            for (let k = 0; k < prediction_list.length; k++)
            {
                let li = document.createElement("li");
                li.setAttribute("class", "prediction-item")
                li.appendChild(document.createTextNode(prediction_list[k][0] + " " + Number.parseFloat(prediction_list[k][1]).toFixed(2) + "%"));
                console.log(prediction_list[k]);
                prediction_html.appendChild(li);
            }

            
        }
    }

    post_object.open("POST", '/predict');

    let form_data = new FormData();
    form_data.append("canvas", canvas_data);
    post_object.send(form_data);
}