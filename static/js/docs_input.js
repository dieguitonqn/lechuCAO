




const habilitar = document.getElementById("numDocs");
habilitar.addEventListener("keydown", preInfo);
// habilitar.addEventListener("keyup",(e)=>{
habilitar.addEventListener("change", hijo);
habilitar.addEventListener("keyup", hijo);
const maxDoc = document.getElementById('maxDocs');
const numero = document.getElementById("numDocs");

var preFileDesc = [], preFileCod = [], preFileRev = [], preFileDoc = [];

function preInfo() {

    if (numero.value !== "") {

        for (let i = 1; i <= numero.value; i++) {
            let fileDoc = document.forms['formIngreso'][`fileDoc${i}`].files[0]; //getElementById(`fileDoc${i}`);
            let fileDesc = document.getElementById(`fileDesc${i}`).value;

            let fileCod = document.getElementById(`fileCod${i}`).value;
            let fileRev = document.getElementById(`fileRev${i}`).value;
            preFileDoc[i] = fileDoc;
            preFileDesc[i] = fileDesc;

            preFileCod[i] = fileCod;
            preFileRev[i] = fileRev;

            console.log("Ruta del documento " + i + ":" + preFileDoc[i]);
            console.log("Descripcion del documento " + i + ":" + preFileDesc[i]);

            console.log("Codigo del documento " + i + ":" + preFileCod[i]);
            console.log("Revision del documento " + i + ":" + preFileRev[i]);
        }
    }
}



function hijo() {


    const formulario = document.getElementById("formDocs");

    const formsNuevos = document.createDocumentFragment();
    const inputsNuevos = document.getElementById("ingresos");

    const tbodyInputs = document.createElement("TBODY");
    tbodyInputs.setAttribute("id", "ingresos");

    for (i = 0; i < Number(numero.value); i++) {
        if (!preFileCod[i + 1]) {
            preFileCod[i + 1] = "";
        }

        if (!preFileDesc[i + 1]) {
            preFileDesc[i + 1] = "";
        }
        if (!preFileRev[i + 1]) {
            preFileRev[i + 1] = "";
        }
        if (!preFileDoc[i + 1]) {
            preFileDoc[i + 1] = "";
        }


        //Creo todos los elementos de la fila de la tabla
        const trInput = document.createElement("TR");
        const tdInputItem = document.createElement("TD");
        const tdInputFile = document.createElement("TD");
        const tdInputCod = document.createElement("TD");
        const tdInputDesc = document.createElement("TD");
        const tdInputRev = document.createElement("TD");

        //creo los elementos de cada "TD"
        const inputFile = document.createElement("INPUT");
        const inputCod = document.createElement("INPUT");
        const inputDesc = document.createElement("INPUT");
        const inputRev = document.createElement("INPUT");


        //Defino los atributos de cada INPUT
        //-->
        tdInputItem.innerText = i + 1;

        //--> INPUT FILE
        inputFile.setAttribute("type", "file");
        inputFile.setAttribute("id", `fileDoc${i + 1}`);
        // inputFile.setAttribute("name", `fileDoc${i + 1}`);
        inputFile.setAttribute("name", `fileDoc`);
        inputFile.setAttribute("accept", "application/pdf");
        inputFile.setAttribute("required", "true");
        inputFile.setAttribute("style", "width: 500px");
        inputFile.classList.add("form-control");


        //-->INPUT COD
        inputCod.setAttribute("type", "text");
        // inputCod.setAttribute("id", `fileCod${i + 1}`);
        inputCod.setAttribute("id", `fileCod`);

        inputCod.setAttribute("name", `fileCod${i + 1}`);
        inputCod.setAttribute("required", "true");
        inputCod.classList.add("form-control");
        inputCod.setAttribute("value", preFileCod[i + 1]);


        //--> INPUT Desc
        inputDesc.setAttribute("type", "text");
        inputDesc.setAttribute("id", `fileDesc${i + 1}`);
        inputDesc.setAttribute("name", `fileDesc${i + 1}`);
        inputDesc.setAttribute("required", "true");
        inputDesc.setAttribute("style", "min-width: 200px;text-overflow: ellipsis");
        inputDesc.classList.add("form-control");
        inputDesc.setAttribute("value", preFileDesc[i + 1]);

        //-->INPUT Rev
        inputRev.setAttribute("type", "text");
        inputRev.setAttribute("id", `fileRev${i + 1}`);
        inputRev.setAttribute("name", `fileRev${i + 1}`);
        inputRev.setAttribute("required", "true");
        inputRev.classList.add("form-control");
        inputRev.setAttribute("style", "max-width:3vw");
        inputRev.setAttribute("value", preFileRev[i + 1]);


        //Agrego los inputs a cada TD
        tdInputFile.appendChild(inputFile);
        tdInputCod.appendChild(inputCod);
        tdInputDesc.appendChild(inputDesc);
        tdInputRev.appendChild(inputRev);

        //Finalmente, agrego todos los TD al TR
        trInput.appendChild(tdInputItem);
        trInput.appendChild(tdInputFile);
        trInput.appendChild(tdInputCod);
        trInput.appendChild(tdInputDesc);
        trInput.appendChild(tdInputRev);

        formsNuevos.appendChild(trInput);

    }

    tbodyInputs.appendChild(formsNuevos)
    formulario.replaceChild(tbodyInputs, inputsNuevos);

    // Acá va la parte de agregado de eventos
    for (i = 0; i < Number(numDocs.value); i++) {
        let otro = document.getElementById(`fileDoc${i + 1}`);
        otro.addEventListener("change", FileSize);
    }


};



