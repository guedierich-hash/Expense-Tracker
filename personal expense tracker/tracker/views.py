from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from .models import Transaction
from .forms import RegisterForm, TransactionForm


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'tracker/register.html', {'form': form})


@login_required
def dashboard(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')[:10]
    income_total = sum(t.amount for t in Transaction.objects.filter(user=request.user, transaction_type='income'))
    expense_total = sum(t.amount for t in Transaction.objects.filter(user=request.user, transaction_type='expense'))
    balance = income_total - expense_total
    context = {
        'transactions': transactions,
        'income_total': income_total,
        'expense_total': expense_total,
        'balance': balance,
    }
    return render(request, 'tracker/dashboard.html', context)


@login_required
def transaction_list(request):
    transactions = Transaction.objects.filter(user=request.user)
    return render(request, 'tracker/transaction_list.html', {'transactions': transactions})


@login_required
def transaction_add(request):
    if request.method == 'POST':
        form = TransactionForm(request.user, request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, 'Transaction added.')
            return redirect('dashboard')
    else:
        form = TransactionForm(request.user)
    return render(request, 'tracker/transaction_form.html', {'form': form, 'title': 'Add Transaction'})
