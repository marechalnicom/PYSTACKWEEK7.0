from django.shortcuts import render, redirect
from .models import Conta, Categoria
from django.contrib import messages
from django.contrib.messages import constants
from .utils import calcula_total, formata_float

def home(request):
    contas = Conta.objects.all()
    if contas.exists():
        saldo_total = calcula_total(contas, 'valor')
        #saldo_total = contas.aggregate(Sum('valor'))
        saldo_total = formata_float(saldo_total)
        for conta in contas:
            conta.valor = formata_float(conta.valor)
    else:        
        saldo_total = "0,00"
    
    context = {
        'contas': contas,
        'saldo_total': saldo_total,
        }
    return render(request, 'home.html', context)

def gerenciar(request):
    contas = Conta.objects.all()
    categorias = Categoria.objects.all()
    if contas.exists():
        total_contas = calcula_total(contas, 'valor')#contas.aggregate(Sum('valor'))
        total_contas = formata_float(total_contas)
        for conta in contas:
            conta.valor = formata_float(conta.valor)
    else:        
        total_contas = "0,00"
    context = {
        'contas': contas,
        'total_contas': total_contas,
        'categorias': categorias,
        'banco_choices': Conta.banco_choices,
        'tipo_choices': Conta.tipo_choices,
        }
    return render(request, 'gerenciar.html', context)

def cadastrar_banco(request):
    apelido = request.POST.get('apelido')
    banco = request.POST.get('banco')
    tipo = request.POST.get('tipo')
    valor = request.POST.get('valor')
    icone = request.FILES.get('icone')
    
    if len(apelido.strip()) == 0 or len(valor.strip()) == 0:
        messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
        return redirect('/perfil/gerenciar/')
    
    conta = Conta(
        apelido = apelido,
        banco=banco,
        tipo=tipo,
        valor=valor,
        icone=icone
    )

    conta.save()
    messages.add_message(request, constants.SUCCESS, 'Conta salva com Sucesso')
    return redirect('/perfil/gerenciar/')

def deletar_banco(request, id):
    conta = Conta.objects.get(id=id)
    conta.delete()
    
    messages.add_message(request, constants.SUCCESS, 'Conta removida com sucesso')
    return redirect('/perfil/gerenciar/')

def cadastrar_categoria(request):
    nome = request.POST.get('categoria')
    essencial = bool(request.POST.get('essencial'))
    if len(nome.strip()) == 0 or not isinstance(essencial,bool):
        messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
        return redirect('/perfil/gerenciar/')
    categoria = Categoria(
        categoria=nome,
        essencial=essencial
    )
    categoria.save()
    messages.add_message(request, constants.SUCCESS, 'Categoria cadastrada com sucesso')
    return redirect('/perfil/gerenciar/')
def update_categoria(request, id):
    categoria = Categoria.objects.get(id=id)
    if categoria:
        categoria.essencial = not categoria.essencial

        categoria.save()

    return redirect('/perfil/gerenciar/')