function FileSize() {
    let docSize = [];
    let maxDocsSize = 0;
    const formIngreso = document.forms['formIngreso'];

    for (let i = 0; i < Number(numDocs.value); i++) {
        const fileInput = formIngreso[`fileDoc${i + 1}`];
        if (fileInput.files[0]) {
            docSize[i] = fileInput.files[0].size / (2 ** 20);
            maxDocsSize += docSize[i];
        }
    }

    maxDoc.innerHTML = maxDocsSize.toFixed(2);

    const fondo = document.getElementById('maxDocsLabel');
    fondo.style.backgroundColor = maxDocsSize > 45 ? 'red' : maxDocsSize > 35 ? 'yellow' : '';
}




// const form = document.getElementById('formIngreso');
// const submitButton = form.querySelector('button[type="submit"]');
// const numDocsInput = document.getElementById('numDocs');
// const ingresosTable = document.getElementById('ingresos');
// form.addEventListener('submit', (event) => {
//     event.preventDefault(); // Prevent default form submission

//     // Prepare form data as a list of objects
//     const formData = [];
//     for (let i = 1; i <= numDocsInput.value; i++) {
//         const fileInput = document.getElementById(`fileDoc${i}`);
//         const codeInput = document.getElementById(`fileCod${i}`);
//         const descInput = document.getElementById(`fileDesc${i}`);
//         const revInput = document.getElementById(`fileRev${i}`);

//         formData.push({
//             file: fileInput.files[0], // Assuming single file selection
//             codigo: codeInput.value,
//             descripcion: descInput.value,
//             revision: revInput.value,
//         });
//     }   

//     const bodyJ = JSON.stringify({ obra: document.getElementById('obra').value, form_data: formData })
//     console.log(bodyJ);
//     // Send the data to the server using Fetch API (or any preferred method)
//     fetch('/ingreso_docs', {
//         method: 'POST',
//         body: JSON.stringify({ obra: document.getElementById('obra').value, form_data: formData }), // Add obra data
//     })
//         .then(response => response.json())
//         .then(data => {
//             console.log('Success:', data);
//             // Handle successful submission (e.g., display message, reset form)
//         })
//         .catch(error => {
//             console.error('Error:', error);
//         })
//     }
// )
//