//seleciona item menu
var menuItem = document.querySelectorAll('.item-menu')
function selectLink(){
    menuItem.forEach((item)=>
        item.classList.remove('ativo')
    )
    this.classList.add('ativo')
}
menuItem.forEach((item)=>
    item.addEventListener('click', selectLink)
)

//expandir menu

var btnexp = document.querySelector('#btnexp')
var menuSide = document.querySelector('.menulateral')

btnexp.addEventListener('click', function(){
    menuSide.classList.toggle('expandir')
})

function confirmar(usuarioId) {
    // Exibe um diálogo de confirmação
    var confirmacao = confirm("Tem certeza que deseja excluir este usuário?");
    
    // Se o usuário confirmar a exclusão
    if (confirmacao) {
        // Aqui você pode enviar uma requisição para o backend, passando o ID do usuário a ser excluído
        // Por exemplo, utilizando fetch() ou XMLHttpRequest para fazer uma requisição AJAX
        // Aqui está um exemplo básico de como poderia ser feito com fetch():
        fetch('/excluirusuario/' + usuarioId, {
            method: 'DELETE', // Assumindo que você esteja usando RESTful API e DELETE para exclusão
        })
        .then(response => {
            // Aqui você pode lidar com a resposta do backend, como redirecionar o usuário ou atualizar a página
            // Por exemplo, se o backend retornar um status 200 (OK), você pode redirecionar o usuário para uma página de confirmação
            if (response.status === 200) {
                window.location.href = '/exclusaosucesso';
            } else {
                // Caso contrário, você pode exibir uma mensagem de erro
                alert("Erro ao excluir usuário. Por favor, tente novamente.");
            }
        })
        .catch(error => {
            // Em caso de erro na requisição, você pode exibir uma mensagem de erro
            console.error('Erro ao excluir usuário:', error);
            alert("Erro ao excluir usuário. Por favor, tente novamente.");
        });
    }
}
