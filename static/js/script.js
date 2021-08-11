const btnAdd = document.querySelector("div#btn button.btn-adicionar")
const btnCancel = document.querySelector("div#btn button.btn-cancelar")
const areaCatalogo = document.querySelector("section#catalogo")
const areaAdicionar = document.querySelector("section#add-item")
const btnCadastrar = document.querySelector("section#add-item button")
const inputNome = document.querySelector("section#add-item input#nome")
const inputValor = document.querySelector("section#add-item input#valor")
const inputQuantidade = document.querySelector("section#add-item input#quantidade")

// Arrow function que valida os campos nome (obrigatorio), valor e quantidade (ambos numéricos)
const validateCadastro = (nome, valor, quantidade) => nome && valor && quantidade ? true : false
const btnFormMod = callback => {
    if(callback){
        btnCadastrar.removeAttribute("disabled")
        btnCadastrar.classList.remove("btn-disable")
        btnCadastrar.classList.add("btn-active")
    }
    else{
        btnCadastrar.setAttribute("disabled", "")
        btnCadastrar.classList.remove("btn-active")
        btnCadastrar.classList.add("btn-disable")
    }
}

const validNumber = value => {
    let regex = /[^0-9.]+/
    return regex.test(value)
}

let nome = false
let valor = false
let quantidade = false

btnCancel.style.display = 'none'
areaAdicionar.style.display = 'none'
btnAdd.style.display = 'block'
areaCatalogo.style.display = 'flex'

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

inputNome.addEventListener("keyup", function(){
    if(this.value.length < 1)
        nome = false
    else
        nome = true

    console.log(this.value)
    console.log(nome, valor, quantidade)
    btnFormMod(validateCadastro(nome, valor, quantidade))
})

inputValor.addEventListener("keyup", function(){
    if(validNumber(this.value))
        valor = false
    else
        valor = true
    
    console.log(Number(this.value))
    console.log(nome, valor, quantidade)
    btnFormMod(validateCadastro(nome, valor, quantidade))
})

inputQuantidade.addEventListener("keyup", function(){
    if(validNumber(this.value))
        quantidade = false
    else
        quantidade = true
    
    console.log(Number(this.value))
    console.log(nome, valor, quantidade)

    btnFormMod(validateCadastro(nome, valor, quantidade))
})