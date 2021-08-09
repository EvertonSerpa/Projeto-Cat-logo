const btnAdd = document.querySelector("div#btn button.btn-adicionar")
const btnCancel = document.querySelector("div#btn button.btn-cancelar")
const areaCatalogo = document.querySelector("section#catalogo")
const areaAdicionar = document.querySelector("section#add-item")

btnCancel.style.display = 'None'
areaAdicionar.style.display = 'None'
btnAdd.style.display = 'Block'
areaCatalogo.style.display = 'Flex'

btnAdd.addEventListener('click', () => {
    btnCancel.style.display = 'Block'
    areaAdicionar.style.display = 'Flex'
    btnAdd.style.display = 'None'
    areaCatalogo.style.display = 'None'
})

btnCancel.addEventListener('click', () => {
    btnCancel.style.display = 'None'
    areaAdicionar.style.display = 'None'
    btnAdd.style.display = 'Block'
    areaCatalogo.style.display = 'Flex'
})