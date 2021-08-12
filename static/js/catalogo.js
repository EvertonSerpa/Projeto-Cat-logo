function abrirMenu(){
    document.getElementById('submenu').style.width = '18%';
    document.getElementById('perfilFechar').style.display = 'block';
    document.getElementById('perfilAbrir').style.display = 'none';
}
 
function fecharMenu(){
    document.getElementById('submenu').style.width = '0';
    document.getElementById('perfilFechar').style.display = 'none';
    document.getElementById('perfilAbrir').style.display = 'block';
}